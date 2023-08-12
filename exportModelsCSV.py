#!/usr/bin/env python

# Name: exportModels.py
# Purpose: export models in a show folder to an excel file
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/05/2022

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
# exportModelsCSV             #
###############################

def exportModelsCSV(baseURL, exportfilename, xlightsshowfolder, outputfolder, verbose):
 
	# Output Folder
	if (outputfolder == "DEFAULT"):
		outputfolder = xlightsshowfolder + "\\exportModelsCSV"
	# Output Folder does not exist?
	outputfolder = os.path.abspath(outputfolder)
	if not os.path.isdir(outputfolder):
		# Make Output Folder
		os.mkdir(outputfolder)
	# Output File
	outputfile = outputfolder + "\\" + exportfilename + ".xlsx" 
	request = baseURL + "exportModelsCSV?filename=" + re.sub(" ", r"%20", outputfile) 
	print ("##### Export ModelsCSV for Show Folder %s " % xlightsshowfolder)
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

	print ("#" *5 + " exportModelsCSV Begin")

	cli_parser = argparse.ArgumentParser(prog = 'exportModelsCSV',
		description = '''%(prog)s is a tool to perform a export models to an excel file,''')
	
	### Define Arguments	

	cli_parser.add_argument('-f', '--exportfilename', help = 'Excel Export Models File Name',
		required = True)

	cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
		required = True)

	cli_parser.add_argument('-o', '--outputfolder', help = 'Excel File Output Folder', default = "DEFAULT",
		required = False)

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
	
	exportfilename = args.exportfilename
	xlightsshowfolder = os.path.abspath(args.xlightsshowfolder)
	outputfolder = args.outputfolder
	xlightsipaddress = args.xlightsipaddress
	xlightsport = args.xlightsport
	xlightsprogramfolder = os.path.abspath(args.xlightsprogramfolder)
	closexlights = args.closexlights
	verbose = args.verbose
	if (verbose):
		print ("Excel Export Models File Name = %s" % exportfilename)
		print ("XLights Show Folder = %s" % xlightsshowfolder)
		print ("Output Folder = %s" % outputfolder)
		print ("XLights IP Address = %s" % xlightsipaddress)
		print ("xLights Port = %s" % xlightsport)
		print ("xLights Program Folder = %s" % xlightsprogramfolder)
		print ("Close xLights = %s" % closexlights)
	
	# Base URL
	baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
	if (verbose):
		print ("Base URL = %s" % baseURL)

	# Verify Show Folder
	if not os.path.isdir(xlightsshowfolder):
		print("Error: Show Folder not found %s" % xlightsshowfolder)
		sys.exit(-5)

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
			
	# Change Show Folder
	request = baseURL + "changeShowFolder?folder=" + re.sub(" ", r"%20", xlightsshowfolder)
	if (verbose):
		print ("##### Change Show Folder")
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

	exportModelsCSV(baseURL, exportfilename, xlightsshowfolder, outputfolder, verbose)

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

	print ("#" *5 + " exportModelsCSV End")

if __name__ == "__main__":
	main()