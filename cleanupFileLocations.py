#!/usr/bin/env python

# Name: cleanupFileLocations.py
# Purpose: clean up file locations in all xlLights sequences in a show folder and sub folders
# Author: Bill Jenkins
# Version: v1.0
# Date: 08/12/2023

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

import urllib.parse

###############################
# createParamsStr			  #
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
# cleanupFileLocations        #
###############################

def cleanupFileLocations(baseURL, sequence, fullsequence, verbose):

	# Open sequence
	params_dict =  {"seq": fullsequence}
	fppparams = createParamsStr(params_dict, verbose)
	request = baseURL + "openSequence/" + fppparams
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
	# Clean Up File Locations
	request = baseURL + "cleanupFileLocations"
	(ret_code, status_code, result) = doRequestsGet(request, 900, verbose)
	# Request Error?
	if (ret_code < 0):
		print("Unable to connect to xLights REST API %s" % baseURL)
		print ("ret_code = ", ret_code)
		print ("result = ", result) 
		sys.exit(ret_code)
	
	
	print ("sequence = ", sequence)
	print ("status_code = ", status_code)
	print ("result = ", result)
	# Save sequence
	request = baseURL + "saveSequence"
	if (verbose):
		print ("##### Save sequence %s" % sequence)
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
	# Close sequence
	request = baseURL + "closeSequence"
	if (verbose):
		print ("##### Close sequence %s" % sequence)
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
# main                        #
###############################

def main():

	print ("#" *5 + " cleanupFileLocations Begin")

	cli_parser = argparse.ArgumentParser(prog = 'cleanupFileLocation',
		description = '''%(prog)s is a tool to render all xLights sequences in a show folder,''')
	
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

	
	# Base URL
	baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
	if (verbose):
		print ("Base URL = %s" % baseURL)

	# Verify Show Folder
	if not os.path.isdir(xlightsshowfolder):
		print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
		sys.exit(-5)

	# verify xlights program file exists
	xlightsprogramfile = xlightsprogramfolder + "\\xlights.exe"
	if not os.path.isfile(xlightsprogramfile):
		print("Error: xLights Program File not found %s" % xlightsprogramfile)
		sys.exit(-1)

	# Start xLights
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
				  # Render All Sequence
				  cleanupFileLocations(baseURL, sequence, fullsequence, verbose)
				  

	# Save Layout
	request = baseURL + "saveLayout"
	if (verbose):
		print ("##### Save Layout")
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
	
	print ("#" *5 + " cleanupFileLocations End")
if __name__ == "__main__":
	main()