import re
from .agent_based_api.v1 import *
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
   get_value_store,
)



def discover_bcnet_hvac_controller(section):
    yield Service()

def check_bcnet_hvac_controller(section):
    
    #hvac_snmp_name = str(section[0][0])
    #hvac_snmp_value = int(section[0][1])
    hvac_snmp_name = []
    hvac_snmp_value =[]
    
    var_test = "test me"
    for hvac_snmp_count in range (0,66):
        if hvac_snmp_count%2 == 0:
            hvac_snmp_name.append(str(section[0][hvac_snmp_count]))
        else:
            hvac_snmp_value.append(int(section[0][hvac_snmp_count]))
    

    for i in range(len(hvac_snmp_name)):
        hvac_snmp_name[i]=re.sub(r"\s+", "_", hvac_snmp_name[i])
        hvac_snmp_name[i]=re.sub(r"/+", "-", hvac_snmp_name[i])
        hvac_snmp_name[i]=re.sub(r"BCN-+", "BCN_", hvac_snmp_name[i])
        print(hvac_snmp_name[i])
        summary_hvac = "" + hvac_snmp_name[i] + ": "+str(hvac_snmp_value[i])
        yield Result(state=State.OK,summary=summary_hvac)
        yield Metric(hvac_snmp_name[i],hvac_snmp_value[i])
        #yield Metric("test",hvac_snmp_value[i])
    '''
    my_test= "Values of SNMP "+hvac_snmp_name+": "+str(hvac_snmp_value)
    yield Result(state=State.OK,summary=my_test)
    print(hvac_snmp_value) 
    x=1
    yield Metric("hvac_snmp_name",hvac_snmp_value)
    #yield Metric("VALUE Now",str(hvac_snmp_value))
    '''
    return

##initials - register snmp section

list1= []
for x in range (1,14):
    list1.append('5.'+str(x))
    list1.append('2.'+str(x))

for x in range (21,31):
    list1.append('5.'+str(x))
    list1.append('2.'+str(x))

for x in range (51,61):
    list1.append('5.'+str(x))
    list1.append('2.'+str(x))

print(len(list1))


'''
for i in range (0,10):
    if i%2==0:
        print("Hello "+str(i))
    else:
        print("Hi "+str(i))
'''                
register.snmp_section(
    name = "bcnet_hvac_controller",
    detect = exists(".1.3.6.1.4.1.15255.1.2.1.3.1.5.*"),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.15255.1.2.1.3.1',
        oids = list1,
        #oids = [
        #        '5.1', #variableObjName
        #        '2.1', #variableValInt
        #],
    ),
    #parse_function = parse_bcnet_hvac,
)

##register plugins
register.check_plugin(
    name='bcnet_hvac_controller',
    service_name='HVAC Controller',
    discovery_function= discover_bcnet_hvac_controller,
    check_function= check_bcnet_hvac_controller,
    )
