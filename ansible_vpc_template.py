#!/bin/python3

# This process creates the VPC and configures it onto switch ports, then sets the server-facing interface descriptions

# Version 5.1

import template_functions as f

# requires [prefix]ansible-vpc.csv to be populated
f.IfVpc()
