from .agent_based_api.v1 import *
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    get_value_store,
)

def parse_juniper_acl_cnt(string_table):
    parsed = {}
    Total_Bytes = {}
    Total_Packets = {}
    JACL_count ={}

    for service, _packet, _bytes  in string_table:
        if service != '':
            JACL_count['ACL name'] = str(service)
            #print(service + "- This is the value of service")
        #elif _packet !='':
            JACL_count['Packet drop'] = int(_packet)
            #print(_packet + "- This is the value of packet")

        #elif _bytes !='':
            JACL_count['Byte drop'] = int(_bytes)
            #print(_bytes + "- This is the value of bytes")

        if 'ACL name' in JACL_count and 'Packet drop' in JACL_count and 'Byte drop' in JACL_count:
            parsed[JACL_count['ACL name']] = JACL_count
            #JACL_count = {}
    #return parsed
    return parsed


def discover_juniper_acl_cnt(section):
   for service  in section.keys():
        yield Service(item=service)

def check_juniper_acl_cnt(item,section): 
    #try:
    #    byte_cnt = int(section[0][2])
    #    packet_cnt= int(section[0][1])
    #except:
    #    return

    if item not in section:
        return
    
    #print(section[item]['Packet drop'])
    packet_cnt = int(section[item]['Packet drop'])
    byte_cnt = int(section[item]['Byte drop'])


    persistent_values_byte = get_value_store()
    persistent_values_packet = get_value_store()

    if not persistent_values_byte.get('previous_value_byte') or not persistent_values_packet.get('previous_value_packet'):
        persistent_values_byte['previous_value_byte'] = int(byte_cnt)
        persistent_values_packet['previous_value_packet'] = int(packet_cnt)
        previous_value_byte = byte_cnt
        previous_value_packet = packet_cnt
    else:
        previous_value_byte = persistent_values_byte['previous_value_byte']
        previous_value_packet = persistent_values_packet['previous_value_packet']
        persistent_values_byte['previous_value_byte'] = byte_cnt
        persistent_values_packet['previous_value_packet']=packet_cnt

    diff_value_bytes = int(byte_cnt) - int(previous_value_byte)
    diff_value_packets = int(packet_cnt) - int(previous_value_packet)

    if diff_value_bytes ==0:
        current_state = "The current ACL count in bytes: "+str(byte_cnt)+" in packet: "+ str(packet_cnt)
        yield Result(state=State.OK, summary=current_state)

    else:
        current_state = "Blocked IP count is increasing | bytes: "+str(diff_value_bytes)+" packets: "+str(diff_value_packets)+"|| Current IP Blocked | bytes:  "+str(byte_cnt)+" packets: "+str(packet_cnt)
        yield Result(state=State.WARN, summary=current_state)

    yield Metric("Total_Block_IP_in_Bytes",byte_cnt)
    yield Metric("Total_Block_IP_in_Packets",packet_cnt)
    yield Metric("Current_Value_Bytes",diff_value_bytes)
    yield Metric("Current_Value_Packets",diff_value_packets)

    return


register.snmp_section(
    name = "juniper_acl_cnt",
    detect = exists(".1.3.6.1.4.1.2636.3.5.1.1.2.12.*"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.2636.3.5.1.1',
        oids = [
                '2.12.66', #jnxFWCounter
                '4.12.66', #jnxFWPackets
                '5.12.66', #jnxFWBytes
        ],
    ),
    parse_function = parse_juniper_acl_cnt,
)

register.check_plugin(
    name='juniper_acl_cnt',
    service_name='Juniper ACL count %s',
    discovery_function=discover_juniper_acl_cnt,
    check_function=check_juniper_acl_cnt,
    )
