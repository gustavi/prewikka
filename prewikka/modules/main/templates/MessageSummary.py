#!/usr/bin/env python

"""
Autogenerated by CHEETAH: The Python-Powered Template Engine
 CHEETAH VERSION: 0.9.15
 Generation time: Fri Jul 16 18:49:32 2004
   Source file: prewikka/modules/main/templates/MessageSummary.tmpl
   Source file last modified: Fri Jul 16 18:49:04 2004
"""

__CHEETAH_genTime__ = 'Fri Jul 16 18:49:32 2004'
__CHEETAH_src__ = 'prewikka/modules/main/templates/MessageSummary.tmpl'
__CHEETAH_version__ = '0.9.15'

##################################################
## DEPENDENCIES

import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers
from prewikka.Views import NormalLayoutView

##################################################
## MODULE CONSTANTS

try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFS=valueFromSearchList
VFN=valueForName
currentTime=time.time

##################################################
## CLASSES

class MessageSummary(NormalLayoutView):
    """
    
    Autogenerated by CHEETAH: The Python-Powered Template Engine
    """

    ##################################################
    ## GENERATED METHODS


    def __init__(self, *args, **KWs):
        """
        
        """

        NormalLayoutView.__init__(self, *args, **KWs)

    def main_content(self,
            trans=None,
            dummyTrans=False,
            VFS=valueFromSearchList,
            VFN=valueForName,
            getmtime=getmtime,
            currentTime=time.time,
            globals=globals,
            locals=locals,
            __builtin__=__builtin__):


        """
        Generated from #block main_content at line 4, col 1.
        """

        if not trans:
            trans = DummyTransaction()
            dummyTrans = True
        write = trans.response().write
        SL = self._searchList
        filter = self._currentFilter
        globalSetVars = self._globalSetVars
        
        ########################################
        ## START - generated method body
        
        for section in VFS(SL + [globals(), __builtin__],"sections",True):
            write('\t<div class="section_alert">\n\t\t<div class="section_alert_title">')
            write(filter(VFN(section,"title",True), rawExpr='$section.title')) # from line 7, col 36.
            write('''</div>
		
		<table class="section_alert_entries">
''')
            row_classes = ("table_row_even", "table_row_odd")
            write('')
            entry_value_classes = ("section_alert_entry_value_normal", "section_alert_entry_value_emphasis")
            write('')
            cnt = 0
            write('')
            for entry in VFN(section,"entries",True):
                write('\t\t\t\t<tr class="section_alert_entry ')
                write(filter(row_classes[cnt%2], rawExpr='$row_classes[$cnt%2]')) # from line 14, col 36.
                write('">\n\t\t\t\t\t<td class="section_alert_entry_name">')
                write(filter(VFN(entry,"name",True), rawExpr='$entry.name')) # from line 15, col 43.
                write('</td>\n\t\t\t\t\t<td class="')
                write(filter(entry_value_classes[VFN(entry,"emphase",True)], rawExpr='$entry_value_classes[$entry.emphase]')) # from line 16, col 17.
                write('">')
                write(filter(VFN(entry,"value",True), rawExpr='$entry.value')) # from line 16, col 55.
                write('</td>\n\t\t\t\t</tr>\n')
                cnt += 1
                write('')
            write('\t\t</table>\n\t</div>\n')
        
        ########################################
        ## END - generated method body
        
        if dummyTrans:
            return trans.response().getvalue()
        else:
            return ""
        

    def writeBody(self,
            trans=None,
            dummyTrans=False,
            VFS=valueFromSearchList,
            VFN=valueForName,
            getmtime=getmtime,
            currentTime=time.time,
            globals=globals,
            locals=locals,
            __builtin__=__builtin__):


        """
        This is the main method generated by Cheetah
        """

        if not trans:
            trans = DummyTransaction()
            dummyTrans = True
        write = trans.response().write
        SL = self._searchList
        filter = self._currentFilter
        globalSetVars = self._globalSetVars
        
        ########################################
        ## START - generated method body
        
        write('\n')
        self.main_content(trans=trans) # generated from ('main_content', '#block main_content') at line 4, col 1.
        
        ########################################
        ## END - generated method body
        
        if dummyTrans:
            return trans.response().getvalue()
        else:
            return ""
        
    ##################################################
    ## GENERATED ATTRIBUTES


    _mainCheetahMethod_for_MessageSummary= 'writeBody'


# CHEETAH was developed by Tavis Rudd, Mike Orr, Ian Bicking and Chuck Esterbrook;
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org

##################################################
## if run from command line:
if __name__ == '__main__':
    MessageSummary().runAsMainProgram()

