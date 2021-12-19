#!/bin/python3

# This process adds the overlay vlan to interfaces.

# Version 5.1

import template_functions as f

# requires [prefix]ansible-network.csv to be populated
f.IfNetwork()
