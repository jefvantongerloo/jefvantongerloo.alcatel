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
terminal: jefvantongerloo.aos.aos
short_description: Terminal support for Alcatel-Lucent Enterprise aos6 and aos8 devices
description:
  - This plugin provides the pseudo terminal for connecting and setup channels for 
    sessions to Alcatel-Lucent Enterprise aos6 and aos8 network devices.
"""

import re
from ansible.plugins.terminal import TerminalBase


class TerminalModule(TerminalBase):

    #: compiled bytes regular expressions as stdout
    terminal_stdout_re = [
        # Prompt can be anything, but best practice is to end with > or #
        re.compile(rb"[a-zA-Z0-9.\-_@\/:]{1,63}[>|#]\s*$")
    ]

    #: compiled bytes regular expressions as stderr
    terminal_stderr_re = [
        re.compile(rb"Authentication failure", re.IGNORECASE),
        re.compile(rb"[\r\n]ERROR:\s*.*[\r\n]+", re.IGNORECASE),
    ]

    #: compiled bytes regular expressions to remove ANSI codes
    ansi_re = []

    #: terminal initial prompt
    terminal_initial_prompt = None

    #: terminal initial answer
    terminal_initial_answer = None

    #: Send newline after prompt match
    terminal_inital_prompt_newline = False

    def __init__(self, *args, **kwargs):
        super(TerminalModule, self).__init__(*args, **kwargs)

    def warning(self, msg):
        self._connection.queue_message("warning", msg)
