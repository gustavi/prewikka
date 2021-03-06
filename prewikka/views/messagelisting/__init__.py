from __future__ import absolute_import, division, print_function, unicode_literals

from prewikka import pluginmanager, version

from .alertlisting import AlertListing, CorrelationAlertListing
from .heartbeatlisting import HeartbeatListing
from .messagelisting import HostInfoAjax


class MessageListing(pluginmanager.PluginPreload):
    plugin_name = "Alert and Heartbeat listing"
    plugin_author = "Nicolas Delon, %s" % version.__author__
    plugin_license = version.__license__
    plugin_version = version.__version__
    plugin_copyright = version.__copyright__
    plugin_description = N_("Alert and Heartbeat listing page")

    plugin_classes = [AlertListing, CorrelationAlertListing, HeartbeatListing, HostInfoAjax]
