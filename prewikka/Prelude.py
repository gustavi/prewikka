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


import prelude
import preludedb
from preludedb import PreludeDB


Error = (prelude.Error, preludedb.Error)


class Message:
    def __init__(self, message):
        self._message = message

    def __getitem__(self, key):
        return self._message[key]
    
    def get(self, key, default=None):
        value = self[key]
        return value is None and default or value

    def getAdditionalData(self, searched, many_values=False):
        values = [ ]
        i = 0
        while True:
            meaning = self["%s.additional_data(%d).meaning" % (self._root, i)]
            if meaning is None:
                break
            
            if meaning == searched:
                value = self["%s.additional_data(%d).data" % (self._root, i)]
                if not many_values:
                    return value
                
                values.append(value)

            i += 1

        return many_values and [ ] or None

    def __str__(self):
        return str(self._message)



class Alert(Message):
    _root = "alert"
    
    def __getitem__(self, key):
        if key.find("alert.") != 0:
            key = "alert." + key
        return Message.__getitem__(self, key)



class Heartbeat(Message):
    _root = "heartbeat"
    
    def __getitem__(self, key):
        if key.find("heartbeat.") != 0:
            key = "heartbeat." + key
        return Message.__getitem__(self, key)



class Prelude(PreludeDB):
    def __init__(self, config):
        PreludeDB.init()
        PreludeDB.__init__(self,
                           type=config.getOptionValue("type", "mysql"),
                           host=config.getOptionValue("host", "127.0.0.1"),
                           port=config.getOptionValue("port", 0),
                           name=config.getOptionValue("name", "prelude"),
                           user=config.getOptionValue("user", "prelude"),
                           password=config.getOptionValue("password", "prelude"))
        self.connect()

    def getAlertIdents(self, criteria=None, limit=-1, offset=-1):
        if criteria:
            criteria = prelude.IDMEFCriteria(criteria)
        return self.get_alert_ident_list(criteria, limit, offset) or [ ]

    def getHeartbeatIdents(self, criteria=None, limit=-1, offset=-1):
        if criteria:
            criteria = prelude.IDMEFCriteria(criteria)
        return self.get_heartbeat_ident_list(criteria, limit, offset) or [ ]

    def _getLastMessageIdent(self, type, analyzerid):
        criteria = None
        if analyzerid != None:
            criteria = "%s.analyzer.analyzerid == %d" % (type, analyzerid)

        rows = self.getValues(selection=("%s.create_time/order_desc" % type, "%s.messageid" % type),
                              criteria=criteria, limit=1)

        return rows[0][1]

    def getLastAlertIdent(self, analyzer=None):
        return self._getLastMessageIdent("alert", analyzer)

    def getLastHeartbeatIdent(self, analyzer=None):
        return self._getLastMessageIdent("heartbeat", analyzer)

    def getAlert(self, analyzerid, alert_ident):
        return Alert(self.get_alert(analyzerid, alert_ident))

    def deleteAlert(self, analyzerid, alert_ident):
        return self.delete_alert(analyzerid, alert_ident)

    def getHeartbeat(self, analyzerid, heartbeat_ident):
        return Heartbeat(self.get_heartbeat(analyzerid, heartbeat_ident))

    def deleteHeartbeat(self, analyzerid, heartbeat_ident):
        return self.delete_heartbeat(analyzerid, heartbeat_ident)

    def getValues(self, selection, criteria=None, distinct=0, limit=-1, offset=-1):
        if criteria:
            criteria = prelude.IDMEFCriteria(criteria)
        
        return self.get_values(selection, criteria, distinct, limit, offset) or [ ]

    def _countMessages(self, root, criteria):
        return self.getValues(["count(%s.messageid)" % root], criteria)[0][0]

    def countAlerts(self, criteria=None):
        return self._countMessages("alert", criteria)

    def countHeartbeats(self, criteria=None):
        return self._countMessages("heartbeat", criteria)

    def getAnalyzerids(self):
        analyzerids = [ ]
        rows = self.getValues(selection=[ "heartbeat.analyzer.analyzerid/group_by" ])
        for row in rows:
            analyzerid = row[0]
            analyzerids.append(analyzerid)

        return analyzerids

    def getAnalyzer(self, analyzerid):
        ident = self.getLastHeartbeatIdent(analyzerid)
        heartbeat = self.getHeartbeat(analyzerid, ident)
        
        analyzer = { }
        analyzer["analyzerid"] = analyzerid
        analyzer["name"] = heartbeat.get("heartbeat.analyzer.name", "n/a")
        analyzer["model"] = heartbeat.get("heartbeat.analyzer.model", "n/a") 
        analyzer["version"] = heartbeat.get("heartbeat.analyzer.version", "n/a")
        analyzer["ostype"] = heartbeat.get("heartbeat.analyzer.ostype", "n/a")
        analyzer["osversion"] = heartbeat.get("heartbeat.analyzer.osversion", "n/a")
        analyzer["node_name"] = heartbeat.get("heartbeat.analyzer.node.name", "n/a")
        analyzer["node_location"] = heartbeat.get("heartbeat.analyzer.node.location", "n/a")
        analyzer["node_address"] = heartbeat.get("heartbeat.analyzer.node.address(0).address", "n/a")
        analyzer["last_heartbeat_time"] = heartbeat.get("heartbeat.create_time")
        analyzer["last_heartbeat_interval"] = heartbeat.getAdditionalData("Analyzer heartbeat interval")
        analyzer["last_status"] = heartbeat.getAdditionalData("Analyzer status")
        
        return analyzer
