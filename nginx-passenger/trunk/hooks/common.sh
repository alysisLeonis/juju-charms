#!/bin/bash

set -eu

sites_enabled_path='/etc/nginx/sites-enabled'

exit_if_blank() {
  if [ -z "$1" ] ; then
      juju-log "$2 not set yet."
      exit 0
  fi
}

reload_configuration() {
  juju-log 'Reload Nginx configuration'
  service nginx reload
}

disable_site() {
  juju-log "Disable site: $1"
  rm -rf "$sites_enabled_path/$1"

  reload_configuration
}

enable_site() {
  juju-log "Enable site: $1"

  write_config "$sites_enabled_path/$1" "$2" "$3"
  reload_configuration
}

write_config() {
  cat > $1 <<EOS
server {
    server_name localhost;
    listen $3;
    root $2/public;
    passenger_enabled on;
}
EOS
}

disabled() {
  [[ ! -f "$sites_enabled_path/$1" ]]
}

ensure_disabled() {
  disabled $1 || disable_site $1
}