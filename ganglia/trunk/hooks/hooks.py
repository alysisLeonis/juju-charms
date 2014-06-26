#!/usr/bin/python

import hashlib
import os
import subprocess
import sys
from utils import (
    juju_log,
    relation_get,
    relation_set,
    relation_ids,
    relation_list,
    config_get,
    render_template,
    install,
    expose,
    configure_source,
    unit_get
    )


def checksum(sfile):
    sha256 = hashlib.sha256()  # IGNORE:E1101
    with open(sfile, 'r') as source:
        sha256.update(source.read())
    return sha256.hexdigest()

# Services
GMETAD = "gmetad"
GMOND = "ganglia-monitor"
APACHE = "apache2"

# Service Commands
START = "start"
STOP = "stop"
RESTART = "restart"
RELOAD = "reload"


def control(service_name, action):
    cmd = [
        "service",
        service_name,
        action
        ]
    if action == RESTART:
        if subprocess.call(cmd) != 0:
            control(service_name, START)
    else:
        subprocess.call(cmd)

GMETAD_CONF = "/etc/ganglia/gmetad.conf"


def configure_gmetad():
    juju_log("INFO", "Configuring gmetad for master unit")
    data_sources = {
        "self": ["localhost"]
        }
    for _rid in relation_ids("master"):
        for _unit in relation_list(_rid):
            # endpoint is set by ganglia-node
            # subordinate to indicate that
            # gmond should not be used as a
            # datasource
            _datasource = relation_get('datasource',
                                       _unit, _rid)
            if _datasource == "true":
                service_name = _unit.split('/')[0]
                if service_name not in data_sources:
                    data_sources[service_name] = []
                data_sources[service_name]\
                    .append(relation_get('private-address',
                                         _unit, _rid))

    context = {
        "data_sources": data_sources,
        "gridname": config_get("gridname")
        }

    before = checksum(GMETAD_CONF)
    with open(GMETAD_CONF, "w") as gmetad:
        gmetad.write(render_template("gmetad.conf", context))
    if before != checksum(GMETAD_CONF):
        control(GMETAD, RESTART)

GMOND_CONF = "/etc/ganglia/gmond.conf"


def configure_gmond():
    juju_log("INFO", "Configuring ganglia monitoring daemon")
    service_name = os.environ['JUJU_UNIT_NAME'].split('/')[0]
    _rids = relation_ids("head")
    masters = []
    if _rids:
        # Configure as head unit and send data to masters
        for _rid in _rids:
            for _master in relation_list(_rid):
                masters.append(relation_get('private-address',
                                            _master, _rid))
    context = {
        "service_name": service_name,
        "masters": masters,
        "dead_host_timeout": config_get("dead_host_timeout")
        }

    before = checksum(GMOND_CONF)
    with open(GMOND_CONF, "w") as gmond:
        gmond.write(render_template("gmond.conf", context))
    if before != checksum(GMOND_CONF):
        control(GMOND, RESTART)


#APACHE_CONFIG = "/etc/apache2/conf.d/ganglia.conf"
APACHE_CONFIG = "/etc/apache2/sites-available/ganglia.conf"
GANGLIA_APACHE_CONFIG = "/etc/ganglia-webfrontend/apache.conf"


def configure_apache():
    juju_log("INFO", "Configuring apache vhost for ganglia master")
    if not os.path.exists(APACHE_CONFIG):
        os.symlink(GANGLIA_APACHE_CONFIG, APACHE_CONFIG)
	command = [ 'a2ensite', os.path.basename(APACHE_CONFIG) ]
        code = subprocess.call(command)
        if code != 0:
            juju-log("ERROR", "Unable to configure apache2")
            exit(code)
    control(APACHE, RELOAD)


def expose_ganglia():
    expose(80)


def install_ganglia():
    install("ganglia-webfrontend", "gmetad")
    install("ganglia-monitor")


# Hook helpers for dict lookups for switching
def install_hook():
    configure_source()
    install_ganglia()
    configure_gmond()
    configure_gmetad()
    configure_apache()
    expose_ganglia()


def website_hook():
    relation_set(port=80)
    relation_set(hostname=unit_get("private-address"))


def upgrade_hook():
    configure_gmond()
    configure_gmetad()
    expose_ganglia()


def head_hook():
    relation_set(datasource="true")
    configure_gmond()

HOOK = os.path.basename(sys.argv[0])

hooks = {
    "install": install_hook,
    "master-relation-departed": configure_gmetad,
    "master-relation-broken": configure_gmetad,
    "master-relation-changed": configure_gmetad,
    "ganglia-node-relation-changed": configure_gmetad,
    "ganglia-node-relation-joined": configure_gmetad,
    "head-relation-joined": head_hook,
    "head-relation-departed": configure_gmond,
    "head-relation-broken": configure_gmond,
    "website-relation-joined": website_hook,
    "upgrade-charm": upgrade_hook
}

try:
    hooks[HOOK]()
except KeyError:
    juju_log("ERROR", "Unsupported hook execution %s" % HOOK)
