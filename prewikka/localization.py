# Copyright (C) 2007 PreludeIDS Technologies. All Rights Reserved.
# Author: Yoann Vandoorselaere <yoann.v@prelude-ids.com>
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
# You should have received a copy of the GNU General Public License
# along with this program; see the file COPYING.  If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.

import locale, gettext, __builtin__, time
from prewikka import siteconfig

try: 
    import threading    

except ImportError:
    _lock = None
    currentThread = lambda: "none"

else:
    _lock = threading.Lock()
    currentThread = threading.currentThread


_DEFAULT_LANGUAGE = "en"
_localized_thread = { }
_all_locale = { _DEFAULT_LANGUAGE: None }


def _safeGettext(s):
    tid = currentThread()
    if _localized_thread.has_key(tid) and _localized_thread[tid] != None:
        return _localized_thread[tid].gettext(s)
    else:
        return s

def _deferredGettext(s):
    return s
    
gettext.install("prewikka", siteconfig.locale_dir)
__builtin__._ = _safeGettext
__builtin__.N_ = _deferredGettext


_LANGUAGES = { 
               _("Brazilian Portuguese"): "pt_BR",
               _("English"): "en", 
               _("French"): "fr", 
             }
    

def setLocale(lang):
    if _lock:
        _lock.acquire()
    
    if not _all_locale.has_key(lang):
        _all_locale[lang] = gettext.translation("prewikka", siteconfig.locale_dir, languages=[lang])
        
    if _lock:
        _lock.release()
            
    _localized_thread[currentThread()] = _all_locale[lang]


def getLanguages():
    return [ _(x) for x in _LANGUAGES.keys() ]
        

def getLanguagesIdentifiers():
    return _LANGUAGES.values()


def getLanguagesAndIdentifiers():
    return [ (_(x), y) for x, y in _LANGUAGES.items() ]


def getCurrentCharset():
    tid = currentThread()
    
    if _localized_thread.has_key(tid) and _localized_thread[tid] != None:
        return _localized_thread[currentThread()].charset()
    else:
        return "iso-8859-1"

def getDate():
    _localized_month = [ _("January"), 
                         _("February"), 
                         _("March"), 
                         _("April"), 
                         _("May"), 
                         _("June"), 
                         _("July"), 
                         _("August"), 
                         _("September"),
                         _("November"), 
                         _("October"), 
                         _("December") ]

    _localized_weekday = [ _("Monday"),
                           _("Tuesday"),
                           _("Wednesday"),
                           _("Thursday"),
                           _("Friday"),
                           _("Saturday"),
                           _("Sunday") ]
                                
    weekday, day, month, year = time.strftime("%A %d %B %Y").split()
    return " ".join((_(weekday).lower(), day, _(month).lower(), year))


