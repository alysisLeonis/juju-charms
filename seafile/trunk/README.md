# Overview

This charm provides Seafile server, an online file storage and collaboration
tool. Seafile enables you to build a private cloud for file sharing and
collaboration among team members in your company/organization. 

First, you create a file library on the web and upload files to it. Then you
share it into a team or with another user.

File libraries can also be synchronized among computers and mobile devices. You
download a library to your PC. Whenever you add, delete or edit a file, the
latest version will be uploaded to the server automatically and will then be
synchronized to everyone's computer.

This charm provides the Seafile server as well as Seahub, the web interface for
Seafile.

# Usage

In order to deploy this charm, you will need to have a configuration file ready
for it. You can learn how to make it in the next section.

First, bootstrap your environment:

    juju bootstrap

Then, deploy the service. Assuming the configuration file is called
`seafile.yaml` and is on the same folder as your shell, execute:

    juju deploy seafile --config seafile.yaml

Finally, expose the service:

    juju expose seafile

# Configuration

There are several configuration options for this charm. In case you want to do
a basic deploy of the charm, the required options are the following:

 * `domain`: This is the domain or public IP address where Seahub will be
hosted at. If you don't know what it is until deployment, you can use
`localhost` in the meanwhile, but make sure to change it as soon as you have the
domain or uploads will fail.
 * `server_name`: This server name will be seen by your seafile users. The name
should be between 3 and 15 characters long. It can be anything you would like,
so let your creativity fly.
 * `seahub_admin_email`: This is the email address for the main administrator
account. It will be used for your login.
 * `seahub_admin_passwd`: This is the password for the main administrator
account. It will also be used for your login, along with the email in the
previous field.

If you want to customize your install a bit more, you can set the following
configuration options:

 * `ccnet_server_port`: The port to be used for the ccnet server.
 * `seafile_server_port`: The port to be used for the Seafile server.
 * `http_server_port`: The port to be used for the http Seafile server. Please,
note that this is not the web interface (Seahub) port.
 * `seahub_port`: The port to be used for Seahub, Seafile's web interface.

If you want to modify any of the options after deployment, you can use:

    juju set seafile [option]=[value]

## Creating your own configuration file

Here, you have a sample configuration file. In order to use it, just copy it,
fill in the blanks and save it.

    seafile:
      domain: [domain]
      server_name: [server_name]
      seahub_admin_email: [seahub_admin_email]
      seahub_admin_passwd: [seahub_admin_passwd]

If you would like, you can add the other configuration options to your file.

# Contact Information

Authors: Juan L. Negron <juan@ubuntu.com>, José Antonio Rey <jose@ubuntu.com>  
Report bugs at: http://bugs.launchpad.net/charms  
Location: http://jujucharms.com   

## Seafile

- [Seafile website](http://seafile.com)
