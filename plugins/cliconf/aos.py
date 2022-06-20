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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
author: Jef Vantongerloo (@jefvantongerloo)
cliconf: jefvantongerloo.aos.aos
short_description: Cliconf plugin to configure and run CLI commands on Alcatel-Lucent Enterprise aos6 and aos8 devices.
description:
  - This plugin provides low level abstraction APIs for sending CLI commands and
    receiving responses from Alcatel-Lucent Enterprise aos6 and aos8 network devices.
"""

import re
import json

from ansible.module_utils._text import to_text
from ansible.plugins.cliconf import CliconfBase
from textfsm_aos import parser


class Cliconf(CliconfBase):
    def get_capabilities(self):
        capabilities = super(Cliconf, self).get_capabilities()
        capabilities["device_operations"] = self.get_device_operations()
        capabilities["device_info"] = self.get_device_info()
        capabilities["network_api"] = "cliconf"
        capabilities["rpc"] = self.get_aos_rpc()
        # capabilities.upow date(self.get_option_values()) # todo lookinto
        return json.dumps(capabilities)

    def get_device_operations(self):
        return {
            "supports_diff_replace": False,  # identify if config should be merged or replaced is supported
            "supports_commit": False,  # identify if commit is supported by device or not
            "supports_rollback": False,  # identify if rollback is supported or not
            "supports_defaults": False,  # identify if fetching running config with default is supported
            "supports_commit_comment": False,  # identify if adding comment to commit is supported of not
            "supports_onbox_diff": True,  # identify if on box diff capability is supported or not
            "supports_generate_diff": False,  # identify if diff capability is supported within plugin
            "supports_multiline_delimiter": False,  # identify if multiline demiliter is supported within config
            "supports_diff_match": False,  # identify if match is supported
            "supports_diff_ignore_lines": False,  # identify if ignore line in diff is supported
            "supports_config_replace": False,  # identify if running config replace with candidate config is supported
            "supports_admin": False,  # identify if admin configure mode is supported or not
            "supports_commit_label": False,  # identify if commit label is supported or not
        }

    def get_aos_rpc(self):
        return [
            "get_config",  # Retrieves the specified configuration from the device
            # 'edit_config', # Loads the specified commands into the remote device
            "get",  # Execute specified command on remote device
            "get_capabilities",  # Retrieves device information and supported rpc methods
            # 'commit', # Load configuration from candidate to running
            # 'discard_changes', # Discard changes to candidate datastore
        ]

    # def get_option_values(self):
    #     return {
    #         'format': ['text'],
    #         'diff_match': [],
    #         'diff_replace': [],
    #         'output': ['text']
    #     }

    def get_device_info(self):

        device_info = {}

        resource = self.get("show system")
        data = to_text(resource, errors="surrogate_or_strict").strip()

        device_info_raw = {}
        device_info_raw = parser.parse("ale_aos8", "show system", data)
        (device_info_raw,) = device_info_raw

        description_structured = re.search(
            r"^Alcatel-Lucent\sEnterprise\s(\S+)\s((\d+\.){3,}.*?(?=,)),\s\w+\s\d{1,2},\s\d{4,}.",
            device_info_raw["description"],
        )
        description_model = description_structured.group(1)
        description_version = description_structured.group(2)

        if description_model:
            device_info["network_os_model"] = description_model
        if description_version:
            device_info["network_os_version"] = description_version

        device_info["network_os_hostname"] = device_info_raw["name"]
        device_info["network_os_platform"] = "Alcatel-Lucent Enterprise"

        if device_info["network_os_version"][0] == "8":
            device_info["network_os"] = "aos8"
        elif device_info["network_os_version"][0] == "6":
            device_info["network_os"] = "aos6"

        return device_info

    def get_config(self, source="running", flags=None, format=None):

        resource = self.get("show configuration snapshot")
        data = to_text(resource, errors="surrogate_or_strict").strip()

        return data

    def edit_config(self, candidate=None, commit=True, replace=None, comment=None):
        return self.edit_config(
            self, candidate=candidate, commit=commit, replace=replace, comment=comment
        )

        operations = self.get_device_operations()
        self.check_edit_config_capability(
            operations, candidate, commit, replace, comment
        )

        # requests = []
        # responses = []

        # try:
        #     for cmd in to_list(candidate):
        #         # requests.append(cmd['command'])
        #         responses.append(self.send_command(cmd))
        # except  AnsibleConnectionFailure as exc:
        #     raise exc

        # return {'request': requests, 'response': responses}

    def get(
        self,
        command,
        prompt=None,
        answer=None,
        sendonly=False,
        newline=True,
        check_all=False,
    ):
        return self.send_command(
            command=command,
            prompt=prompt,
            answer=answer,
            sendonly=sendonly,
            newline=newline,
            check_all=check_all,
        )
