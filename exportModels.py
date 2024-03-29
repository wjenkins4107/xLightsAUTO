#!/usr/bin/env python

# Name: exportModels.py
# Purpose: export models in a show folder to an excel file
# Author: Bill Jenkins
# Version: v2.1
# Date: 08/24/2023

###############################
# Imports                     #
###############################

import argparse
import sys
import subprocess
import os
import time
import re
import requests
import json
import datetime

###########################
# From Imports            #
###########################
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

###############################
# exportModels                #
###############################

def exportModels(baseURL, xlightsshowfolder, exportfolder, exportfile, verbose):
 
    # Output Folder
    if (exportfolder == "DEFAULT"):
        exportfolder = xlightsshowfolder + "\\exportModels"
    # Output Folder does not exist?
    exportfolder = os.path.abspath(exportfolder)
    if not os.path.isdir(exportfolder):
        # Make Output Folder
        os.mkdir(exportfolder)
    # Export File
    if (exportfile == "DEFAULT"):
        # Get Current Date Time
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        exportfile = "exportModels_" + timestamp + ".xlsx" 
    else:    
        exportfile = exportfolder + "\\" + exportfile + ".xlsx" 
    request = baseURL + "exportModelsCSV?filename=" + re.sub(" ", r"%20", exportfile) 
    print ("##### Export Models for Show Folder %s " % xlightsshowfolder)
    print ("request = ", request)    
    (ret_code, status_code, result) = doRequestsGet(request, 900, verbose)
    # Request Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result) 
        sys.exit(ret_code)        
    # 
    print ("status_code = ", status_code)
    print ("result = ", result)

    return()

###############################
# main                        #
###############################

def main():

    print ("#" *5 + " exportModels Begin")

    cli_parser = argparse.ArgumentParser(prog = 'exportModels',
        description = '''%(prog)s is a tool to perform a export models to an excel file,''')
    
    ### Define Arguments    

    cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
        required = True)

    cli_parser.add_argument('-o', '--exportfolder', help = 'Excel Export Folder', default = "DEFAULT",
        required = False)

    cli_parser.add_argument('-f', '--exportfile', help = 'Excel Export Models File', default = "DEFAULT",
        required = False)

    cli_parser.add_argument('-c', '--closexlights' , help = 'Close xLights', action='store_true',
        required = False)

    cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
        required = False)

    ### Get Arguments
    args = cli_parser.parse_args()
    

    xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
    exportfolder = args.exportfolder
    exportfile = args.exportfile
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
        print ("XLights Show Folder = %s" % xlightsshowfolder)
        print ("XLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program = %s" % xlightsprogram)
        print ("Output Folder = %s" % exportfolder)
        print ("Excel Export Models File Name = %s" % exportfile)
        print ("Close xLights = %s" % closexlights)
        print ("CWD = %s" % CWD)
        
    # Base URL
    baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
    if (verbose):
        print ("Base URL = %s" % baseURL)

    # Verify Show Folder
    if not os.path.isdir(xlightsshowfolder):
        print("Error: Show Folder not found %s" % xlightsshowfolder)
        sys.exit(-5)

    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(xlightsshowfolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % xlightsshowfolder)
        sys.exit(-1)

    # verify xlights program file exists
    if not os.path.isfile(xlightsprogram):
        print("Error: xLights Program File not found %s" % xlightsprogram)
        sys.exit(-1)

    # Start xLights?
    (ret_code, status_code, result) = startxLights(baseURL, xlightsprogram, verbose)
    # xLights Start Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result)
        sys.exit(ret_code)
            
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


    exportModels(baseURL, xlightsshowfolder, exportfolder, exportfile, verbose)

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

    print ("#" *5 + " exportModels End")

if __name__ == "__main__":
    main()