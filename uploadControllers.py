#!/usr/bin/env python

# Name: uploadControllers.py
# Purpose: Upload selected controller configurations
# Author: Bill Jenkins
# Version: v2.0
# Date: 08/15/2023

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
import csv
import ast
import json
###########################
# From Imports            #
###########################
from functools import partial
from tkinter import *
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
# startxLights                #
###############################

def startxLights(baseURL, xlightsprogramfile, verbose):

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
                    print ("ret_code = ", ret_code)
                    print ("status_code = ", status_code)
                    print ("result = ", result)
            # REST API Connection Error?
            case -2:
                if (not started):
                    # Start xLights
                    cmd = "\"" + xlightsprogramfile + "\""
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
# createParamsStr             #
###############################

def createParamsStr(params_dict, verbose): 

    if (verbose):
        print ("params_dict = %s" % params_dict)

    params_str = ""
    params_ctr = 0
    params_len = len(params_dict)

    for params_key, params_value in params_dict.items():
        if (verbose):
            print ("params_key = %s" % params_key)
            print ("params_value = %s" % params_value)
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
# uploadController            #
###############################
def uploadController(baseURL, uploadip, verbose):

    params_dict =  {"ip": str(uploadip)}
    uploadparams = createParamsStr(params_dict, verbose)
    request = baseURL + "uploadController/" + uploadparams  
    print ("Upload configuration to controller:%s" % (uploadip)) 
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

def selectAll(lb):
    lb.select_set(0, END)

###############################
# clearAll                    #
###############################

def clearAll(lb):
    lb.select_clear(0, END)

###############################
# selectedControllers         #
###############################
def selectedControllers(window, listCTL, baseURL, verbose):
    #
    if (verbose):
        print(listCTL)
        print(baseURL)
    Controllers = []
    ctlSel = listCTL.curselection()
    for i in ctlSel:
        s1 = str(listCTL.get(i))
        s2 = s1.split(" ")
        uploadIP = s2[0]
        uploadController(baseURL, uploadIP, verbose)
    # Close Window
    window.quit()

###############################
# main                        #
###############################
def main():

    print ("#" *5 + " uploadControllers Begin")

    cli_parser = argparse.ArgumentParser(prog = 'uploadController',
        description = '''%(prog)s is a tool to upload a controller configuration from the conroller IPs in xLights,''')
   
    ### Define Arguments    

    cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
        required = True)        
    
    cli_parser.add_argument('-i', '--xlightsipaddress', help = 'xLights REST API IP Address', default = "127.0.0.1",
        required = False)

    cli_parser.add_argument('-p', '--xlightsport', help = 'xLights REST API Port', default = "49913", choices = ["49913", "49914"],
        required = False)

    cli_parser.add_argument('-x', '--xlightsprogramfolder', help = 'xLights Program Folder', default = "c:\\program files\\xlights",
        required = False)
    cli_parser.add_argument('-c', '--closexlights' , help = 'Close xLights', action='store_true',
        required = False)
    cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
        required = False)

    ### Get Arguments
    args = cli_parser.parse_args()
    
    xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
    xlightsipaddress = args.xlightsipaddress
    xlightsport = args.xlightsport
    xlightsprogramfolder = os.path.abspath(args.xlightsprogramfolder)
    closexlights = args.closexlights
    verbose = args.verbose
    if (verbose):
        print ("xLights Show Folder = %s" % xlightsshowfolder)
        print ("xLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program Folder = %s" % xlightsprogramfolder)
        print ("Close xLights = %s" % closexlights)

    # verify xlights show folder exists
    if not os.path.isdir(xlightsshowfolder):
        print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
        sys.exit(-1)

    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(xlightsshowfolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % xlightsshowfolder)
        sys.exit(-1)

    # verify xlights program file exists
    xlightsprogramfile = xlightsprogramfolder + "\\xlights.exe"
    if not os.path.isfile(xlightsprogramfile):
        print("Error: xLights Program File not found %s" % xlightsprogramfile)
        sys.exit(-1)

    # Base URL
    baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
    if (verbose):
        print ("Base URL = %s" % baseURL)

    # Start xLights?
    (ret_code, status_code, result) = startxLights(baseURL, xlightsprogramfile, verbose)
    # xLights Start Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result)
        sys.exit(-1)
        
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

    # Get Controllers
    request = baseURL + "getControllers"
    result = []
    if (verbose):
        print ("##### Get Controllers")
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
    controllers = json.loads(result)
    # Upload Controller Selection Window
    window = Tk()
    window.title('Upload Controllers')
    window.geometry("400x520")

    Label(window, text="Upload Controllers Configuration").pack()

    frame = Frame(window)
    frame.pack()

    listCTL = Listbox(frame, width=50, height=20, font=("Helvetica", 12), selectmode = "multiple")
    listCTL.pack(padx = 10, pady = 10, expand = YES, fill = "both")

    scrollbar = Scrollbar(frame, orient="vertical")
    scrollbar.config(command=listCTL.yview)
    scrollbar.pack(side="right", fill="y")

    listCTL.config(yscrollcommand=scrollbar.set)

    for i in range(len(controllers)):
        dCtl = {}
        dCtl = controllers[i]
        nameCtl = dCtl.get('name')
        ipCtl = dCtl.get('ip')
        listCTL.insert(END, ipCtl + "     " + nameCtl)


    allButton = Button(window, text="Select ALL", command = partial(selectAll, listCTL)).pack(side = LEFT, padx=10)
    clearButton = Button(window, text="Clear All", command = partial(clearAll, listCTL)).pack(side = LEFT, padx=10)
    uploadButton = Button(window, text="Upload", command = lambda: selectedControllers(window, listCTL, baseURL, verbose)).pack(side = LEFT, padx=10)
    cancelButton = Button(window, text="Cancel", command = window.destroy).pack(side = LEFT, padx=10)

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
    print ("#" *5 + " uploadControllers End")

if __name__ == "__main__":
    main()