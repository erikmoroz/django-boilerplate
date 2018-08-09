erik-moroz.Supervisor
=================

[![Build Status](https://travis-ci.org/erik-moroz/Supervisor.svg)](https://travis-ci.org/erik-moroz/Supervisor)
[![Galaxy](http://img.shields.io/badge/erik-moroz.Supervisor-blue.svg?style=flat-square)](https://galaxy.sudo.com/list#/roles/885)
[![Tag](http://img.shields.io/github/tag/erik-moroz/erik-moroz.Supervisor.svg?style=flat-square)]()

Ansible role which manage [supervisor](http://supervisord.org)

* Install and manage [supervisor](http://supervisord.org)
* Manage supervisor tasks
* Provide handlers for reload and restart supervisor

#### Variables

The role variables and default values.

```yaml
---
supervisor_enabled: yes                                       # The role is enabled
supervisor_version: latest                                    # [default: latest]: Supervisor version to install (e.g. latest, 3.3.1)
supervisor_system_user: root                                  # [default: root]: Name of the user that should own the config file/directory
supervisor_system_group: root                                 # [default: root]: Name of the group that should own the config file/directory
supervisor_bindir: '/usr/local/bin'
supervisor_unix_http_server_file: '/var/run/supervisor.sock'  # [default: /var/run/supervisor.sock]: A path to a UNIX domain socket (e.g. /tmp/supervisord.sock) on which supervisor will listen for HTTP/XML-RPC requests. supervisorctl uses XML-RPC to communicate with supervisord over this port
supervisor_pid: '/var/run/supervisord.pid'                    # [default: /var/run/supervisord.pid]: The location in which supervisord keeps its pid file
supervisor_logdir: '/var/log/supervisor'                      # [default: /var/log/supervisor/supervisord.log]: The path to the activity log of the supervisord process
supervisor_restart_sec: 5
supervisor_cfgdir: '/etc/supervisor'                          # path to config directory
supervisor_conf_file: '{{ supervisor_cfgdir }}/supervisord.conf'
supervisor_incdir: '{{supervisor_cfgdir}}/conf.d'             # path to include directory
supervisor_programs: {}                                       # List of supervisor programs
                                                              # Ex. supervisor_tasks:
                                                              #       - django_application:
                                                              #         name: "project-django"
                                                              #         command: "/usr/bin/python ./manage.py runserver"
                                                              #         option: value
                                                              #         option: value
supervisor_groups: {}                                         # groups of tasks

```

#### Usage

Add `erik-moroz.Supervisor` to your roles and set vars in your playbook file.

Example:

```yaml

- hosts: all

  roles:
    - Stouts.supervisor

  vars:
    supervisor_tasks:
        - google_ping:
            name: ping
            command: ping google.com
            autostart: true
            autorestart: true
    supervisor_groups:
        - stuff:
            name: my_group
            programs: ping
```

#### License

Licensed under the MIT License. See the LICENSE file for details.

#### Feedback, bug-reports, requests, ...

Are [welcome](https://github.com/erik-moroz/Supervisor/issues)!
