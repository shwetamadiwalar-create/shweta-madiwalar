#!/usr/bin/env python3
import json, time
from hashlib import sha256

def load_data():
    stakes = json.load(open("stake_table.json"))
    validators = json.load(open("validators_epoch.json"))
    return stakes, validators
