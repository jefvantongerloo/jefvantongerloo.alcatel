# Ansible Collection - jefvantongerloo.alcatel

Ansible collection to support Alcatel-Lucent Enterprise OmniSwitch aos devices (aos6 &amp; aos8)

## Supported connections

The Alcatel collection supports network_cli connections.

## Cliconf Plugins

| Network OS                | Description                                                               |
|---------------------------|---------------------------------------------------------------------------|
| jefvantongerloo.alcatel.aos   | Use aos cliconf to run command on ALE aos platform                        |

## Action Plugins

| Name                           | Description                                                          |
|--------------------------------|----------------------------------------------------------------------|
| ansible.netcommon.cli_command  | Run a cli command on aos device                                      |
| ansible.netcommon.cli_config   | Push text based configuration to aos over network_cli                |
| ansible.netcommon.net_get      | Copy a file from the aos device to Ansible Controller                |
| ansible.netcommon.net_put      | Copy a file from Ansible Controller to the aos device                |

## Modules

| Name                              | Description                                                       |
|-----------------------------------|-------------------------------------------------------------------|
|  jefvantongerloo.alcatel.device_info  | Get ALE Omniswitch device information dictionary                  |

## Installation

Collection distribution is via[Ansible-Galaxy](https://galaxy.ansible.com/jefvantongerloo/alcatel)

Install the Python [Textfsm-aos](https://github.com/jefvantongerloo/textfsm-aos) and [Ansible-pylibssh](https://github.com/ansible/pylibssh) packages:

```bash
pip install -r requirements.txt
```

You can install the `jefvantongerloo.alcatel` collection with the Ansible Galaxy CLI:

```bash
ansible-galaxy collection install jefvantongerloo.alcatel
```

You can also include it in the `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: jefvantongerloo.alcatel
```

## Usage

To use this collection make sure to set required inventory host parameters, for example:

```yaml
---
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: jefvantongerloo.alcatel.aos
ansible_user: admin
ansible_password: switch
```

## Example playbooks

### Device_info

```yaml
---
- name: test device_info module
  connection: network_cli
  hosts: all
  gather_facts: no

  tasks:
    - name: device_info test
        jefvantongerloo.alcatel.device_info:
        register: device_info

    - name: debug device_info
        debug:
        msg: "{{ device_info }}"
```

### Cli_command

```yaml
---
- name: cli_command
  connection: network_cli
  hosts: all
  gather_facts: no

  tasks:
    - name: cli_command test
      cli_command:
        command: show chassis
      register: chassis

    - name: debug cli_command output
        debug:
        msg: "{{ chassis }}"
```

### Cli_config backup

```yaml
---
- name: cli_config backup
  connection: network_cli
  hosts: all
  gather_facts: no

  tasks:
    - name: cli_config backup test
      cli_config:
        backup: yes
        backup_options:
          dir_path: tmp
      register: backup_running

    - name: debug backup_running
        debug:
        msg: "{{ backup_running }}"
```

### Net_get

```yaml
---
- name: Copy file from aos device
  connection: network_cli
  hosts: all
  gather_facts: no
  tasks:
    - name: net_get test
      ansible.netcommon.net_get:
        src: /flash/working/vcboot.cfg
        dest: tmp/vcboot.cfg
        protocol: sftp
```

### Net_put

```yaml
---
- name: Copy file to aos device
  connection: network_cli
  hosts: all
  gather_facts: no
  tasks:
    - name: net_put test
      net_put:
        src: tmp/vcboot.cfg
        dest: /flash/vcboot.cfg
        protocol: sftp
```
