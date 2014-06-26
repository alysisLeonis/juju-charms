## Overview

Apache2 with module Passenger [Juju Charm](http://jujucharms.com/). Provides a container for subordinate [Rack Charm](http://jujucharms.com/charms/precise/rack).

## Usage

1. Deploy Apache2 with Passenger module.

        juju deploy apache2-passenger

2. Deploy Rack application and all dependent services ([see how](http://example.com)).

        juju deploy rack --config myapp.yml

3. Relate them

        juju add-relation rack apache2-passenger

4. Open the stack up to the outside world.

        juju expose apache2-passenger

5. Find the apache2-passenger instance's public URL from

        juju status

## Scaling

It's possible to use this service with load balancer. Here is an example

1. Run steps 1-3 from **Usage** section

2. Deploy load balancer, e.g. haproxy

        juju deploy haproxy

3. Relate it to the stack

        juju add-relation haproxy apache2-passenger

4. Scale up the stack

        juju add-unit -n3 apache2-passenger

5. Expose load balancer up to the outside world.

        juju expose haproxy

## Under the hood

- installs Apache2 and all dependencies
- installs Ruby 1.9.3, Phusion Passenger, apache2-mod-passenger from [Brightbox Launchpad package repository](https://launchpad.net/~brightbox/+archive/ruby-ng).
- configures Apache2 to run Rack applications
