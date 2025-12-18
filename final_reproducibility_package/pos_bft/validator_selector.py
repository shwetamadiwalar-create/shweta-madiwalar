#!/usr/bin/env python3
import json, random
from hfc.fabric import Client

client = Client(net_profile="network.json")
def query_stakes():
    resp = client.chaincode_query(
        requestor="Admin",
        channel_name="mychannel",
        cc_name="stake_cc",
        fcn="GetStakeTable",
        args=[]
    )
    return json.loads(resp)
