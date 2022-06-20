#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Jef Vantongerloo <jefvantongerloo@gmail.com>
#
# All rights reserved.
#
# License: CC BY-NC-ND 4.0
#          Attribution-NonCommercial-NoDerivatives 4.0 International
#
# You are free to:
#
# Share — copy and redistribute the material in any medium or format
#
# Under the following terms:
#
# Attribution   — You must give appropriate credit, provide a link to the
#                 license, and indicate if changes were made. You may do so in
#                 any reasonable manner, but not in any way that suggests the
#                 licensor endorses you or your use.
# NonCommercial — You may not use the material for commercial purposes.
# NoDerivatives — If you remix, transform, or build upon the material, you may
#                 not distribute the modified material.
# No additional restrictions — You may not apply legal terms or technological
#                              measures that legally restrict others from doing
#                              anything the license permits.

DOCUMENTATION = """
---
module: jefvantongerloo.aos.device_info
short_description: return device information
description:
    - Connect to an Alcatel-Lucent Enterprise Omniswitch device and return a device information dictionary.
version_added: '0.1.0'
author: Jef Vantongerloo (@jefvantongerloo)
options: {}
notes:
    - 'Tested against: aos8 8.7.354.R01'
    - This module works with connection C(network_cli)
requirements:
    - 'textfsm-aos >= 1.0.0'
"""

EXAMPLES = """
  - name: Get device info
    jefvantongerloo.aos.device_info:
    register: device_info
"""

RETURN = """
output:
  description: device information gathered
  returned: success
  type: dict
  sample:
    "network_os": "aos8"
    "network_os_hostname": "net-ant-swi-001"
    "network_os_model": "OS6860E-U28"
    "network_os_platform": "Alcatel-Lucent Enterprise"
    "network_os_version": "8.6.289.R01 GA"
"""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection


def main():
    argument_spec = dict()
    module = AnsibleModule(argument_spec=argument_spec)
    connection = Connection(module._socket_path)

    result = {"changed": False, "output": connection.get_device_info()}

    module.exit_json(**result)


if __name__ == "__main__":
    main()
