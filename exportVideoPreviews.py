#!/usr/bin/env python

# Name: exportVideoPreviews.py
# Purpose: export video preview for sequences selected in a show folder and sub folders
# Author: Bill Jenkins
# Version: v2.0
# Date: 08/15/2023

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
# exportVideoPreview          #
###############################

def exportVideoPreview(baseURL, fullsequence, xlightsshowfolder, outputfolder, verbose):
    # Open Sequence
    sequence = os.path.basename(fullsequence).split('/')[-1]
    request = baseURL + "openSequence/" + re.sub(" ", r"%20", fullsequence)
    if (verbose):
        print ("##### Open Sequence %s" % sequence)
        print ("request = ", request)
    (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
    # Request Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)
        print ("ret_code = ", ret_code)
        print ("result = ", result) 
        sys.exit(ret_code)
    if (verbose):
        print ("status_code = ", status_code)
        print ("result = ", result)
        
    # Full Output Folder
    if (outputfolder == "DEFAULT"):
        outputfolder = xlightsshowfolder + "\\exportVideoPreview"

    # Output Folder does not exist?
    outputfolder = os.path.abspath(outputfolder)
    if not os.path.isdir(outputfolder):
        # Make Output Folder
        os.mkdir(outputfolder)

    # outputfile
    outputfile = outputfolder + "\\" + re.sub(".xsq", ".mp4", sequence)
    outputfile = re.sub(" ", r"%20", outputfile)
    # Export Video Preview
    request = baseURL + "exportVideoPreview?filename=" + outputfile 
    print ("##### Export Video Preview %s" % sequence)
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
                
    # Close Sequence
    request = baseURL + "closeSequence"
    if (verbose):
        print ("##### Close Sequence %s" % sequence)
        print ("request = ", request)
    (ret_code, status_code, result) = doRequestsGet(request, 30, verbose)
    # Request Error?
    if (ret_code < 0):
        print("Unable to connect to xLights REST API %s" % baseURL)        
        print ("ret_code = ", ret_code)
        print ("result = ", result) 
        sys.exit(ret_code)
    if (verbose):
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

def selectSequences(window, listSEQ, baseURL, xlightsshowfolder, outputfolder, verbose):
    if (verbose):
        print(listSEQ)
        print(baseURL)
    seqSel = listSEQ.curselection()
    for i in seqSel:
        fullsequence = str(listSEQ.get(i))
        exportVideoPreview(baseURL, fullsequence, xlightsshowfolder, outputfolder, verbose)
    # Close Window
    window.quit()

###############################
# main                        #
###############################

def main():

    print ("#" *5 + " exportVideoPreviews Begin")

    cli_parser = argparse.ArgumentParser(prog = 'exportVideoPreviews',
        description = '''%(prog)s is a tool to perform an export video preview on all xLights sequences in a show directory,''')
    
    ### Define Arguments    

    cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
        required = True)

    cli_parser.add_argument('-i', '--xlightsipaddress', help = 'xLights REST API IP Address', default = "127.0.0.1",
        required = False)

    cli_parser.add_argument('-p', '--xlightsport', help = 'xLights REST API Port', default = "49913", choices = ["49913", "49914"],
        required = False)

    cli_parser.add_argument('-x', '--xlightsprogramfolder', help = 'xLights Program Folder', default = "c:\\program files\\xlights",
        required = False)

    cli_parser.add_argument('-o', '--outputfolder', help = 'Output Folder', default = "DEFAULT",
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
    outputfolder = args.outputfolder
    closexlights = args.closexlights
    verbose = args.verbose
    if (verbose):
        print ("xLights Show Folder = %s" % xlightsshowfolder)
        print ("xLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program Folder = %s" % xlightsprogramfolder)
        print ("Output Folder = %s" % outputfolder)
        print ("Close xLights = %s" % closexlights)
    
    # Base URL
    baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
    if (verbose):
        print ("Base URL = %s" % baseURL)

    # Verify Show Folder
    if not os.path.isdir(xlightsshowfolder):
        print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
        sys.exit(-5)

    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(xlightsshowfolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % xlightsshowfolder)
        sys.exit(-1)

    # verify xlights program file exists
    xlightsprogramfile = xlightsprogramfolder + "\\xlights.exe"
    if not os.path.isfile(xlightsprogramfile):
        print("Error: xLights Program File not found %s" % xlightsprogramfile)
        sys.exit(-1)

    # Start xLights?
    (ret_code, status_code, result) = startxLights(baseURL, xlightsprogramfile, verbose)
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

    # Export Video Preview Selection Window
    window = Tk()
    window.title('Export Video Previews')
    window.geometry("520x520")

    Label(window, text="Select Sequences to Export Video Preview").pack()

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
    
    allButton = Button(window, text="Select ALL", command = partial(selectAll, listSEQ)).pack(side = LEFT, padx=10)
    clearButton = Button(window, text="Clear All", command = partial(clearAll, listSEQ)).pack(side = LEFT, padx=10)
    exportButton = Button(window, text="Export", command = lambda: selectSequences(window, listSEQ, baseURL, xlightsshowfolder, outputfolder, verbose)).pack(side = LEFT, padx=10)
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

    print ("#" *5 + " exportVideoPreviews End")

if __name__ == "__main__":
    main()