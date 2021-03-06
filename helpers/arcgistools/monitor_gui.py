#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
########################################################################################################################
# Copyright © 2019-2020 Pi-Yueh Chuang and Lorena A. Barba.
# All Rights Reserved.
#
# Contributors: Pi-Yueh Chuang <pychuang@gwu.edu>
#
# Licensed under the BSD-3-Clause License (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at: https://opensource.org/licenses/BSD-3-Clause
#
# BSD-3-Clause License:
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided
# that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
#    promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
########################################################################################################################
"""
A Tk GUI for monitoring Azure status.
"""
import sys
import tkinter

class AzureMonitorWindow(tkinter.Frame):
    """The base and frame for printing information."""

    def __init__(self, master=None):
        """__init__"""
        super().__init__(master)
        self.master = master
        self.pack()
        self.init_button()
        self.init_text()

    def init_button(self):
        """Definition of the Quit button."""
        self.button = tkinter.Button(self)
        self.button["text"] = "Quit"
        self.button["command"] = self.master.destroy
        self.button.pack(side="bottom")

    def init_text(self):
        """Initialization of the text section."""
        self.text = tkinter.Text(self, state=tkinter.DISABLED)
        self.text.pack(side=tkinter.LEFT, fill=tkinter.Y)

        self.scrollbar = tkinter.Scrollbar(self)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        self.text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text.yview)

    def update_text(self, s):
        """Update the text inf the text section with s."""
        vw = self.text.yview()
        self.text.config(state=tkinter.NORMAL)
        self.text.delete(1.0, tkinter.END)
        self.text.insert(tkinter.END, s)
        self.text.config(state=tkinter.DISABLED)
        self.text.yview_moveto(vw[0])
