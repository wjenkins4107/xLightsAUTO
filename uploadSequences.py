#!/usr/bin/env python

# Name: uploadSequences.py
# Purpose: Upload a sequence in a show folders and sub folders to players defined in  a csv formatted input file 
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
import urllib.parse

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

##############################
# uploadSequence             #
##############################

def uploadSequence(baseURL, uploadip, uploadmedia, uploadformat, uploadseq, verbose):

    
    params_dict =  {"ip": uploadip, "media": uploadmedia, "format": uploadformat, "seq": uploadseq}
    uploadparams = createParamsStr(params_dict, verbose)
    request = baseURL + "uploadSequence/" + uploadparams  
    print ("Upload Sequence:%s to Player IP:%s" % (uploadseq, uploadip)) 
    print ("   Media:%s Format:%s" % (uploadmedia, uploadformat))
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
# selectSequences             #
###############################

def selectSequences(window, listSEQ, baseURL, uploadfileparms_list, verbose):
    if (verbose):
        print(listSEQ)
        print(baseURL)
    seqSel = listSEQ.curselection()
    for i in seqSel:
        uploadseq = str(listSEQ.get(i))
        for j in range(len(uploadfileparms_list)):
            uploadip = uploadfileparms_list[j][0]
            uploadmedia = uploadfileparms_list[j][1]
            uploadformat = uploadfileparms_list[j][2]
            # Upload Sequence
            uploadSequence(baseURL, uploadip, uploadmedia, uploadformat, uploadseq, verbose) 
    # Close Window
    window.quit()
###############################
# main                        #
###############################
def main():

    print ("#" *5 + " uploadSequences Begin")

    cli_parser = argparse.ArgumentParser(prog = 'uploadSequences',
        description = '''%(prog)s is a tool to upload a sequence in a show folder and sub folders to players defined in  a csv formatted input file ,''')
   
    ### Define Arguments    

    cli_parser.add_argument('-u', '--uploadcsvfile', help = 'Upload CSV File',
        required = True)

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
    
    uploadcsvfile = os.path.abspath(args.uploadcsvfile)
    xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
    xlightsipaddress = args.xlightsipaddress
    xlightsport = args.xlightsport
    xlightsprogramfolder = os.path.abspath(args.xlightsprogramfolder)
    closexlights = args.closexlights
    verbose = args.verbose
    if (verbose):
        print ("Upload Sequence CSV File = %s" % uploadcsvfile)
        print ("xLights Show Folder = %s" % xlightsshowfolder)
        print ("xLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program Folder = %s" % xlightsprogramfolder)
        print ("Close xLights = %s" % closexlights)
    
    # verify upload file exists
    if not os.path.isfile(uploadcsvfile):
        print("Error: Upload Sequence CSV file not found %s" % uploadcsvfile)
        sys.exit(-1)
        
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
    controllerIPs = result
    # Compile Searches
    p1 = re.compile(r"^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$")
    # Load upload file parms into list
    uploadfileparms_list = []
    with open(uploadcsvfile) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if (verbose):
               print ("Upload parms %s" % row)
            rowstr = str(row)
            if (rowstr[2] != "#"):
                # Valid Number of Parms?
                if (len(row) == 3):
                    uploadip = row[0]
                    s1 = p1.search(uploadip)
                    if (not s1):
                        sys.exit("*** ERROR Invalid IPv4 Address %s" % uploadip)
                    if uploadip not in controllerIPs:
                        sys.exit("*** ERROR Controller IP %s not defined in Xlights" % uploadip)
                    uploadmedia = row[1]
                    if uploadmedia not in ["true","false"]:
                        print ("*** Media parm invalid on %s changed to default of \"false\"" % uploadip)
                        uploadmedia = "false"
                    uploadformat = row[2]
                    if uploadformat not in ["v1", "v2std", "v2zlib", "v2uncompressedsparse", "v2uncompressed", "v2stdsparse", "v2zlibsparse"]:
                        print ("*** Format parm invalid on %s changed to default of \"v2std\"" % uploadip)
                        uploadformat = "v2std"
                    uploadfileparms_list.append([uploadip, uploadmedia, uploadformat])
                    if (verbose):
                        print (uploadip)
                        print (uploadmedia)
                        print (uploadformat)
                else:
                    print ("*** Invalid number of upload parms %s" % row)
    # Build Sequence List
    SEQlist = []
    ### OS Walk Show Folder Recursively
    for root, dir, files in os.walk(xlightsshowfolder):
        for file in files:
            # xLights Sequence File?
            if (file.endswith(".xsq")):
                fullsequence = os.path.join(root, file)
                found = fullsequence.find("Backup\\")
                # xLights Sequence File not in the Backup folder?
                if (found < 0):
                    sequence = file
                    if (verbose):
                        print ("sequence = ", sequence)
                        print ("fullsequence = ", fullsequence)
                    SEQlist.append(fullsequence)

    # Upload Sequences Selection Window
    window = Tk()
    window.title('Upload Sequences')
    window.geometry("520x520")

    Label(window, text="Select Sequences to Upload").pack()

    frame = Frame(window)
    frame.pack()

    listSEQ = Listbox(frame, width=50, height=20, font=("Helvetica", 12), selectmode = "multiple")
    listSEQ.pack(padx = 10, pady = 10, expand = YES, fill = "both")

    # Vertical Scrollbar
    scroll_V = Scrollbar(frame, orient="vertical")
    scroll_V.config(command=listSEQ.yview)
    scroll_V.pack(side="right", fill="y")
    # Horizontal Scrollbar
    scroll_H = Scrollbar(frame, orient="horizontal")
    scroll_H.config(command=listSEQ.xview)
    scroll_H.pack(side= BOTTOM, fill= "x")
    # List Config
    listSEQ.config(yscrollcommand=scroll_V.set, xscrollcommand=scroll_H.set)
    # Load Sequence List
    for i in range(len(SEQlist)):
        listSEQ.insert(END, SEQlist[i])
    
    allButton = Button(window, text="Select All", command = partial(selectAll, listSEQ)).pack(side = LEFT, padx=10)
    clearButton = Button(window, text="Clear All", command = partial(clearAll, listSEQ)).pack(side = LEFT, padx=10)
    uploadButton = Button(window, text="Upload", command = lambda: selectSequences(window, listSEQ, baseURL, uploadfileparms_list, verbose)).pack(side = LEFT, padx=10)
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

    print ("#" *5 + " uploadSequences End")

if __name__ == "__main__":
    main()