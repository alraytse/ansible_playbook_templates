# Version 5.1
import os
import sys
import csv

def checkHelp():
    for arg in sys.argv:
        if arg == '?' or arg == '-?' or arg == '-help':
            printOptions()

def FabNetworks():
    # This functions processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-create.csv')
    output = ""

    # Get the contents of the CSV file
    with open(file) as csvdata:
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "create new network(s) task"'.format(getPadding(2)) +
                    '\n{}dcnm_create_network:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}networks:'.format(getPadding(4))
                )
                # Set the previous fabric name to the current one
                prev_fab = row["fab_name"]

            # Print network section
            output += (
                '\n{}- subnet: {}'.format(getPadding(5), row["network"]) +
                '\n{}vlan: {}'.format(getPadding(6), row["vlan"])
            )
        outputString(output)

def getArgvValue(argkey):
    # Returns a command line argument value for the given arguement key
    result = False # default result if no match is found
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg.count('=') > 0:
                kvp = arg.split('=',1)
                if kvp[0] == argkey and kvp[1] != "":
                    result = kvp[1]
                    break
    return result

def getAuthInfo(url, uid, name):
    # Returns formatted yaml auth info
    return (
        '\n{}base_url: {}'.format(getPadding(4), url) +
        '\n{}username: "{}"'.format(getPadding(4), uid) +
        '\n{}password: '.format(getPadding(4)) +
        '"{{ ansible_password }}"' +
        '\n{}fabric_name: {}'.format(getPadding(4), name)
    )

def getPadding(count):
    # This function returns an amount of padding based on the number passed in the function arguement
    padding = ""
    for i in range(count):
        padding += "  "
    return padding

def getPorts(portslist, padcount):
    # This function print a formatted list of ports
    padding = getPadding(padcount)
    output = ""
    for port in portslist.split(","):
        output += (
            '\n{}- {}'.format(padding, port.capitalize())
        )
    return output

def getUid():
    # This function returns user id
    uid = getArgvValue('uid')
    if uid == False:
        printUsage('\nERROR: A missing or blank User ID is not valid.\n')
    return uid

def Header():
    # Outputs the YAML header section
    output = (
        '---' +
        '\n- name: "DCNM Ansible Modules: Saving Carpal Tunnel[s] Since 2019"' +
        '\n{}hosts: localhost'.format(getPadding(1)) +
        '\n{}gather_facts: false\n'.format(getPadding(1)) +
        '\n{}tasks:'.format(getPadding(1))
    )
    # Always begin with an empty file
    outputString(output, "w")

def IfDecomm():
    # This function processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-decomm.csv')
    output = ''

    # Get the contents of the CSV file
    with open(file) as csvdata:
        # Translate the data into a List
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "interface decomm task"'.format(getPadding(2)) +
                    '\n{}dcnm_default_interface:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}switches:'.format(getPadding(4))
                )
                # Set the previous fabric name to the current one
                prev_fab = row["fab_name"]

            # Switch/Ports section
            output += (
                '\n{}{}:'.format(getPadding(5), row["switch"].lower()) +
                getPorts(row["ports"], 6)
            )
        outputString(output)

def IfDesc():
    # This function processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-desc.csv')
    output = ''

    # Get the contents of the CSV file
    with open(file) as csvdata:
        # Translate the data into a List
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "description task"'.format(getPadding(2)) +
                    '\n{}dcnm_interface_description:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}interfaces:'.format(getPadding(4))
                )
                # Set the previous fabric name to the current one
                prev_fab = row["fab_name"]

            # Switch section
            output += (
                    '\n{}- switch: {}'.format(getPadding(5), row["switch"].lower()) +
                    '\n{}interface: {}'.format(getPadding(6), row["port"].capitalize()) +
                    '\n{}desc: {}'.format(getPadding(6), row["description"])
            )
        outputString(output)

def IfNetwork():
    # This function processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-network.csv')
    output = ""

    # Backout operation
    operation = getArgvValue('backout')
    if operation == "true":
        backout = "True"
    else:
        backout = "False"

    # Get the contents of the CSV file
    with open(file) as csvdata:
        # Translate the data into a List
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        prev_net = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "VNI task"'.format(getPadding(2)) +
                    '\n{}dcnm_attach_overlay:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}backout: {}'.format(getPadding(4), backout) +
                    '\n{}networks:'.format(getPadding(4))
                )
                # Set the previous fabric name to the current one, and clears the previous network
                prev_fab = row["fab_name"]
                prev_net = ""

            # Print new network section if the current network IS NOT the same as the previous network
            if row["network"] != prev_net:
                output += (
                    '\n{}- subnet: {}'.format(getPadding(5), row["network"]) +
                    '\n{}vlan: {}'.format(getPadding(6), row["vlan"]) +
                    '\n{}switch:'.format(getPadding(6))
                )
                # Set the previous network to the current one
                prev_net = row["network"]

            # Switch/Ports section
            output += (
                '\n{}- name: {}'.format(getPadding(7), row["switch"].lower()) +
                '\n{}interfaces:'.format(getPadding(8)) +
                getPorts(row["ports"], 9)
            )
        outputString(output)

def IfPolicy():
    # This function processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-network.csv')
    output = ""

    portmode = getArgvValue('portmode')
    # Port mode should be either "trunk", "routed", or "access" (default)
    if portmode == "trunk":
        # Adds the indicated VLAN to the trunk allowed list
        if_pol = "int_trunk_host_11_1"
    elif portmode == "routed":
        # Sets the port to layer 3 mode
        if_pol = "int_routed_host_11_1"
    else:
        # Sets the "switchport access vlan" to the indicated VLAN
        if_pol = "int_access_host_11_1"

    # Get the contents of the CSV file
    with open(file) as csvdata:
        # Translate the data into a List
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "interface policy task"'.format(getPadding(2)) +
                    '\n{}dcnm_interface_policy:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}policy:'.format(getPadding(4)) +
                    '\n{}- name: {}'.format(getPadding(5), if_pol) +
                    '\n{}switch:'.format(getPadding(6))
                )
                # Set the previous fabric name to the current one
                prev_fab = row["fab_name"]

            # Switch/Ports section
            output += (
                '\n{}- name: {}'.format(getPadding(7), row["switch"].lower()) +
                '\n{}interfaces:'.format(getPadding(8)) +
                getPorts(row["ports"], 9)
            )
        outputString(output)

def IfVpc():
    # This function processes a CSV file and outputs formatted YAML
    file = testFileValid('ansible-vpc.csv')
    output = ""

    portmode = getArgvValue('portmode')
    # Port mode should be either "trunk" or "access" (default)
    if portmode == "trunk":
        if_pol = portmode
    else:
        if_pol = "access"

    # Get the contents of the CSV file
    with open(file) as csvdata:
        # Translate the data into a List
        dictdata = csv.DictReader(csvdata)
        prev_fab = ""
        counter = 0
        # Process each row of data
        for row in dictdata:
            # Current fabric name IS NOT equal to the previous fabric name
            if row["fab_name"] != prev_fab:
                if counter == 0:
                    counter += 1
                else:
                    output += '\n'
                # Try to get the standard url to prevent errors
                if row["fab_name"] in fabricDict:
                    faburl = fabricDict[row["fab_name"]]
                else:
                    faburl = row["fab_url"]
                output += (
                    '{}- name: "create server vpc"'.format(getPadding(2)) +
                    '\n{}dcnm_server_vpc:'.format(getPadding(3)) +
                    getAuthInfo(faburl, uid, row["fab_name"]) +
                    '\n{}vpc_info:'.format(getPadding(4))
                )
                # Set the previous fabric name to the current one
                prev_fab = row['fab_name']

            # VPC_ID section
            output += (
                '\n{}- vpc_id: {}'.format(getPadding(5), row["vpc_id"]) +
                '\n{}policy: {}'.format(getPadding(6), if_pol) +
                '\n{}switch_one:'.format(getPadding(6)) +
                '\n{}name: {}'.format(getPadding(7), row["sw1_name"]) +
                '\n{}po_description: {}'.format(getPadding(7), row["sw1_desc"]) +
                '\n{}member_interface: {}'.format(getPadding(7), row["sw1_port"].capitalize()) +
                '\n{}switch_two:'.format(getPadding(6)) +
                '\n{}name: {}'.format(getPadding(7), row["sw2_name"]) +
                '\n{}po_description: {}'.format(getPadding(7), row["sw2_desc"]) +
                '\n{}member_interface: {}'.format(getPadding(7), row["sw2_port"].capitalize())
            )
        outputString(output)

def outputString(data, mode="a"):
    # This function checks to see if an output filename was specified on the comand line and if so writes the output to the indicated filename
    # Check if an output filename was given
    outfile = getArgvValue('outfile')
    if outfile != False:
        try:
            # Try to open the file and write the output
            f = open(outfile, mode)
            f.write(data + '\n')
        finally:
            f.close()
    else:
        # No output file specified so default to print the output to the screen
        print (data)

def printOptions():
    # This function passes a command line parameter message to printUsage
    printUsage(
        '\n{}REQUIRED\n'.format(getPadding(1)) +
        '{}uid        Specifies the user id to use in data generation.\n'.format(getPadding(2)) +
        '\n{}OPTIONS\n'.format(getPadding(1)) +
        '{}backout    Specifies whether to add (backout=false[default]) overlay network(s) to, or to remove (backout=true) from, interfaces. (only takes effect when using the IfNetwork function)\n'.format(getPadding(2)) +
        '{}outfile    Specifies the output file to write the generated data to. If outfile is not specified all output is to the screen.\n'.format(getPadding(2)) +
        '{}portmode   Specifies the port mode of the interface policy (access[default], routed, trunk). (Only takes effect when using the IfPolicy or IfVpc functions)\n'.format(getPadding(2)) +
        '{}prefix     Specifies the input data file prefix. Example: specifying CRQ1234- as a prefix would tell the IfDesc function to read CRQ1234-ansible-desc.csv file instead of the default ansible-desc.csv file.\n'.format(getPadding(2))
    )

def printUsage(msg=""):
    # This function prints a potential message and then a generic usage message
    sys.exit(
        '{}\nUsage: {} <REQUIRED=value>... [OPTION=value]...\n'.format(msg, os.path.basename(sys.argv[0])) +
        '{}?, -?, -help for help\n'.format(getPadding(2))
    )

def testFileValid(file):
    # This function tests if a file is valid and ends the program if not
    prefix = getArgvValue('prefix')
    if prefix != False:
        file = prefix + file
    if os.path.isfile(file) == False:
        sys.exit('{} is missing. Terminating early.'.format(file))
    return file

# Do these things when this file is imported into another script
checkHelp()
uid = getUid()
Header()

fabricDict =   {"PDC1-MANAGEMENT-FABRIC":"https://dcnm-pdc1.cdc.schwab.com",
                "PDC1-PRODUCTION-E-CORE":"https://dcnm-pdc1.cdc.schwab.com",
                "DC4-MANAGEMENT-FABRIC":"https://dcnm-pdc1.cdc.schwab.com",
                "DC4-SERVICES-FABRIC":"https://dcnm-pdc1.cdc.schwab.com",
                "PDC1-PRODUCTION-F-CORE":"https://dcnm-cdc-f.cdc.schwab.com",
                "PDC3-MANAGEMENT-FABRIC":"https://dcnm-pdc3.cdc.schwab.com",
                "PDC3-PRODUCTION-E-CORE":"https://dcnm-pdc3.cdc.schwab.com",
                "PDC3-PRODUCTION-F-CORE":"https://dcnm-bdc-f.cdc.schwab.com",
                "DC4-PRODUCTION-E-CORE":"https://dcnm-tdc.cdc.schwab.com",
                "DC4-PRODUCTION-F-CORE":"https://dcnm-tdc.cdc.schwab.com",
                "DC4-PRODUCTION-R-CORE":"https://dcnm-tdc-r.cdc.schwab.com",
                "PDC1-DEV-FABRIC":"https://dcnm-dev.dev.schwab.com",
                "PDC3-DEV-FABRIC":"https://dcnm-dev.dev.schwab.com",
                "PDC3-DEV-TDA-FABRIC":"https://svip1-svs0064bdc.us.global.schwab.com",
                "EQ-CH01-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "EQ-SV05-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "EQ-NY05-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "EQ-DC11-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "EQ-DA01-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "EQ-DE02-MGMT-FABRIC":"https://dcnm-eq.cdc.schwab.com",
                "PDC1-LAB1-Fabric":"https://dcnm-lab.dev.schwab.com"
               }
