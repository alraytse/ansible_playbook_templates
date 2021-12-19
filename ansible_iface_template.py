#!/bin/python3

# This process sets the policy for given interfaces, then sets interface descriptions, and then adds the overlay vlan to those interfaces.

# Version 5.1

import template_functions as f

# requires [prefix]ansible-network.csv to be populated
f.IfPolicy()

# requires [prefix]ansible-desc.csv to be populated
f.IfDesc()

# requires [prefix]ansible-network.csv to be populated
f.IfNetwork()
