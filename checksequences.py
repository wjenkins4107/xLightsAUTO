#!/usr/bin/env python

# Name: checkSequences.py
# Purpose: check sequence for all sequences in a show folder and sub folders
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/07/2022

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
from shutil import copy

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

###############################
# checkSequence               #
###############################

def checkSequence(baseURL, sequence, fullsequence, xlightsshowfolder, outputfolder, notepadopen, verbose):

	# Check Sequence
	request = baseURL + "checkSequence?seq=" + re.sub(" ", r"%20", fullsequence)
	if (verbose):
		print ("##### Check Sequence %s" % sequence)
		print ("request = ", request)
	(ret_code, status_code, result) = doRequestsGet(request, 900, verbose)
	# Request Error?
	if (ret_code < 0):
		print("Unable to connect to xLights REST API %s" % baseURL)
		print ("ret_code = ", ret_code)
		print ("result = ", result) 
		sys.exit(ret_code)		
	# 
	if (verbose):
		print ("status_code = ", status_code)
		print ("result = ", result)
	
	# Output full file name
	d1 = json.loads(result)
	outputfile = d1["output"]
	
	# No Output Folder Defined? 
	if (outputfolder == "NONE"):
		newoutputfile = outputfile
	else:
		# Copy Check Sequence Output File to Check Sequence Output Folder using Sequence name
		checksequencefolder = xlightsshowfolder + "\\" + outputfolder
		# Folder does not exist?
		if not os.path.isdir(checksequencefolder):
			os.mkdir(checksequencefolder)
		# Copy Check Sequence Output File Name
		newoutputfile = checksequencefolder + "\\" + re.sub(".xsq", ".txt", sequence) 
		# Copy File
		copy(outputfile, newoutputfile)

	# Check Sequence Output File Searches
	p1 = re.compile(r"^Show folder:")
	p2 = re.compile(r"^Sequence:")
	p3 = re.compile(r"^Errors:")
	
	print ("##### Check Sequence Summary")
	print ("Check Sequence Output File: %s" % newoutputfile)	
	
	# Open Check Sequence Output File 
	FINPUT = open(newoutputfile, "r")
	for line in FINPUT:
		s1 = p1.search(line)
		# Strip Trailing Newline
		line = line.rstrip()
		if (s1):
			print (line)
		else:
			s2 = p2.search(line)
			if (s2):
				print (line)
			else:
				s3 = p3.search(line)
				if (s3):
					print (line)
	# Close INPUT File
	FINPUT.close()

	# Open Check Sequence Output in Notepad?
	if (notepadopen):
		cmd = ("notepad.exe " + newoutputfile)
		try:
			cp = subprocess.Popen(cmd)
		except:
			sys.exit("*** Error in starting notepad %s" % sys.exc_info()[0])
	return()

###############################
# Main                        #
###############################	

def main():

	cli_parser = argparse.ArgumentParser(prog = 'checkSequences',
		description = '''%(prog)s is a tool to perform a check sequence on all xLights sequences in a show directory,''')
	
	### Define Arguments	

	cli_parser.add_argument('-s', '--xlightsshowfolder', help = 'xLights Show Folder',
		required = True)

	cli_parser.add_argument('-i', '--xlightsipaddress', help = 'xLights REST API IP Address', default = "127.0.0.1",
		required = False)

	cli_parser.add_argument('-p', '--xlightsport', help = 'xLights REST API Port', default = "49913", choices = ["49913", "49914"],
		required = False)
		
	cli_parser.add_argument('-x', '--xlightsprogramfolder', help = 'xLights Program Folder', default = "c:\\program files\\xlights",
		required = False)
		
	cli_parser.add_argument('-o', '--outputfolder', help = 'Output Folder', default = "NONE",
		required = False)

	cli_parser.add_argument('-n', '--notepadopen' , help = 'Notepad Open', action='store_true',
		required = False)

	cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
		required = False)

	print ("##### checkSequence Started")
	
	### Get Arguments

	args = cli_parser.parse_args()
	
	xlightsshowfolder = args.xlightsshowfolder
	xlightsipaddress = args.xlightsipaddress
	xlightsport = args.xlightsport
	xlightsprogramfolder = args.xlightsprogramfolder
	outputfolder = args.outputfolder
	notepadopen = args.notepadopen
	verbose = args.verbose
	if (verbose):
		print ("Xlights Show Folder = %s" % xlightsshowfolder)
		print ("Xlights IP Address = %s" % xlightsipaddress)
		print ("Xlights Port = %s" % xlightsport)
		print ("xLights Program Folder = %s" % xlightsprogramfolder)
		print ("Output Folder = %s" % outputfolder)
		print ("Notepad Open = %s" % notepadopen)

	
	# Base URL
	baseURL = "http://" + xlightsipaddress + ":" + xlightsport + "/"
	if (verbose):
		print ("Base URL = %s" % baseURL)

	# Verify Show Folder
	if not os.path.isdir(xlightsshowfolder):
		print("Error: xLights Show Folder not found %s" % xlightsshowfolder)
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
					# Check Sequence
					checkSequence(baseURL, sequence, fullsequence, xlightsshowfolder, outputfolder, notepadopen, verbose)

	print ("##### checkSequence Ended")	
				  

if __name__ == "__main__":
	main()