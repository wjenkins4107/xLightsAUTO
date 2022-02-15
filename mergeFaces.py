#!/usr/bin/env python

# Name: mergeFaces.py
# Purpose: Parse the xLights RGB Effects XML file for model face attributes, copies face image file to faces folder in show folder and write updated rgbeffects file xml file
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/12/2022

###########################
# Imports                 #
###########################

import argparse
import xml.etree.ElementTree as ET
import sys
import os
import datetime
import re
import shutil

###############################
# main                        #
###############################

def main():

	print ("#" *5 + " mergeFaces Begin")

	cli_parser = argparse.ArgumentParser(prog = 'checkSequence',
		description = '''%(prog)s is a tool to parse the xLights RGB Effects XML file for model face attributes, copy face image file to faces folder in show folder and write updated rgbeffects file xml file,''')
	
	### Define Arguments

	cli_parser.add_argument('-s', '--xLightsShowFolder', help = 'xLights Show Folder',
		required = True)

	cli_parser.add_argument('-f', '--facesFolder', help = 'Merged Faces Folder',default = "DEFAULT",
		required = False)

	cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
		required = False)

	args = cli_parser.parse_args()
	
	xLightsShowFolder = args.xLightsShowFolder
	facesFolder = args.facesFolder
	verbose = args.verbose
	if (verbose):
		print ("xLights Show Folder = %s" % xLightsShowFolder)
		print ("Faces Folder = %s" % facesFolder)

	# Verify Show Folder
	if not os.path.isdir(xLightsShowFolder):
		print("Error: xLights Show Folder not found %s" % xLightsShowFolder)
		sys.exit(-5)

	# Default Faces Folder
	if (facesFolder == "DEFAULT"):
		facesFolder =  xLightsShowFolder + "\\Faces"
	facesFolder = os.path.abspath(facesFolder)
	# Make Faces Folder?
	if not os.path.isdir(facesFolder):
		os.mkdir(facesFolder)

	# Face Info Attr List
	faceInfoAttr = ["Type", "Name", "Mouth-AI-EyesClosed", "Mouth-AI-EyesOpen", "Mouth-E-EyesClosed", "Mouth-E-EyesOpen", "Mouth-FV-EyesClosed", "Mouth-FV-EyesOpen", 
					"Mouth-L-EyesClosed", "Mouth-L-EyesOpen", "Mouth-MBP-EyesClosed", "Mouth-MBP-EyesOpen", "Mouth-O-EyesClosed", "Mouth-O-EyesOpen",
					"Mouth-U-EyesClosed", "Mouth-U-EyesOpen", "Mouth-WQ-EyesClosed", "Mouth-WQ-EyesOpen", "Mouth-etc-EyesClosed", "Mouth-etc-EyesOpen",
					"Mouth-rest-EyesClosed", "Mouth-rest-EyesOpen"]
	
	xrgbEffectsXMLFile = "xlights_rgbeffects.xml"

	# RGB Effects Tree
	rgbEffectsTree = ET.parse(xLightsShowFolder + "\\" + xrgbEffectsXMLFile)
	# RGB Effects Root
	rgbEffectsRoot = rgbEffectsTree.getroot()
	# Get model in models
	for model in rgbEffectsRoot.findall("models/model"):
		modelName = model.get("name")
		if (verbose):
			print ("#" * 50)
			print ("# Model Name = %s" % modelName)
			print ("#" * 50)
		# Find All faceInfo
		for faceInfo in model.findall("faceInfo"):
			# Find faceInfo Attributes
			for i in range(len(faceInfoAttr)):
				# Type Attr?
				if (i == 0):
					faceType = faceInfo.get(faceInfoAttr[i])
					if (verbose):
						print (" " * 4 + "Begin Face Info")
						print (" " * 8 + "%s = %s" % (faceInfoAttr[i], faceType))
				# Name Attr?
				elif (i == 1):
					faceName = faceInfo.get(faceInfoAttr[i])
					if (verbose):
						print (" " * 8 + "%s = %s" % (faceInfoAttr[i], faceName))
				# Mouth Attr?
				elif (i > 1):
					if (verbose):
						print (" " * 8 + "Mouth Attr = %s" % (faceInfoAttr[i]))
					# Matrix Face Type?
					if (faceType == "Matrix"):
						oldImageFile = faceInfo.get(faceInfoAttr[i])
						if (verbose):
							print (" " * 12 + "Image File=%s" % oldImageFile)
						# Image File not None
						if (oldImageFile is not None):
							# Image File Not Empty?
							if oldImageFile.strip():
								# OS Absolute Path of Image File Exists?
								oldImageFile = os.path.abspath(oldImageFile)
								if os.path.isfile(oldImageFile):
									imageFile = oldImageFile.split("\\")[-1]
									newImageFile = facesFolder + "\\" +  imageFile
									if (verbose):
										print(" " * 12 + "old image file %s = new image file %s" % (oldImageFile, newImageFile))
									# Copy Image file
									if not os.path.isfile(newImageFile):
										shutil.copy(oldImageFile, newImageFile) 
									# Update faceInfo attribute
									faceInfo.attrib[faceInfoAttr[i]] = str(newImageFile)
								else:
									print(" " * 12 + "Error: Image file not found; Model Name=%s; Face Name=%s; Face Info Attr=%s; File=%s" % (modelName, faceName, faceInfoAttr[i], oldImageFile))
							else:
								print(" " * 12 + "Error: Image file empty; Model Name=%s; Face Name=%s; Face Info Attr=%s" % (modelName, faceName, faceInfoAttr[i]))
						else:
							print(" " * 12 + "Error: Image file = None; Model Name=%s; Face Name=%s; Face Info Attr=%s" % (modelName, faceName, faceInfoAttr[i]))
			if (verbose):
				print (" " * 4 + "End Face Info")
		if (verbose):
			print ("End Model %s" % modelName)

	# Write Updated RGB Effects XML File
	timestamp = "\\xrgb_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_"
	newxrgbEffectsXMLFull = xLightsShowFolder + timestamp + xrgbEffectsXMLFile
	rgbEffectsTree.write(newxrgbEffectsXMLFull)
	print ("#" * 5 + " New RGB Effects XML file= %s" % newxrgbEffectsXMLFull)
	
	print ("#" * 5 + " mergeFaces End")

if __name__ == "__main__":
    main()