# Overview

This charm deploys [MongoDB](http://mongodb.org) in three configurations:

- Single node
- Replica set
- Sharded clusters

# Usage

## Review the configurable options

The MongoDB charm allows for certain values to be configurable via a config.yaml file. The options provided are extensive, you should [review the options](https://jujucharms.com/fullscreen/search/precise/mongodb-20/?text=mongodb#bws-configuration). 

Specificlly the following options are important: 

- replicaset
   - ie: myreplicaset
   - Each replicaset has a unique name to distinguish it’s members from other replicasets available in the network.
   - The default value of myset should be fine for most single cluster scenarios.

- web_admin_ui
   - MongoDB comes with a basic but very informative web user interface that provides health
     and status information on the database node as well as the cluster.
   - The default value of yes will start the Admin web UI on port 28017.

- replicaset_master
   - If this node is going to be joining an existing replicaset, you can specify a member of that cluster
     ( preferably the master node ) so we can join the existing replicaset.
   - The value should be in the form of host[:port]
   - ie:  hostname ( will connect to hostname on the default port of 27017 )
   - ie:  hostname:port  ( will connect to hostname on port number <port> )

Most of the options in config.yaml have been modeled after the default configuration file for mongodb (normally in /etc/mongodb.conf) and should be familiar to most mongodb admins.  Each option in this charm have a brief description of what it does.

# Usage

## Single Node

Deploy the first MongoDB instance

    juju deploy mongodb
    juju expose mongodb

## Replica Sets

Deploy the first MongoDB instance

    juju deploy mongodb
    juju expose mongodb

Your deployment should look similar to this ( `juju status` ):

    environment: amazon
    machines:
      "0":
        agent-state: started
        agent-version: 1.16.5
        dns-name: ec2-184-73-7-172.compute-1.amazonaws.com
        instance-id: i-cb55cceb
        instance-state: running
        series: precise
        hardware: arch=amd64 cpu-cores=1 cpu-power=100 mem=1740M root-disk=8192M
      "1":
        agent-state: pending
        dns-name: ec2-54-196-181-161.compute-1.amazonaws.com
        instance-id: i-974bd2b7
        instance-state: pending
        series: precise
        hardware: arch=amd64 cpu-cores=1 cpu-power=100 mem=1740M root-disk=8192M
    services:
      mongodb:
        charm: cs:precise/mongodb-20
        exposed: false
        relations:
          replica-set:
          - mongodb
        units:
          mongodb/0:
            agent-state: pending
            machine: "1"
            public-address: ec2-54-196-181-161.compute-1.amazonaws.com


In addition, the MongoDB web interface should also be accessible via the services’
public-address and port 28017 ( ie: http://ec2-50-17-73-255.compute-1.amazonaws.com:28017 ).

### (Optional) Change the replicaset name

    juju set mongodb replicaset=<new_replicaset_name>

### Add one more nodes to your replicaset

    juju add-unit mongodb


### Add multiple nodes to your replicaset

    juju add-unit mongodb -n5


We now have a working MongoDB replica-set.

## Sharding (Scale Out Usage)

According the the MongoDB documentation found on [their website](http://docs.mongodb.org/manual/tutorial/deploy-shard-cluster/), one way of deploying a Shard Cluster is as follows:

- deploy config servers
- deploy a mongo shell (mongos)
- deploy shards
- connect the config servers to the mongo shell
- add the shards to the mongo shell

Using Juju we can deploy a sharded cluster using the following commands:

### Prepare a configuration file similar to the following:

    shard1:
      replicaset: shard1
    shard2:
      replicaset: shard2
    shard3:
      replicaset: shard3
    configsvr:
      replicaset: configsvr

We'll save this one as `~/mongodb-shard.yaml`.
  
### Bootstrap the environment
    juju bootstrap

### Config Servers ( we'll deploy 3 of them )
    juju deploy mongodb configsvr --config ~/mongodb-shard.yaml -n3

### Mongo Shell ( We just deploy one for now )
    juju deploy mongodb mongos

### Shards ( We'll deploy three replica-sets )
    juju deploy mongodb shard1 --config ~/mongodb-shard.yaml -n3
    juju deploy mongodb shard2 --config ~/mongodb-shard.yaml -n3
    juju deploy mongodb shard3 --config ~/mongodb-shard.yaml -n3

### Connect the Config Servers to the Mongo shell (mongos)

    juju add-relation mongos:mongos-cfg configsvr:configsvr

### Connect each Shard to the Mongo shell (mongos)

    juju add-relation mongos:mongos shard1:database
    juju add-relation mongos:mongos shard2:database
    juju add-relation mongos:mongos shard3:database

With the above commands, we should now have a three replica-set sharded cluster running.
Using the default configuration, here are some details of our sharded cluster:

- mongos is running on port 27021
- configsvr is running on port 27019
- the shards are running on the default mongodb port of 27017
- The web admin is turned on by default and accessible with your browser on port 28017 on each of the shards.

To verify that your sharded cluster is running, connect to the mongo shell and run `sh.status()`:

- `mongo --host <mongos_host>:<mongos_port>`
- `run sh.status()`
You should see your the hosts for your shards in the status output.

To deploy mongodb using permanent volume on Openstack, the permanent volume should be attached to the mongodb unit just after the deployment, then the configuration should be updated like follows.

### Use a permanent Openstack volume to store mongodb data.

    juju set mongodb volume-dev-regexp="/dev/vdc" volume-map='{"mongodb/0": "vol-id-00000000000000"}' volume-ephemeral-storage=false

### Backups

Backups can be enabled via config. Note that destroying the service cannot
currently remove the backup cron job so it will continue to run. There is a
setting for the number of backups to keep, however, to prevent from filling
disk space.

To fetch the backups scp the files down from the path in the config.

## Known Limitations and Issues

- If your master/slave/replicaset deployment is not updating correctly, check the log files at `/var/log/mongodb/mongodb.log` to see if there is an obvious reason ( port not open etc.).
- Ensure that TCP port 27017 is accessible from all of the nodes in the deployment.
- If you are trying to access your MongoDB instance from outside your deployment, ensure that the service has been exposed ( `juju expose mongodb` )
- Make sure that the mongod process is running ( ps -ef | grep mongo ).
- Try restarting the database ( restart mongodb )
- If all else fails, remove the data directory on the slave ( `rm -fr /var/log/mongodb/data/*` ) and restart the mongodb-slave daemon ( `restart mongodb` ).

# Contact Information

## MongoDB Contact Information

- [MongoDB website](http://mongodb.org) 
- [MongoDB documentation](http://www.mongodb.org/display/DOCS/Home)
- [MongoDB bug tracker](https://jira.mongodb.org/secure/Dashboard.jspa)
- [MongoDB user mailing list](https://groups.google.com/forum/#!forum/mongodb-user)
