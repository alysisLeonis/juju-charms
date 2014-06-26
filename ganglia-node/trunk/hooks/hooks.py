#!/usr/bin/python

import subprocess
import os
import sys
import hashlib
from utils import (
    juju_log,
    relation_get,
    relation_set,
    relation_ids,
    relation_list,
    render_template,
    install,
    configure_source,
    )


def checksum(sfile):
    sha256 = hashlib.sha256()  # IGNORE:E1101
    with open(sfile, 'r') as source:
        sha256.update(source.read())
    return sha256.hexdigest()

# Services
GMOND = "ganglia-monitor"

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

GMOND_CONF = "/etc/ganglia/gmond.conf"


def configure_gmond():
    juju_log("INFO", "Configuring new ganglia node")
    _rid = relation_ids("juju-info")[0]
    principle_unit = get_principle_name()
    service_name = principle_unit.split('/')[0]
    _rids = relation_ids("node")
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
        "unit_name": principle_unit
        }

    before = checksum(GMOND_CONF)
    with open(GMOND_CONF, "w") as gmond:
        gmond.write(render_template("gmond.conf", context))

    if len(masters) > 0:
        if before != checksum(GMOND_CONF):
            control(GMOND, RESTART)
    else:
        control(GMOND, STOP)

# Workaround as unable to query locally scoped
# juju relationship for principle service name
PRINCIPLE = "/etc/juju_principle_name"


def store_principle_name():
    ## Store principle unit name for use later
    unit_name = os.environ['JUJU_REMOTE_UNIT']
    with open(PRINCIPLE, "w") as principle:
        principle.write(unit_name)


def get_principle_name():
    principle_name = "unknown"
    if os.path.exists(PRINCIPLE):
        with open(PRINCIPLE, "r") as principle:
            principle_name = principle.read().strip()
    return principle_name


def install_node():
    install("ganglia-monitor")


# Hook helpers for dict switching
def install_hook():
    configure_source()
    install_node()


def node_joined_hook():
    relation_set(service=get_principle_name().split('/')[0])

HOOK = os.path.basename(sys.argv[0])

hooks = {
    "install": install_hook,
    "node-relation-changed": configure_gmond,
    "node-relation-departed": configure_gmond,
    "node-relation-broken": configure_gmond,
    "upgrade-charm": configure_gmond,
    "node-relation-joined": node_joined_hook,
    "juju-info-relation-joined": store_principle_name
}

try:
    hooks[HOOK]()
except KeyError:
    juju_log("ERROR", "Unsupported hook execution {}".format(HOOK))
