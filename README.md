# Django Boilerplate

# How to start with vagrant:

## What's inside?
 * [Django](https://github.com/django/django)
 * [Django REST framework](https://github.com/tomchristie/django-rest-framework)
 * [Django Channels](https://channels.readthedocs.io/en/latest/) - is a project that takes Django and extends its abilities beyond HTTP - to handle WebSockets, chat protocols, IoT protocols, and more.
 * [Celery](http://www.celeryproject.org) - is an asynchronous task queue/job queue based on distributed message passing.
 * [Flower](http://flower.readthedocs.io/en/latest/) - is a web based tool for monitoring and administrating [Celery](http://www.celeryproject.org) clusters.
 * [PostgreSQL](https://github.com/postgres/postgres)
 * [Redis](https://redis.io) - in-memory data structure store, used as a database, cache and message broker.
 * [Gunicorn](https://github.com/benoitc/gunicorn) - WSGI HTTP Server
 * [Daphne](https://github.com/django/daphne/) - is a HTTP, HTTP2 and WebSocket protocol server for ASGI and ASGI-HTTP
 * [Nginx](https://nginx.org/)
 * [Supervisor](https://github.com/Supervisor/supervisor) - client/server process management system
 * Config samples for each tool from above
 * and more...

## Instruction:
 1. Copy repository `repository`
 2. Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads) if not installed.
 3. Install [Vagrant](https://www.vagrantup.com/downloads.html) if not installed.
 4. Install  [Ansible](http://docs.ansible.com/ansible/intro_installation.html) if not installed.  (Version 2.4+)
 5. Run `sudo ansible-galaxy install -r ./ansible/requirements.yml --force -p ./ansible/galaxy_roles` from root project directory for installing Ansible role dependencies.
 6. Run `sudo -- sh -c "echo '192.168.12.32 webapp.local api.webapp.local flower.webapp.local' >> /etc/hosts"` for simple accessing to Vagrant machine in your browser.
 7. Run `vagrant up` from root project directory for start the Vagrant machine. At first time machine will be automatically provisioned.

> `vagrant provision` this command is a great way to quickly to run provisioning new changes on virtual machine.

### Configure PyCharm (if you are using it):
- Configuring Python interpreter: File > Settings > Project Interpreter > Add Remote > Vagrant > Python interpreter path: `/home/ubuntu/webapp/venv/bin/python` > OK
- Configuring Django support: File > Settings > Languages & Frameworks > Django > Enable Django support; Django project root: `{project_dir}`; Settings: `src/django_project/local_settings.py`
- Configuring Django run/debug configurations: Run > Edit configurations? > Add new configuration > Django server > Name: Django Development Server; Host: 0.0.0.0; Port: 8000; Run browser: http://api.webapp.local:8000/; Path mapping: `Local path - path to project on host system : Remote path - path to project on vagrant machine`
- Configuring database: Database > Add > Data Source > PostgreSQL > Download Driver > Host: `localhost`; Port: `5433`; Database: `django_app`; User: `django_app`; Password: `{password} (by default: qwe123)` > Configure SSH > Check use SSH tunnel; Proxy host: `127.0.0.1`; Port: `2222`; Proxy user: `ubuntu`; Auth type: Key pair; Private key file: `./.vagrant/machines/default/virtualbox/private_key` > OK > Test Connection > OK

***
# Server structure

## Endpoints

Endpoints

                http://{server_name}.local (home page) - e.g. webapp
                http://api.{server_name}.local/ws/   (Websocket connections)
                http://api.{server_name}.local/api/   (REST API)
                http://api.{server_name}.local/admin/   (Django Admin Interface)
                

## Nginx configurations
Domain is located in `./ansible/group_vars/project.yml`|`./ansible/host_vars/staging/vars.yaml`|`./ansible/host_vars/production/vars.yaml` files and used by NGINX (`./ansible/group_vars/nginx.yaml`).
Default structure of domains:
 -  {site_domain} - by default `webapp.local`. A main domain which uses for React/Angular/Vue application.
 -  {api_domain} - by default `api.{site_domain}.local`. A sub-domain which uses for Django application.
 -  {flower_domain} - by default `flower.{site_domain}.local`. sub-domain for [Flower](http://flower.readthedocs.io/en/latest/) (tool for monitoring and management of [Celery](http://www.celeryproject.org))


## Directory structure
The directory structure of the project in the virtual machine.

 *  `/home/{deploy user}/{project name}/` - Main director.
 *  `/home/{deploy user}/{project name}/etc/` - Directory contains configuration files.
 *  `/home/{deploy user}/{project name}/log/` - Directory contains logs.
 *  `/home/{deploy user}/{project name}/run/` - Directory contains unix sockets and pid files.
 *  `/home/{deploy user}/{project name}/src/` - Directory contains source code of project.
 *  `/home/{deploy user}/{project name}/bin/` - Directory contains scripts.
 *  `/home/{deploy user}/{project name}/venv/` - Directory contains virtualenv.

## Manage services
>   `./ansible/group_vars/` directory contains files with variables for configuration files of Supervisor and Systemd.

## List services
 List installed services.

> Names of services could be changed in `./ansible/group_vars/`

 -  Nginx - `sudo service nginx start|stop|restart|reload|force-reload|status`
 -  Postgresql - `sudo service postgresql start|stop|restart|reload|force-reload|status`
 -  Redis - `sudo service redis_6379 start|stop|restart|reload|force-reload|status`
 -  Celery worker - `sudo service {project_name}-worker start|stop|restart|reload|force-reload|status`
 -  Celery beat - `sudo service {project_name}-beat start|stop|restart|reload|force-reload|status`
 -  Gunicorn (WSGI HTTP Server) for Django - `sudo supervisorctl {actions: start|restart|stop|status|...} {gunicorn_supervisor_name|default({project_name}-gunicorn)}`
 -  Daphne (ASGI Server) for Django - `sudo supervisorctl {actions: start|restart|stop|status|...} {gunicorn_supervisor_name|default({project_name}-channels)}`
 -  Flower (Monitoring&Management of Celery) for Django - `sudo supervisorctl {actions: start|restart|stop|status|...} {flower_supervisor_name|default({project_name}-flower)}`

## Django settings file
Ansible creates local_settings.py file (by template (`./ansible/roles/webtier/templates/local_settings.py`) and variables in `./ansible/group_vars/` and `./ansible/host_vars/`) which contains configs to services and libraries (DB/Redis/python libraries and etc) according to environment (vagrant/develop/staging/production - values are defined in `./ansible/host_vars/vagrant|develop|stating|production`).
 The local_settings.py is generated every time after deploying with Ansible and is in the root directory of Django code at the same level as `manage.py` file.

***
# Useful commands

## Deploy.sh script

### How to deploy the project to a local Vagrant
 - `./deploy vagrant` (both backend and frontend)
 - `./deploy vagrant frontend`
 - `./deploy vagrant backend`

### How to deploy the project to remote server(s)
 1. Edit respective files in a `host_vars` directory, as well as inventory files. This repo includes default configuration samples for production and staging environments.
 2. Execute `./deploy <inventory name> <tags>` command in the project's root directory, where <inventory name> is the name of your inventory (e.g. "staging" or "production"), and <tags> are optional tags that will execute only the tasks that were marked by this tag (e.g. "provision" tag, which will skip installing most part of the setup and only update the code from a repo and restart services).
 3. Give password to decrypt necessary vault data.
 3. Enjoy deployment :)

## Ansible
 - `bin/ansible-playbook -i ./ansible/{environment}.ini ./ansible/site.yml` - Deploy to {environment} servers.

## Restart Django & React/Angular/Vue applications on external/local machines.
### Restart Django app by supervisorctl command
    sudo supervisorctl start/restart/stop {project_name}-gunicorn
> {project_name} - By default is 'webapp'

### Restart React/Angular app by supervisorctl command
    sudo supervisorctl start/restart/stop {project_name}-webapp
> {project_name} - By default is 'webapp'

## Vagrant
 - `vagrant up` - Start the virtual machine.
 - `vagrant halt` - Shutdown the virtual machine.
 - `vagrant destroy` - Destroy the virtual machine.
 - `vagrant provision` - Triggers provisioning on a running virtual machine.
 - `vagrant ssh` - Create an ssh connection with the virtual machine.
 - `vagrant reload` - Restarts vagrant machine, loads new Vagrantfile configuration.
 - `vagrant status` - Outputs status of the vagrant machine.
 - `vagrant suspend` - Suspends the machine.
 - `vagrant resume` - Resume a suspended vagrant machine.
 - `vagrant share` - Share your Vagrant environment with anyone in the world.
 
# How to quickly deploy:

## Tools:
- [Ansible](http://docs.ansible.com/ansible/intro_installation.html) (Version 2.4+).

## How it works
1. Ansible uses values (e.g. name or version of a package) from files in group_vars and host_vars folders for executing commands on the remote server to install stuff and configure the server.
2. group_vars folder contains "default" values (e.g. site_domain by default is webapp.local) and configurations. host_vars folder contains overridden values for specific servers (e.g. production should use webapp.com for variable site_domain)
3. Inventory files (vagrant.ini/staging.ini/production.ini) in ansible folder contain variables (server domain, user name and password or ssh key) for auth to a server.

## How run deploy
1. Install [Ansible](http://docs.ansible.com/ansible/intro_installation.html)
2. Install ansible roles by next command `sudo ansible-galaxy install -r ./ansible/requirements.yml --force -p ./ansible/galaxy_roles` from root project directory (on the same level with VagrantFile and Deploy script) for installing Ansible role dependencies.
3. Push last changes of the code to the repo.
4. Run next command to start deploying process `./deploy {name of inventory ini file}` from root project directory - example: [`./deploy production`](###How to deploy the project to remote server(s)). (Ansible will execute git pull on the remote server and restart services)
5. After start deploy process ansible will prompt password input in console for Ansible Vault. Enter the password (default the password is `Ulumulu88`).
6. Done.

> _Notice!_ In this project is used Ansible Vault!
Files `./ansible/host_vars/production/vault.yml` and `./ansible/host_vars/production/vault.yml` are encrypted by default (Default password is `Ulumulu88`).
They're used to store sensitive data as db names, passwords, keys, secrets etc.
Before deploying to public servers as production or staging you must:

 1. Decrypt necessary files by command `ansible-vault decrypt ./ansible/host_vars/production/vault.yml --ask-vault-pass` (run it from ansible directory) using default password.
 2. Edit configuration in those files as needed.
    Also if it's first edition of those files you _SHOULD_ edit:
     - database name, user and password;
     - django secret key (http://www.miniwebtool.com/django-secret-key-generator/);
    For passwords better to use generated (http://passwordsgenerator.net/).
 3. Encrypt files again with your _NEW AND SECURE_ password using command `./ansible-vault encrypt ansible/host_vars/production/vault.yml --ask-vault-pass`.


## Examples:
### How to change domain name:
Domain name uses for generating nginx configs files. In `./ansible/group_vars/all/project.yml` file is a section of domains (site_domain - for react app, api_domain - for django, flowe_domain - for flower tool) are default domains (which use for local development).

1. Copy and past those variables to e.g. `./ansible/host_vars/production/vars.yml` and update values.
2. Run deploy [(e.g. `./deploy production`)](###How to deploy the project to remote server(s))
