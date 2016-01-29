Description
===========

#### Production - RCv3

This stack is intended for low to medium traffic production
websites and can be scaled as needed to accommodate future
growth.  This stack includes a Cloud Load Balancer, Cloud
Database, and a Master server (plus optional secondary
servers).  It also includes Cloud Monitoring and Cloud
Backups.

This stack is running the latest version of
[Drupal](https://www.drupal.org/),
[nginx](https://www.nginx.com/),
and [PHP FPM](http://php-fpm.org/).
with a Cloud Database running
[MySQL 5.6](http://www.mysql.com/about/).

This template will only function with RackConnect v3.


Instructions
===========

#### Getting Started
If you're new to Drupal, check out [Getting started with Drupal 7
administration](https://drupal.org/getting-started/7/admin). The getting
started document will help guide you through the initial steps of checking
your site's status, customizing your site's information, adding users, and
more!

After the stack has been created, you can find the admin username and
password listed in the "Credentials" section of Stack Details.

#### Accessing Your Deployment
If you provided a domain name that is associated with your Rackspace Cloud
account and chose to create DNS records, you should be able to navigate to
the provided domain name in your browser. If DNS has not been configured yet,
please refer to this
[documentation](http://www.rackspace.com/knowledge_center/article/how-do-i-modify-my-hosts-file)
on how to setup your hosts file to allow your browser to access your
deployment via domain name. Please note: some applications like WordPress,
Drupal, and Magento may not work properly unless accessed via domain name.
DNS should point to the IP address of the Load Balancer.

#### Migrating an Existing Site
Moving a Drupal site can be both difficult and time consuming. Drupal Modules
such as the [Backup and Migrate
module](http://drupal.org/project/backup_migrate) can help you move your
database content. We recommend backing everything up on both the source and
destination locations before anything is done. The content you want to move
over will be in the 'sites' directory. If you're running a single Drupal
site, you may just need the content of 'sites/default/files' along with your
database. Be careful not to overwrite the settings.php file within your site.
It contains the database configuration for your site.

This deployment has all of the core Drupal files in place, and their
permissions are properly set. Be careful with ownerhip and permissions as you
move things over. If you're unsure, check the original ownership and
permissions of the files in this deployment.

#### Modules
There are over 22,000 modules that have been created by an enaged developer
community. The [modules](https://drupal.org/project/Modules) section on
Drupal's website provides an easy way to search for and research modules.

#### Scaling out
This deployment is configured to be able to scale out easily.  However,
if you are expecting higher levels of traffic, please look into one of our
larger-scale stacks.

#### Details of Your Setup
This deployment was stood up using [Ansible](http://www.ansible.com/).
Once the stack has been deployed, Ansible will not run again unless you update the
stack. **Any changes made to the configuration may be overwritten when the stack
is updated.**

Drupal was installed using [Drush](http://www.drush.org/en/master/). Drupal
is installed into /var/www/vhosts/<YOUR DOMAIN>/ and served by
[nginx](https://www.nginx.com/).

Because this stack is intended for lower-traffic deployments, there is no
caching configured.

[Lsyncd](https://github.com/axkibe/lsyncd) has been installed in order to
sync static content from the Master server to all secondary servers.
When uploading content, it only needs to be uploaded to the Master node,
and will be automatically synchronized to all secondary nodes.

MySQL is being hosted on a Cloud Database instance, running MySQL 5.6.
Backups for MySQL are provided by [Holland](http://wiki.hollandbackup.org/),
which is running on the Master server.

Backups are configured using Cloud Backups.  The Master server is configured
to back up /var/spool/holland and /var/www once per week, and to retain
these backups for 30 days.

In order to restore the Database from backup, you will need to first restore
/var/spool/holland from the appropriate Cloud Backup.  After you have done so,
you will need to log into the Master server and restore the Holland backup
to the Cloud Database via the MySQL client.  For more assistance, please
contact your Support team.

Monitoring is configured to verify that Apache is running on both the Master
and all secondary servers, as well as that the Cloud Load Balancer is
functioning.  Additionally, the default CPU, RAM, and Filesystem checks
are in place on all servers.

#### Updating Drupal
Drupal does provide community documentation on [how to
upgrade](https://drupal.org/upgrade) your installation of Drupal. There are
several steps involved with the upgrade process. First, make sure to backup
your site files and your database prior to taking any steps to replace the
core site files. There are number of other tutorials available on places like
YouTube that can also step you though the upgrade/update process. There is
not currently a way to perform these upgrades automatically through the admin
interface.

#### Logging in via SSH
The private key provided in the passwords section can be used to login as
root via SSH. We have an article on how to use these keys with [Mac OS X and
Linux](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-linuxmac)
as well as [Windows using
PuTTY](http://www.rackspace.com/knowledge_center/article/logging-in-with-a-ssh-private-key-on-windows).

#### Additional Notes
You can add additional servers to this deployment by updating the
"server_count" parameter for this stack. This deployment is
intended for low to medium traffic production websites and can be
scaled as needed to accommodate future growth.

When scaling this deployment by adjusting the "server_count" parameter,
make sure that you DO NOT change the "database_flavor" and "database_disk"
parameters, as this will result in the loss of all data within the
database.

This stack will not ensure that Drupal or the servers themselves are
up-to-date.  You are responsible for ensuring that all software is
updated.


Requirements
============
* A Heat provider that supports the following:
  * OS::Heat::RandomString
  * OS::Heat::ResourceGroup
  * OS::Heat::SoftwareConfig
  * OS::Heat::SoftwareDeployment
  * OS::Nova::KeyPair
  * OS::Nova::Server
  * OS::Trove::Instance
  * Rackspace::Cloud::BackupConfig
  * Rackspace::CloudMonitoring::Check
  * Rackspace::RackConnect::PublicIP
* An OpenStack username, password, and tenant id.
* [python-heatclient](https://github.com/openstack/python-heatclient)
`>= v0.2.8`:

```bash
pip install python-heatclient
```

We recommend installing the client within a [Python virtual
environment](http://www.virtualenv.org/).

Parameters
==========
Parameters can be replaced with your own values when standing up a stack. Use
the `-P` flag to specify a custom parameter.

* `drupal_url`: Domain to use with Drupal Site (Default: example.com)
* `drupal_sitename`: Title to use for Drupal Site (Default: Example Site)
* `drupal_user`: Username for Drupal login (Default: admin)
* `drupal_email`: E-mail Address for Drupal Admin User (Default: admin@example.com)
* `rc_network_name`: Name or UUID of RackConnected network to attach this server to 
* `server_flavor`: Flavor of Cloud Server to use (Default: 4 GB General Purpose v1)
* `database_disk`: Size of the Cloud Database volume in GB (Default: 5)
* `database_flavor`: Flavor for the Cloud Database (Default: 1GB Instance)
* `server_count`: Number of secondary web nodes (Default: 0)
* `loadbalancer_flavor`: Flavor of Cloud Server to use for WordPress (Default: 2 GB General Purpose v1)

Outputs
=======
Once a stack comes online, use `heat output-list` to see all available outputs.
Use `heat output-show <OUTPUT NAME>` to get the value of a specific output.

* `drupal_login_user`: Drupal Admin User 
* `drupal_login_password`: Drupal Admin Password 
* `drupal_public_ip`: Load Balancer IP 
* `drupal_admin_url`: Drupal Admin URL 
* `drupal_public_url`: Drupal Public URL 
* `phpmyadmin_url`: PHPMyAdmin URL 
* `mysql_user`: Database User 
* `mysql_password`: Database Password 
* `ssh_private_key`: SSH Private Key 
* `server_ip`: Server Public IP 
* `secondary_ips`: Secondary Node IPs 

For multi-line values, the response will come in an escaped form. To get rid of
the escapes, use `echo -e '<STRING>' > file.txt`. For vim users, a substitution
can be done within a file using `%s/\\n/\r/g`.
