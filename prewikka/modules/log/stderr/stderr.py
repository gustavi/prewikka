# Copyright (C) 2004 Nicolas Delon <nicolas@prelude-ids.org>
# All Rights Reserved
#
# This file is part of the Prelude program.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.


import sys
import os

from prewikka import Log


class LogStderr(Log.LogBackend):
    def __call__(self, type, event, request, view, user, details):
        message = "[%s/%s] " % (type, event)
        separator = ""
        
        if request:
            message += "peer %s:%d" % (request.getClientAddr(), request.getClientPort())
            separator = "; "

        if user:
            message += "%suser %s" % (separator, user.login)
            separator = "; "

        if view:
            message += "%sview %s" % (separator, view["name"])
            separator = "; "

        if details:
            message += separator + details

        print >> sys.stderr, message



def load(env, config):
    return LogStderr(config)
