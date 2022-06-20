# Ansible Collection - jefvantongerloo.aos

Ansible collection to support Alcatel-Lucent Enterprise OmniSwitch devices (aos6 &amp; aos8)

## Plugins

| Network OS                | Description                                                               |
|---------------------------|---------------------------------------------------------------------------|
|  jefvantongerloo.aos.aos  | Use aos cliconf to run command on ALE aos platform  |

## Modules

| Name                              | Description                                                               |
|-----------------------------------|---------------------------------------------------------------------------|
|  jefvantongerloo.aos.device_info  | Get ALE Omniswitch device information dictionary                          |

## Installation

Collection distribution is via Ansible-Galaxy

<!-- Install the Ansible [netcommon](https://galaxy.ansible.com/ansible/netcommon) collection:

```bash
ansible-galaxy collection install ansible.netcommon
``` -->

Install the Python [Textfsm-aos](https://github.com/jefvantongerloo/textfsm-aos) and [Ansible-pylibssh](https://github.com/ansible/pylibssh) packages:
```bash
pip install -r requirements.txt
```

To install the `jefvantongerloo.aos.aos` collection, use the following Ansible Galaxy CLI command:
```bash
ansible-galaxy collection install jefvantongerloo.aos
```

You can also include it in the `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: jefvantongerloo.aos.aos
```

## Usage
To use this collection make sure to set required inventory host parameters, for example:
```yaml
---
ansible_connection: ansible.netcommon.network_cli
ansible_network_os: jefvantongerloo.aos.aos
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
        jefvantongerloo.aos.device_info:
        register: device_info

    - name: debug device_info
        debug:
        msg: "{{ device_info }}"
```

### Cli_command

```yaml
---
- name: test cli_command module
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
- name: test device_info module
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
