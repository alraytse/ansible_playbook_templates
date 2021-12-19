#!/bin/python3

# This process reverts given interfaces to a default state (description indicates AVAILABLE, and removes vlans and such)

# Version 5.1

import template_functions as f

# requires [prefix]ansible-decomm.csv to be populated
f.IfDecomm()
