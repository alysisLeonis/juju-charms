## Overview

Nginx with [Phusion Passenger](https://www.phusionpassenger.com/) module [Juju Charm](http://jujucharms.com/). Provides a container for subordinate [Rack Charm](https://code.launchpad.net/~pavel-pachkovskij/charms/precise/rack/trunk).

## Usage

1. Deploy Nginx with Passenger module.

        juju deploy nginx-passenger

2. Deploy Rack application and all dependent services ([see how](https://code.launchpad.net/~pavel-pachkovskij/charms/precise/rack/trunk)).

        juju deploy rack --config myapp.yml

3. Relate them

        juju add-relation rack nginx-passenger

4. Open the stack up to the outside world.

        juju expose nginx-passenger

5. Find the nginx-passenger instance's public URL from

        juju status

## Scaling

It's possible to use this service with load balancer. Here is an example

1. Run steps 1-3 from **Usage** section

2. Deploy load balancer, e.g. haproxy

        juju deploy haproxy

3. Relate it to the stack

        juju add-relation haproxy nginx-passenger

4. Scale up the stack

        juju add-unit -n3 nginx-passenger

5. Expose load balancer up to the outside world.

        juju expose haproxy

## Under the hood

This Charm
- installs Nginx, Phusion Passenger and Ruby from  from [Brightbox Launchpad package repository](https://launchpad.net/~brightbox/+archive/ruby-ng).
- installs all dependencies
- configures Nginx to run Rack application

## TODO
- Add Python (WSGI) apps support.