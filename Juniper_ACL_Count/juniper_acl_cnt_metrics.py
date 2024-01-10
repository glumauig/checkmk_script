from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
)


metric_info["Current_Value_Bytes"] = {
    "title": _("Blocked IP Count in Bytes"),
    "unit": "bytes",
    "color": "16/a",
}

metric_info["Current_Value_Packets"] = {
    "title": _("Blocked IP Count in Packets"),
    "unit": "count",
    "color": "16/a",
}

metric_info["Total_Block_IP_in_Bytes"] = {
    "title": _("Total Blocked IP Count in Bytes"),
    "unit": "bytes",
    "color": "16/a",
}


metric_info["Total_Block_IP_in_Packets"] = {
    "title": _("Total Blocked IP Count in Packets"),
    "unit": "count",
    "color": "16/a",
}

