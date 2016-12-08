# Copyright (C) 2004-2016 CS-SI. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoannv@gmail.com>
#
# This file is part of the Prewikka program.
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
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from __future__ import absolute_import, division, print_function, unicode_literals

import abc
import sys
import traceback

import pkg_resources
from prewikka import log, response, template
from prewikka.utils import AttrObj, json


class PrewikkaException(Exception):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def respond(self):
        pass



class RedirectionError(PrewikkaException):
    def __init__(self, location, code):
        self.location = location
        self.code = code

    def respond(self):
        return response.PrewikkaRedirectResponse(self.location, code=self.code)



class PrewikkaError(PrewikkaException):
    template = template.PrewikkaTemplate(__name__, 'templates/error.mak')
    name = N_("An unexpected condition happened")
    message = ""
    details = ""
    code = 500
    log_priority = log.ERROR
    display_traceback = True

    def __init__(self, message, name=None, details=None, log_priority=None, log_user=None, template=None, code=None):
        if name is not None:
            self.name = name

        if message is not None:
            self.message = message

        if details is not None:
            self.details = details

        self._untranslated_name = text_type(self.name)
        self._untranslated_message = text_type(self.message)
        self._untranslated_details = text_type(self.details)

        if self._untranslated_name:
            self.name = _(self._untranslated_name)

        if self._untranslated_message:
            self.message = _(self._untranslated_message)

        if self._untranslated_details:
            self.details = _(self._untranslated_details)

        if template:
            self.template = template

        if code:
            self.code = code

        if log_priority:
            self.log_priority = log_priority

        self.traceback = self._get_traceback()
        self.log_user = log_user

    def _setup_template(self, template, ajax_error):
        dataset = template.dataset()

        for i in ("name", "message", "details", "code", "traceback"):
            dataset[i] = getattr(self, i)

        dataset["is_ajax_error"] = ajax_error
        dataset["document"] = AttrObj()
        dataset["document"].base_url = env.request.web.get_baseurl()
        dataset["is_error_template"] = True

        return dataset

    def _html_respond(self):
        from prewikka import baseview
        return baseview.BaseView().respond(self._setup_template(self.template, False), self.code)

    def _get_traceback(self):
        if self.display_traceback and env.config.general.get("enable_error_traceback") not in ('no', 'false'):
            return sys.exc_info()

    def respond(self):
        if self.message:
            env.log.log(self.log_priority, self)

        if not self.traceback:
            self.traceback = self._get_traceback()

        if not (env.request.web.is_stream or env.request.web.is_xhr):
            # This case should only occur in case of auth error (and viewmgr might not exist at this time)
            return self._html_respond()

        return response.PrewikkaResponse(self, code=self.code)

    @staticmethod
    def _format_error(message, details):
        if details:
            return message + ": " + details

        return message

    def __str__(self):
        return self._format_error(self._untranslated_message, self._untranslated_details)

    def __json__(self):
        dset = self._setup_template(PrewikkaError.template, True)
        return { "content": dset.render() }



class PrewikkaUserError(PrewikkaError):
    display_traceback = False

    def __init__(self, name=None, message=None, **kwargs):
        PrewikkaError.__init__(self, message, name=name, **kwargs)


class NotImplementedError(PrewikkaError):
    name = N_("Not implemented")

    def __init__(self, message=N_("Backend does not implement this operation")):
        PrewikkaError.__init__(self, message, log_priority=log.ERROR)
