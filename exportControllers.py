#!/usr/bin/env python

# Name: exportControllers.py
# Purpose: Get xLights Networks XML and RestAPI GetControllers Information and export to excel workbook
# Author: Bill Jenkins
# Version: v1.0
# Date: 08/24/2023

#######################
### Imports         ###
#######################

import argparse
import xml.etree.ElementTree as ET
import sys
import subprocess
import os
import platform
import re
import requests
import json
import datetime
import time
import xlsxwriter

#######################
### Imports From    ###
#######################
from istools import *
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
# createParamsStr              #
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

#########################
### wsOutputRow       ###
#########################
def wsOutputRow(worksheet, wsRow, wsCol, wsCellList, wsFmtList, wbFmts, verbose):

    if (verbose):
        print ("wsOutput: (000) *** Begin ***")
          # Workbook Format for Cell

    for wsCellwsCol, wsCell in enumerate(wsCellList):
        if (verbose):
            print ("wsOutput: (010) , wsCellList[%s] = %s, wsRow = %s, wsCol = %s" % (wsCellwsCol, wsCell, wsRow, wsCol))
        # Workbook Format?
        wbFmt = wbFmts.get(wsFmtList[wsCol])
        # Number Found?
        (NumberFound, Number) = isnumber(wsCell)
        if (NumberFound):
         #   (NumberFound, Number) = isint(wsCell)
         #   if (NumberFound):
         #       wbFmt = wbFmts.get('intLeft')
         #   else:
         #       wbFmt = wbFmts.get('floatLeft')
            worksheet.write_number(wsRow, wsCol, Number, wbFmt)       
        else:    
            worksheet.write_string(wsRow, wsCol, wsCell, wbFmt)       
        # Increment Column
        wsCol += 1
    if (verbose):
        print ("wsOutput: (000) *** End ***")

#########################
### createWorksheet   ###
#########################

def createWorksheet(workbook, worksheetname, wspaper, wsorientation, wsmleft, wsmright, wsmtop, wsmbottom, wsrepeatrow, wsprintscale, wstitle1, wstitle2, wbHeaderImage, verbose):

    if (verbose):
        print ("createWorksheet: (000) *** Begin ***")

    # Add Worksheet
    worksheet = workbook.add_worksheet(worksheetname)

    # Worksheet Page Setup

    # Set Paper Type
    (valid, number) = isint(wspaper)
    if (valid):
        worksheet.set_paper(number)
    else:
        worksheet.set_paper(0)
    
    # Set Orientation
    if (wsorientation == "portrait"):
        worksheet.set_portrait()
    else:
        worksheet.set_landscape()

    # Set Margins
    (valid, wsmleft) = isfloat(wsmleft)
    if (valid):
        wsmleft == number
    else:
        wsmleft = 0.7
    (valid, number) = isfloat(wsmright)
    if (valid):
        wsmright = number
    else:
        wsmright = 0.7
    (valid, wsmtop) = isfloat(wsmtop)
    if (valid):
        wsmtop = number
    else:    
        wsmtop = 1.25
    (valid, bottom) = isfloat(wsmbottom)
    if (valid):
        wsmbottom = number
    else:
        wsmright = 0.7
    worksheet.set_margins(wsmleft, wsmright, wsmtop, wsmbottom)

    # Set Repeat Row
    (valid, number) = isint(wsrepeatrow)
    if (valid):
        worksheet.repeat_rows(number)

    # Set Print Scale
    (valid, number) = isint(wsprintscale)
    if (valid):
        wsprintscale = number
    else:
        wsprintscale = 100
    worksheet.set_print_scale(wsprintscale)

    # Init Header & Footer
    header = '&L&"Calibri,Bold"&D\n&T' + '&C&"Calibri,Bold"' + wstitle1 + '\n' + wstitle2 + '&R&[Picture]'
    footer = '&CPage &P of &N'

    # Set Header & Footer
    worksheet.set_header(header, {'image_right': wbHeaderImage})
    worksheet.set_footer(footer)

    if (verbose):
        print ("createWorksheet: (999) *** End ***")

    return(worksheet)
    
#########################
### createWorkbook    ###
#########################

def createWorkbook(workbookfile, dwbFmts, verbose):

    if (verbose):
        print ("createWorkbook: (000) *** Begin ***")

    # Create Workbook
    workbook = xlsxwriter.Workbook(workbookfile)
    # Set Workbook Properties
    workbook.set_properties({
        'title': 'Export Controllers',
        'subject': 'xLights Controllers',
        'author': 'Bill Jenkins',
        'manager': '',
        'company': '',
        'category': 'documentation',
        'keywords': 'xlights, controllers, documentation',
        'comments': ''})

    # Create Workbook Formats Dictionary
    dwbFmtsKeys = list(dwbFmts.keys())
    if (verbose):
        print (dwbFmtsKeys)
    wbFmts = {}
    for i in range(len(dwbFmtsKeys)):
        wbFmtKey = dwbFmtsKeys[i]
        wbFmtValue = dwbFmts.get(dwbFmtsKeys[i])
        if (verbose):
            print ("wbFmtKey = ", wbFmtKey, type(wbFmtKey), "wbFmtValue =", wbFmtValue, type(wbFmtValue))
        if (dwbFmtsKeys[i] != "wbHeaderImage"):
            wbFmts[wbFmtKey] = workbook.add_format(wbFmtValue)
        else:
            wbHeaderImage = wbFmtValue
    
    if (verbose):
        print(wbFmts)
        
    if (verbose):
        print ("createWorkbook: (999) *** End ***")

    return(workbook, wbFmts, wbHeaderImage)

###############################
# nested_dict_pairs_iterator  #
###############################

def nested_dict_pairs_iterator(dict_obj):
    # Iterate over all key-value pairs of dict argument
    for key, value in dict_obj.items():
        # Check if value is of dict type
        if isinstance(value, dict):
            # If value is dict then iterate over all its values
            for pair in  nested_dict_pairs_iterator(value):
                yield (key, *pair)
        else:
            # If value is not dict type then yield the value
            yield (key, value)

###############################
### exportControllers  ###
###############################
def exportControllers(baseURL, xlightsshowfolder, xlightsnetworksxmlfull, workbook, wbFmts, wbHeaderImage, verbose):
    if (verbose):
        print ("exportControllers: (000) *** Begin ***")

    #
    # List Dictionary wbFmts
    wbFmtsKeys = list(wbFmts.keys())
    if (verbose):
        print ("wbFmtsKeys =", wbFmtsKeys)
    # 

    #
    ###################################################################
    # Get Controllers Information from xLights Networks Xml File
    ###################################################################
    #

    # Networks XML Tree
    xmlNetTree = ET.parse(xlightsnetworksxmlfull)
    # Networks XML Root
    xmlNetRoot = xmlNetTree.getroot()
    # Get Network XML Root Attributes
    xmlNetKeys = ([*xmlNetRoot.attrib])
    #   
    for Controller in xmlNetRoot.findall('Controller'):
        #
        # Create Worksheet for Controller
        # 
        ControllerName = Controller.get("Name")
        worksheetname = ControllerName
        wspaper = 1
        wsorientation = "landscape"
        wsmleft = 0.7
        wsmright = 0.7
        wsmtop = 1.5
        wsmbottom = 0.7
        wsrepeatrow = "NONE"
        wsprintscale = 100
        wstitle1 = "Controller: " + ControllerName
        wstitle2 = "Show Folder: " + xlightsshowfolder
        wsPageBreak = []
        worksheet = createWorksheet(workbook, worksheetname, wspaper, wsorientation, wsmleft, wsmright, wsmtop, wsmbottom, wsrepeatrow, wsprintscale, wstitle1, wstitle2, wbHeaderImage, verbose)           
        
        # Init Worksheet Row & Column
        wsRow = 0
        wsCol = 0
        # Init Worksheet Column & Format List
        wsColList = []
        wsFmtList = []
        # 
        wsColList.append("Networks XML Controller Information")
        wsFmtList.append("boldLeft")
        wsOutputRow(worksheet, wsRow, wsCol, wsColList, wsFmtList, wbFmts, verbose)
        wsColList = []
        wsFmtList = []
        wsRow += 1
        wsCol = 0

        # Get Controller Keys & Value
        ControllerKeyList = ([*Controller.attrib])
        for i in range(len(ControllerKeyList)):
            ControllerValue = Controller.get(ControllerKeyList[i])
            #
            # Build Worksheet Row
            #
            # Append Label to Worksheet Column List
            wsColList.append(ControllerKeyList[i])
            # Append Label Format           
            wsFmtList.append("boldLeft")
            # Append Value to Worksheet Column List     
            wsColList.append(ControllerValue)
            # Append Value Format            
            wsFmtList.append("strLeft")
                
            # Set Column to 0
            wsCol = 0
            # Worksheet Output Row
            wsOutputRow(worksheet, wsRow, wsCol, wsColList, wsFmtList, wbFmts, verbose)
            # Increment Row
            wsRow += 1
            # Clear Worksheet Column, Format & Type List
            wsColList = []
            wsFmtList = []

        #
        # Get Controllers Information from xLights REST API getControllers
        #
        request = baseURL + "getControllers"
        if (verbose):
            print ("##### Get Controllers %s" % request)
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
        # getControllers result
        getControllers = json.loads(result)
        if (verbose):
            print ("Controllers Length = ", len(getControllers))
        # Increment Row
        wsRow += 1
        wsCol = 0
        # Clear Worksheet Column, Format & Type List
        wsColList = []
        wsFmtList = []
        #
        wsColList.append("REST API getControllers Information")
        wsFmtList.append("boldLeft")
        wsOutputRow(worksheet, wsRow, wsCol, wsColList, wsFmtList, wbFmts, verbose)
        wsColList = []
        wsFmtList = []
        # Increment Row
        wsRow += 1
        wsCol = 0       
        #        
        for i in range(len(getControllers)):
            if (verbose):
                print (getControllers[i])
            # getCtlName
            getCtlName = getControllers[i].get("name")
            if (ControllerName == getCtlName):
                #Loop through all key-value pairs of a nested dictionary
                for dictPair in nested_dict_pairs_iterator(getControllers[i]):
                    dictPairType = type(dictPair)
                    lendictPair = len(dictPair)
                    if (verbose):
                        print ("dictPairType =", dictPairType)
                        print("dictPair =", dictPair)
                        print ("lendictPair =", lendictPair)
                    wsColList = []
                    wsFmtList = []
                    # List Value?
                    if (type(dictPair[-1]) == list):
                        ListFound = True
                        ListdictPair = dictPair[-1]
                    else:
                        ListFound = False
                        ListdictPair = []
                    if not (ListFound):
                        wsCollList = []
                        wsFmtList = []
                        wsCol = 0
                        iSTOP = lendictPair
                        for i in range(iSTOP):
                            if (i < iSTOP - 1): 
                                wsColList.append(dictPair[i])
                                wsFmtList.append("boldLeft")
                            else:
                                wsColList.append(dictPair[i])
                                wsFmtList.append("strLeft")            
                        # Output Worksheet Row
                        wsOutputRow(worksheet, wsRow, wsCol, wsColList, wsFmtList, wbFmts, verbose)
                        wsRow += 1
                    else:
                        wsCollList = []
                        wsFmtList = []
                        wsCol = 0                          
                        iSTOP = lendictPair - 1      
                        for i in range(iSTOP):
                            wsColList.append(dictPair[i])
                            wsFmtList.append("boldLeft")                          
                        jSTOP = len(ListdictPair)
                        for j in range(jSTOP):
                            if (j < 1):
                                wsColList.append(ListdictPair[j])
                                wsFmtList.append("strLeft")
                            else:    
                                wsColList[-1] = (ListdictPair[j])
                                wsFmtList[-1] = ("strLeft")        
                            # Output Worksheet Row
                            wsCol = 0
                            wsOutputRow(worksheet, wsRow, wsCol, wsColList, wsFmtList, wbFmts, verbose)
                            wsRow += 1
        # Autofit Controller Worksheet
        worksheet.autofit()

    if (verbose):
       print ("exportControllers: (999) *** End ***")


#########################
### main              ###
#########################

def main():


    print ("*" * 50)
    print ("main: (000) *** Export Controllers Begin ***")

    cli_parser = argparse.ArgumentParser(
    prog = 'xlDoc',
    description = '''%(prog)s is a tool to create a workbook file from a show folder.''')

    ### Define Arguments

    cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder - Required',
        required = True)

    cli_parser.add_argument('-c', '--closexlights' , help = 'Close xLights - Optional', action='store_true',
        required = False)

    cli_parser.add_argument('-wbfmts', '--wbFmtsFileName', help = 'Workbook Formats JSON File - Optional', default = "wbFmts.json",
        required = False)

    cli_parser.add_argument('-wbname', '--wbName', help = 'Excel Workbook Name - Optional', default = "DEFAULT",
        required = False)        
        
    cli_parser.add_argument('-v', '--verbose', help = 'Verbose logging - Optional', action='store_true',
        required = False)

    ### Get Arguments

    args = cli_parser.parse_args()
    xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
    closexlights = args.closexlights
    wbFmtsFileName = args.wbFmtsFileName
    wbName = args.wbName
    verbose = args.verbose
    
    ### Current Working Directory
    CWD = os.getcwd()
    
    xlightsparmsfilename = "xlightsparms.json" 
    # Verify xLights Parms JSON File
    if not os.path.isfile(xlightsparmsfilename):
        print("Error: xLights Parms JSON File not found %s" % xlightsparmsfilename)
        sys.exit(-1)

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
    xlightsnetworksxmlfile = xlightsparms.get("xlightsnetworksxmlfile")

    ### Verbose Logging?
    if (verbose):
        print ("xLights Show Folder = %s" % xlightsshowfolder)
        print ("xLights IP Address = %s" % xlightsipaddress)
        print ("xLights Port = %s" % xlightsport)
        print ("xLights Program = %s" % xlightsprogram)
        print ("xLights Networks XML File = %s" % xlightsnetworksxmlfile)
        print ("Close xLights = %s" % closexlights)
        print ("wbFmtsFileName = %s" % wbFmtsFileName)
        print ("wbName = %s" % wbName)
        print ("CWD = %s" % CWD)
        

    # Base URL
    baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
    if (verbose):
        print ("Base URL = %s" % baseURL)
        
    # Verify Show Folder
    if not os.path.isdir(xlightsshowfolder):
        print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
        sys.exit(-1)
    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(xlightsshowfolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % xlightsshowfolder)
        sys.exit(-1)
        
    # Verify Network XML File
    xlightsnetworksxmlfull = xlightsshowfolder + "\\" + xlightsnetworksxmlfile
    if not os.path.isfile(xlightsnetworksxmlfull):
        print("Error: xLights Networks XML File not found %s" % xlightsnetworksxmlfull)
        sys.exit(-1)

    # Verify wbFmtsFileName
    if not os.path.isfile(wbFmtsFileName):
        print("Error: dictwbFmtsFile not found %s" % wbFmtsFileName)
        sys.exit(-1)
    
    # Load Workbook Formats JSON File
    dwbFmtsFile = open(wbFmtsFileName, "r+")
    dwbFmts = json.load(dwbFmtsFile)
    if (verbose):
        for dictPair in nested_dict_pairs_iterator(dwbFmts):
            dictPairType = type(dictPair)
            dictPairLen = len(dictPair)
            if (verbose):
                print ("dictPairType =", dictPairType)
                print ("dictPairLen =", dictPairLen)
                print("dictPair =", dictPair)    
    
    # verify xlights program file exists
    if not os.path.isfile(xlightsprogram):
        print("Error: xLights program not found %s" % xlightsprogram)
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

    # Get Current Date Time
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # Workbook Name
    if (wbName == "DEFAULT"):
        workbookfile = "exportControllers_" + timestamp + ".xlsx"
    else:
        workbookfile = wbName + ".xlsx"
    # Create Workbook
    (workbook, wbFmts, wbHeaderImage) = createWorkbook(workbookfile, dwbFmts, verbose)
    
    # exportControllers
    exportControllers(baseURL, xlightsshowfolder, xlightsnetworksxmlfull, workbook, wbFmts, wbHeaderImage, verbose)
   
    ### Close xLights?
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
   
    # Close Workbook
    workbook.close()
    #
    print ("*" * 50)
    print ("main: (900) Exported Controllers to Workbook: %s" % workbookfile)

    print ("*" * 50)
    print ("main: (999) *** Export Controllers End ***")
    print ("*" * 50)


if __name__ == "__main__":
    main()

