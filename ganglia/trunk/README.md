# Overview

> Ganglia is a scalable distributed monitoring system for high-performance computing
 systems such as clusters and Grids. It is based on a hierarchical design targeted
 at federations of clusters. It leverages widely used technologies such as XML for
 data representation, XDR for compact, portable data transport, and RRDtool for data
 storage and visualization. It uses carefully engineered data structures and
 algorithms to achieve very low per-node overheads and high concurrency. The
 implementation is robust, has been ported to an extensive set of operating systems
 and processor architectures, and is currently in use on thousands of clusters around
 the world. It has been used to link clusters across university campuses and around
 the world and can scale to handle clusters with 2000 nodes.

In short - it monitors stuff and scales really well.

# Usage

This charm and is subordinate peer - ganglia-node - support using ganglia in a
couple of different ways.

## Small


For small deployments, use of a single 'master' head server may be sufficient:

    juju deploy ganglia
    juju deploy ganglia-node
    juju add-relation ganglia:node ganglia-node:node
    juju deploy mysql
    juju deploy memcached
    ...
    juju add-relation ganglia-node mysql
    juju add-relation ganglia-node memcached
    juju expose ganglia

Ganglia will start reporting metrics about deployed services::

    http://<IP of ganglia service unit>/ganglia

## Large

For larger deployments which require more scalability, its possible to leverage
the hierarchical nature of ganglia to build up resilience and better scale:
    
    juju deploy ganglia
    juju deploy ganglia mysql-ganglia-cluster
    juju deploy ganglia memcached-ganglia-cluster
    juju deploy ganglia-node ganglia-node-mysql
    juju deploy ganglia-node ganglia-node-memcached
    juju add-relation ganglia:master mysql-ganglia-cluster:head
    juju add-relation ganglia:master memcached-ganglia-cluster:head
    juju add-relation mysql-ganglia-cluster:node ganglia-node-mysql:node
    juju add-relation memcached-ganglia-cluster:node ganglia-node-memcached:node
    juju deploy mysql
    juju deploy -n XX memcached
    juju add-relation ganglia-node-mysql mysql
    juju add-relation ganglia-node-memcached memcached
    juju expose ganglia

The XX-ganglia-cluster service units will receive data from all services associated
with ganglia-node deployments, leaving the main ganglia service to cope with the web
interface and report generation.
