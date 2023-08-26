#!/usr/bin/env python

# Name: uploadFPPConfigs,py
# Purpose: Upload an FPP Config to FPP instance using a csv formatted input file 
# Author: Bill Jenkins
# Version: v2.1
# Date: 08/26/2022

###########################
# Imports                 #
###########################

import argparse
import sys
import subprocess
import os
import time
import re
import requests
import json
import ast
###########################
# From Imports            #
###########################
from functools import partial
from tkinter import *
from tkinter import ttk
from pathlib import Path

###############################
# path_exists_case_sensitive  #
###############################

def path_exists_case_sensitive(path, verbose) -> bool:
    p = Path(path)
    # If it doesn't exist initially, return False
    if not p.exists():
        if (verbose):
            print ("Initial Path not found")
        return False
    # Else loop over the path, checking each consecutive folder for
    # case sensitivity
    while True:
        if (verbose):
            print ("path = ", p)
        # At root, p == p.parent --> break loop and return True
        if p == p.parent:
            return True
        # If string representation of path is not in parent directory, return False
        if str(p) not in map(str, p.parent.iterdir()):
            if (verbose):
                print("Parent path not found")
            return False
        p = p.parent

###############################
# doRequestsGet               #
###############################
def doRequestsGet(request, timeout, verbose):

    try:
        r = requests.get(request, timeout=(timeout))
        ret_code = 0
        status_code = r.status_code
        result = r.text

    # HTTP Error?
    except requests.exceptions.HTTPError as e:
        ret_code = -1
        status_code = ""
        result = "##### Request HTTP Error: " + format(str(e))

    # HTTP Connection Error?   
    except requests.exceptions.ConnectionError as e:
        ret_code = -2
        status_code = ""
        result = "##### Request Connection Error: " + format(str(e))

    # HTTP Timeout?
    except requests.exceptions.Timeout as e:
        ret_code = -3
        status_code = ""
        result = "##### Request Timeout Error: " + format(str(e))
    
    # HTTP Other?
    except requests.exceptions.RequestException as e:
        ret_code = -4
        status_code = ""
        result = "##### Request Exception Error: " + format(str(e))

    return(ret_code, status_code, result)

###############################
# startxLights                  #
###############################

def startxLights(baseURL, xlightsprogram, verbose):

    # xLights Running?
    request = baseURL + "getVersion"
    if (verbose):
        print ("##### Get Version")
        print ("request=", request)
    startloop = True
    started = False
    retryctr = 0
    while (startloop):
        (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
        match ret_code:
            # REST API Connection Successful
            case 0:
                startloop = False
                if (verbose):
                    print ("status_code = ", status_code)
                    print ("result = ", result)
            # REST API Connection Error?
            case -2:
                if (not started):
                    # Start xLights
                    cmd = "\"" + xlightsprogram + "\""
                    if (verbose):
                        print ("##### Start xLights")
                        print ("cmd = ", cmd)
                    try:
                        cp = subprocess.Popen(cmd)
                    except:
                        sys.exit("*** Error in starting xLights %s" % sys.exc_info()[0])
                
                    started = True
                    retryctr = retryctr + 1
                    if (retryctr <= 10):
                        time.sleep(3)
                    else:
                        startloop = False
            # REST API Error?
            case _:
                startloop = False
            
    return(ret_code, status_code, result)

import urllib.parse

###############################
# createParamsStr              #
###############################

def createParamsStr(params_dict, verbose): 

    if (verbose):
        print ("params_dict = %s" % params_dict)

    params_str = ""
    params_ctr = 0
    params_len = len(params_dict) 

    for params_key, params_value in params_dict.items():
        params_ctr += 1
        if (params_ctr == 1):
            if params_ctr == params_len:
                params_str = "?" + params_key + "=" + str(params_value)
            else:
                params_str = "?" + params_key + "=" + str(params_value) + "&"
        elif(params_ctr < params_len):
            params_str = params_str + params_key + "=" + str(params_value) + "&"
        else:
            params_str = params_str + params_key + "=" + str(params_value)
    params_str = re.sub(" ", "%20", params_str)
    if (verbose):
        print ("params_str = %s" % params_str)
    
    return(params_str)

###############################
# uploadFPPConfig              #
###############################

def uploadFPPConfig(baseURL, fppip, fppudp, fppmodels, fppmap, verbose):

    
    params_dict =  {"ip": fppip, "udp": fppudp, "models": fppmodels, "map": fppmap}
    fppparams = createParamsStr(params_dict, verbose)
    request = baseURL + "uploadFPPConfig/" + fppparams
    ("Upload FPP Config to FPP IP:%s udp:%s models:%s map:%s" % (fppip, fppudp, fppmodels, fppmap))
    if (verbose):
       print ("request = ", request)
    (ret_code, status_code, result) = doRequestsGet(request, 900, verbose)
    # Request Error?
    if (ret_code < 0):
       print("Unable to connect to xLights REST API %s" % baseURL)
       print ("ret_code = ", ret_code)
       print ("result = ", result) 
       sys.exit("*** Error in Request to Rest API")       
    # 
    print ("status_code = ", status_code)
    print ("result = ", result)

    return()

###############################
# selectAll                   #
###############################

def selectAll(tree):
    # Iterate over all the root-level items in the treeview.
    for item in tree.get_children():
        select_children(tree, item)
    
def select_children(tree, item):
    # Make sure the item is expanded so the user can see it.
    tree.item(item, open=True)
    
    # Select the current item.
    tree.selection_add(item)
    
    # Select all the children of the current item, if any.
    item_children = tree.get_children(item)
    if item_children:
        for sub_item in item_children:
            select_children(tree, sub_item)
        
###############################
# removeAll                   #
###############################
def removeAll(tree):
    # Iterate over all the root-level items in the treeview.
    for item in tree.get_children():
        remove_children(tree, item)
    
def remove_children(tree, item):
    # Make sure the item is expanded so the user can see it.
    tree.item(item, open=True)
    
    # Remove the current item.
    tree.selection_remove(item)
    
    # Remove all the children of the current item, if any.
    item_children = tree.get_children(item)
    if item_children:
        for sub_item in item_children:
            remove_children(tree, sub_item)
    
#
###############################
# selectedControllers         #
###############################
def selectedControllers(window, tree, baseURL, verbose):
    #
    selected_items = tree.selection()
    if (verbose):
        print(baseURL)
        print (selected_items)
    for i in range(len(selected_items)):
        item_details = tree.item(selected_items[i])
        if (verbose):
            print (item_details)
        item_details_values = item_details.get("values")
        if (verbose):
            print (item_details_values)
    
        # Get Parms    
        fppip = item_details_values[0]
        fppudp = item_details_values[1]
        fppmodel = item_details_values[2]
        fppmap = item_details_values[3]
    
        # Upload FPP Config
        uploadFPPConfig(baseURL, fppip, fppudp, fppmodel, fppmap, verbose)
    
    # Close Window
    window.quit()

###############################
# main                        #
###############################
def main():

    print ("#" *5 + " uploadFPPConfigs Begin")

    cli_parser = argparse.ArgumentParser(prog = 'uploadSequences',
        description = '''%(prog)s is a tool to upload an fpp config with parms defined in a csv formatted input file ,''')
   
    ### Define Arguments    

    cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
        required = True)        

    cli_parser.add_argument('-c', '--closexlights' , help = 'Close xLights', action='store_true',
        required = False)

    cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
        required = False)

    ### Get Arguments
    args = cli_parser.parse_args()
    
    xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
    closexlights = args.closexlights
    verbose = args.verbose

    ### Current Working Directory
    CWD = os.getcwd()
    
    xlightsparmsfilename = "xlightsparms.json"
    ### Load xLights Parms JSON
    xlightsparmsfile = open(xlightsparmsfilename, "r+")
    xlightsparms = json.load(xlightsparmsfile)
    ### Get xLights Parms
    xlightsipaddress = xlightsparms.get("xlightsipaddress")
    xlightsport = xlightsparms.get("xlightsport")
    # Replace xlightsport with real port value
    if (xlightsport == "A"):
        xlightsport = "49913"
    elif (xlightsport == "B"):
        xlightsport = "49914"
    xlightsprogram = xlightsparms.get("xlightsprogram")
	   
    if (verbose):
        print ("xLights Show Folder = %s" % xlightsshowfolder)
        print ("xLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program Folder = %s" % xlightsprogram)
        print ("Close xLights = %s" % closexlights)
        print ("CWD = %s" % CWD)
    
    uploadfppconfigsfilename = "uploadfppconfigs.json"
    # verify upload json file exists
    if not os.path.isfile(uploadfppconfigsfilename):
        print("Error: Upload FPP Config json file not found %s" % uploadfppconfigsfilename)
        sys.exit(-1)
        
    ### load uploadfppconfigs json file 
    uploadfppconfigsfile = open(uploadfppconfigsfilename, "r+")
    uploadfppconfigs = json.load(uploadfppconfigsfile)
    # verify xlights show folder exists
    if not os.path.isdir(xlightsshowfolder):
        print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
        sys.exit(-1)

    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(xlightsshowfolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % xlightsshowfolder)
        sys.exit(-1)

    # verify xlights program file exists
    if not os.path.isfile(xlightsprogram):
        print("Error: xLights Program File not found %s" % xlightsprogram)
        sys.exit(-1)

    # Base URL
    baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
    if (verbose):
        print ("Base URL = %s" % baseURL)

    # Start xLights?
    (ret_code, status_code, result) = startxLights(baseURL, xlightsprogram, verbose)
    # xLights Start Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result)
        sys.exit("*** Error in Request to REST API")

    # Get Current Show Folder
    request = baseURL + "getShowFolder"
    if (verbose):
        print ("##### Get Show Folder")
        print ("request = ", request)    
    (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
    if (ret_code < 0):    
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result)
        sys.exit(-1)
    if (verbose):
        print ("status_code = ", status_code)
        print ("result = ", result)
    getshowfolder = os.path.abspath(result)
    # Change Show Folder?
    if (xlightsshowfolder != getshowfolder):
        request = baseURL + "changeShowFolder?folder=" + re.sub(" ", r"%20", xlightsshowfolder)    
        if (verbose):
            print ("##### Change Show Folder")
            print ("request = ", request)    
        (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
        if (ret_code < 0):    
            print("Unable to connect to xLights REST API %s" % baseURL)
            print ("ret_code = ", ret_code)
            print ("result = ", result)
            sys.exit(-1)
        if (verbose):
            print ("status_code = ", status_code)
            print ("result = ", result)

    # Get Controller IPs 
    request = baseURL + "getControllerIPs" 
    if (verbose):
        print ("##### Get Controller IP Address")
        print ("request = ", request)    
    (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
    if (ret_code < 0):    
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result)
        sys.exit(ret_code)    
    if (verbose):
        print ("status_code = ", status_code)
        print ("result = ", result)

    controllerIPs = ast.literal_eval(result)

    # Compile Searches
    p1 = re.compile(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")

    # Load fpp upload config parms into list
    fppparms_list = []
    fppctllist = uploadfppconfigs.get('controllers')
    if (verbose):
        print (fppctllist)
    for i in range(len(fppctllist)):
        fppctl = fppctllist[i]
        fppip =  fppctl.get("ip")
        if (fppip != None):
            s1 = p1.search(fppip)
            if (not s1):
                sys.exit("*** ERROR Invalid IPv4 Address %s" % fppip)
            if fppip not in controllerIPs:
                sys.exit("*** ERROR Controller IP %s not defined in Xlights" % fppip)
        else:
            sys.exit("*** ERROR Controller IP %s not found" % fppip)
        fppudp = fppctl.get("udp", "none")
        if fppudp not in ["none", "all", "proxy"]:
           print ("*** UDP parm %s invalid on %s changed to default of \"none\"" % (ffpudp, fppip))
        fppmodels = fppctl.get("models", "none")
        if fppmodels not in ["true", "false"]:
            print ("*** Models parm %s invalid on %s changed to default of \"false\"" % (ffpmodels, fppip))
        fppmap = fppctl.get("map", "none")
        if fppmap not in ["true", "false"]:
            print ("*** Map parm %s invalid on %s changed to default of \"false\"" % (fppmap, fppip))
        fppparms_list.append([fppip, fppudp, fppmodels, fppmap])    

    # Upload FPP Configurations Selection Window
    window = Tk()
    window.title('Upload FPP Configurations')
    window.geometry("425x425")

    Label(window, text="Select FPP Configurations to Upload").pack()

    frame = Frame(window)
    frame.pack()
    bottomframe = Frame(window)
    bottomframe.pack( side = BOTTOM )

        # Set Style Theme
    s = ttk.Style()
    s.theme_use('clam')

    # Add a Treeview widget
    tree = ttk.Treeview(window, column=("IP", "udp", "models", "map"), show='headings', height=10)
    tree.pack(side ="left")
    
    tree.column("# 1", width = 100, anchor=CENTER)
    tree.heading("# 1", text= "IP")
    tree.column("# 2", width = 100, anchor=CENTER)
    tree.heading("# 2", text="udp")
    tree.column("# 3", width = 100, anchor=CENTER)
    tree.heading("# 3", text="models")
    tree.column("# 4", width = 100, anchor=CENTER)
    tree.heading("# 4", text="maps")

    # add a scrollbar
    vscrollbar = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    tree.configure(yscroll=vscrollbar.set)
    vscrollbar.pack(side ='right', fill ='x')

    # Get data
    for ctl_fppparms in fppparms_list:
        tree.insert('', END, values=ctl_fppparms)   
    tree.pack()

    # define buttons
    allButton = Button(bottomframe, text="Select ALL", command = partial(selectAll, tree)).pack(side = LEFT, padx=10)
    clearButton = Button(bottomframe, text="Clear All", command = partial(removeAll, tree)).pack(side = LEFT, padx=10)
    fppuploadButton = Button(bottomframe, text="FPP Upload", command = lambda: selectedControllers(window, tree, baseURL, verbose)).pack(side = LEFT, padx=10)
    cancelButton = Button(bottomframe, text="Cancel", command = window.destroy).pack(side = LEFT, padx=10)
    
    window.mainloop()
    
    ### Close xLights
    if (closexlights):
        request = baseURL + "closexLights"
        if (verbose):
            print("##### closexLights")
            print("request = ", request)
        (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
        if (ret_code < 0):
            print("Unable to close xLights %s" % baseURL)
            print("ret_code = ", ret_code)
            print("result = ", result)
            sys.exit(ret_code)
    print ("#" *5 + " uploadFPPConfigs End")

if __name__ == "__main__":
    main()