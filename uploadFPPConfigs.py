#!/usr/bin/env python

# Name: uploadFPPConfigs,py
# Purpose: Upload an FPP Config to FPP instance using a csv formatted input file 
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/07/2022

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
# startxLights				  #
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
# uploadFPPConfig			  #
###############################

def uploadFPPConfig(baseURL, fppip, fppudp, fppmodels, fppmap, verbose):

	
	params_dict =  {"ip": fppip, "udp": fppudp, "models": fppmodels, "map": fppmap}
	fppparams = createParamsStr(params_dict, verbose)
	request = baseURL + "uploadFPPConfig/" + fppparams  
	print ("Upload FPP Config to FPP IP:%s udp:%s models:%s map:%s" % (fppip, fppudp, fppmodels, fppmap))
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

def main():

	print ("#" *5 + " uploadFPPConfigs Begin")

	cli_parser = argparse.ArgumentParser(prog = 'uploadSequences',
		description = '''%(prog)s is a tool to upload an fpp config with parms defined in a csv formatted input file ,''')
   
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
		print ("Upload FPP Config CSV File = %s" % uploadcsvfile)
		print ("xLights Show Folder = %s" % xlightsshowfolder)
		print ("xLights IP Address = %s" % xlightsipaddress)
		print ("xLights Port = %s" % xlightsport)
		print ("xLights Program Folder = %s" % xlightsprogramfolder)
		print ("Close xLights = %s" % closexlights)
	
	# verify upload file exists
	if not os.path.isfile(uploadcsvfile):
		print("Error: Upload FPP Config CSV file not found %s" % uploadcsvfile)
		sys.exit(-1)
		
	# verify xlights show folder exists
	if not os.path.isdir(xlightsshowfolder):
		print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
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
	with open(uploadcsvfile) as csvDataFile:
		csvReader = csv.reader(csvDataFile)
		for row in csvReader:
			if (verbose):
			   print ("FPP parms %s" % row)
			rowstr = str(row)
			if (rowstr[2] != "#"):
				# Valid Number of Parms?
				if (len(row) == 4):
					fppip = row[0]
					s1 = p1.search(fppip)
					if (not s1):
						sys.exit("*** ERROR Invalid IPv4 Address %s" % uploadip)
					if fppip not in controllerIPs:
						sys.exit("*** ERROR Controller IP %s not defined in Xlights" % uploadip)
					fppudp = row[1]
					if fppudp not in ["none", "all", "proxy"]:
						print ("*** UDP parm invalid on %s changed to default of \"none\"" % uploadip)
						fppudp = "none"
					fppmodels = row[2]
					if fppmodels not in ["true", "false"]:
						print ("*** Models parm invalid on %s changed to default of \"false\"" % uploadip)
						fppmodels = "false"
					fppmap = row[3]
					if fppmap not in ["true", "false"]:
						print ("*** Map parm invalid on %s changed to default of \"false\"" % uploadip)
						fppmap = "false"
					fppparms_list.append([fppip, fppudp, fppmodels, fppmap])
				else:
					print ("*** Invalid number of upload parms %s" % row)
	
	# Get Upload Sequence Parms
	for i in range(len(fppparms_list)):
		fppip = fppparms_list[i][0]
		fppudp = fppparms_list[i][1]
		fppmodels = fppparms_list[i][2]
		fppmap = fppparms_list[i][3]
		# Upload FPP Config
		uploadFPPConfig(baseURL, fppip, fppudp, fppmodels, fppmap, verbose) 

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