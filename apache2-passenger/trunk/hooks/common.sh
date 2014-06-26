#!/bin/bash

set -eu

sites_available_path='/etc/apache2/sites-available/'
sites_enabled_path='/etc/apache2/sites-enabled/'

exit_if_blank() {
  if [ -z "$1" ] ; then
      juju-log "$2 not set yet."
      exit 0
  fi
}

reload_configuration() {
  juju-log 'Reload Apache2 configuration'
  service apache2 reload
}

disable_site() {
  juju-log "Disable site: $1"
  a2dissite $1

  reload_configuration
}

enable_site() {
  juju-log "Enable site: $1"

  write_config "$sites_available_path/$1" "$2" "$3"

  a2ensite $1
  reload_configuration
}

write_config() {
  cat > $1 <<EOS
<VirtualHost *:$3>
  ServerSignature Off
  DocumentRoot $2/public
  <Directory $2/public>
    AllowOverride all
    Options -MultiViews
  </Directory>
</VirtualHost>
EOS
  [[ $3 == '80' ]] || echo -e "\nListen $3\n" >> $1
}

disabled() {
  [[ ! -f "$sites_enabled_path/$1" ]]
}

ensure_disabled() {
  disabled $1 || disable_site $1
}