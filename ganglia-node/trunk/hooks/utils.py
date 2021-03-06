
#
# Copyright 2012 Canonical Ltd.
#
# Authors:
#  James Page <james.page@canonical.com>
#
#

import subprocess
import socket


def install(*pkgs):
    cmd = [
        'apt-get',
        '-y',
        'install'
          ]
    for pkg in pkgs:
        cmd.append(pkg)
    subprocess.check_call(cmd)

TEMPLATES_DIR = 'templates'

try:
    import jinja2
except ImportError:
    install('python-jinja2')
    import jinja2


def render_template(template_name, context, template_dir=TEMPLATES_DIR):
    templates = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(template_dir)
                    )
    template = templates.get_template(template_name)
    return template.render(context)


def configure_source():
    source = config_get('source')
    if (source.startswith('ppa:') or
        source.startswith('cloud:') or
        source.startswith('http:')):
        cmd = [
            'add-apt-repository',
            source
            ]
        subprocess.check_call(cmd)
    if source.startswith('http:'):
        key = config_get('key')
        cmd = [
            'apt-key',
            'import',
            key
            ]
        subprocess.check_call(cmd)
    cmd = [
        'apt-get',
        'update'
        ]
    subprocess.check_call(cmd)

# Protocols
TCP = 'TCP'
UDP = 'UDP'


def expose(port, protocol='TCP'):
    cmd = [
        'open-port',
        '{}/{}'.format(port, protocol)
        ]
    subprocess.check_call(cmd)


def juju_log(severity, message):
    cmd = [
        'juju-log',
        '--log-level', severity,
        message
        ]
    subprocess.check_call(cmd)


def relation_ids(relation):
    cmd = [
        'relation-ids',
        relation
        ]
    return subprocess.check_output(cmd).split()  # IGNORE:E1103


def relation_list(rid):
    cmd = [
        'relation-list',
        '-r', rid,
        ]
    return subprocess.check_output(cmd).split()  # IGNORE:E1103


def relation_get(attribute, unit=None, rid=None):
    cmd = [
        'relation-get',
        ]
    if rid:
        cmd.append('-r')
        cmd.append(rid)
    cmd.append(attribute)
    if unit:
        cmd.append(unit)
    return subprocess.check_output(cmd).strip()  # IGNORE:E1103


def relation_set(**kwargs):
    cmd = [
        'relation-set'
        ]
    for k, v in kwargs.items():
        cmd.append('{}={}'.format(k, v))
    subprocess.check_call(cmd)


def unit_get(attribute):
    cmd = [
        'unit-get',
        attribute
        ]
    return subprocess.check_output(cmd).strip()  # IGNORE:E1103


def config_get(attribute):
    cmd = [
        'config-get',
        attribute
        ]
    return subprocess.check_output(cmd).strip()  # IGNORE:E1103


def get_unit_hostname():
    return socket.gethostname()


def get_host_ip(hostname=unit_get('private-address')):
    cmd = [
        'dig',
        '+short',
        hostname
        ]
    return subprocess.check_output(cmd).strip()  # IGNORE:E1103
