#!/bin/bash
IFACE=docker0
tc qdisc add dev $IFACE root netem delay 10ms 2ms loss 0.1%