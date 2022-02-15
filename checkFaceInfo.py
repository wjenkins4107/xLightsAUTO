#!/usr/bin/env python

# Name: checkFaceInfo.py
# Purpose: Parse the xLights RGB Effects XML file for model faceInfo elements, list any errors within the element, optionally remove the element in error and output new XML
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/13/2022

###########################
# Imports                 #
###########################

import argparse
import xml.etree.ElementTree as ET
import sys
import os
import datetime

###############################
# main                        #
###############################

def main():
	print ("#" * 50)
	print ("#" *5 + " checkFaceInfo Begin")
	print ("#" * 50)

	cli_parser = argparse.ArgumentParser(prog = 'checkFaceInfo',
		description = '''%(prog)s is a tool to parse the xLights RGB Effects XML file for faceInfo elements, list any errors within the element, optionally remove the element in error and output new XML,''')
	
	### Define Arguments

	cli_parser.add_argument('-s', '--xShowFolder', help = 'xLights Show Folder',
		required = True)

	cli_parser.add_argument('-x', '--xrgbEffectsXMLFile', help = 'xLights RGB Effects XML File',default = "xlights_rgbeffects.xml",
		required = False)

	cli_parser.add_argument('-r', '--removeFaceInfoElement', help = 'Remove faceInfo Elements with Error from XML', action='store_true',
		required = False)

	cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
		required = False)

	args = cli_parser.parse_args()
	
	xShowFolder = os.path.abspath(args.xShowFolder)
	xrgbEffectsXMLFile = args.xrgbEffectsXMLFile
	removeFaceInfoElement = args.removeFaceInfoElement
	verbose = args.verbose
	if (verbose):
		print ("xLights Show Folder = %s" % xShowFolder)
		print ("xLights RGB Effects XML File = %s" % xrgbEffectsXMLFile)
		print ("Remove faceInfo Element = %s" % removeFaceInfoElement)

	# faceInfo Attributes List
	faceInfoAttr = ["Name",
					"Type", 
					"Mouth-AI-EyesClosed", "Mouth-AI-EyesOpen",
					"Mouth-E-EyesClosed", "Mouth-E-EyesOpen",
					"Mouth-FV-EyesClosed", "Mouth-FV-EyesOpen",
					"Mouth-L-EyesClosed", "Mouth-L-EyesOpen",
					"Mouth-MBP-EyesClosed", "Mouth-MBP-EyesOpen",
					"Mouth-O-EyesClosed", "Mouth-O-EyesOpen",
					"Mouth-U-EyesClosed", "Mouth-U-EyesOpen",
					"Mouth-WQ-EyesClosed", "Mouth-WQ-EyesOpen",
					"Mouth-etc-EyesClosed", "Mouth-etc-EyesOpen",
					"Mouth-rest-EyesClosed", "Mouth-rest-EyesOpen"]

	# Verify Show Folder
	if not os.path.isdir(xShowFolder):
		print("Error: xLights Show Folder not found %s" % xShowFolder)
		sys.exit(-1)

	# Verify RGB Effects XMl File
	xrgbEffectsXMLFull = xShowFolder + "\\" + xrgbEffectsXMLFile
	if not os.path.isfile(xrgbEffectsXMLFull):
		print("Error: xLights RGB Effects XML File not found %s" % xrgbEffectsXMLFull)
		sys.exit(-1)

	# RGB Effects Tree
	xrgbEffectsTree = ET.parse(xrgbEffectsXMLFull)
	# RGB Effects Root
	xrgbEffectsRoot = xrgbEffectsTree.getroot()
	# XML Updated
	xrgbEffectsXMLUpdated = False
	noFaceInfoErrorsFound = True
	errCtr = 0
	elementsRemovedCtr = 0 
	# Get model in models
	for model in xrgbEffectsRoot.findall("models/model"):
		ModelName = model.get("name")
		if (verbose):
			print (" " * 4 + "#" * 50)
			print (" " * 4 + "# Model Name = %s" % ModelName)
			print (" " * 4 + "#" * 50)
		# Find All faceInfo
		for faceInfo in model.findall("faceInfo"):
			# Find faceInfo Attributes
			FaceName = ""
			FaceType = ""
			faceInfoErrorsFound = False
			for i in range(len(faceInfoAttr)):
				# Name?
				if (i == 0):
					FaceName = faceInfo.get(faceInfoAttr[i])
					if (verbose):
						print (" " * 8 + "#" * 50)
						print (" " * 8 + "# Begin Face Info")
						print (" " * 8 + "#" * 50)
						print (" " * 12 + "Name=%s" % (FaceName))
				# Type?
				elif (i == 1):
					FaceType = faceInfo.get(faceInfoAttr[i])
					if (verbose):
						print (" " * 12 + "Type=%s" % (FaceType))
				# Mouth Open/Close Attr
				elif (i > 1):
					# Matrix Type?
					if (FaceType == "Matrix"):
						imageFile = faceInfo.get(faceInfoAttr[i])
						# Image File not None
						if (imageFile is not None):
							# Image File Not Empty?
							if imageFile.strip():
								# OS Absolute Path of Image File Exists?
								imageFile = os.path.abspath(imageFile)
								if os.path.isfile(imageFile):
									if (verbose):
										print (" " * 12 + "Model=%s / Face=%s / Attr=%s / Value=%s found" % (ModelName, FaceName, faceInfoAttr[i], imageFile))
								else:
									noFaceInfoErrorsFound = False
									faceInfoErrorsFound = True
									errCtr += 1
									# Remove Error Element
									if (verbose):
										print (" " * 12 + "ERROR in Element: Model=%s / Face=%s / Attr=%s / Value=%s not found" % (ModelName, FaceName, faceInfoAttr[i], imageFile))
									else:
										print (" " * 4 + "ERROR in Element:  Model=%s / Face=%s / Attr=%s / Value=%s not found" % (ModelName, FaceName, faceInfoAttr[i], imageFile))
							else:
								noFaceInfoErrorsFound = False
								faceInfoErrorsFound = True
								errCtr += 1
								if (verbose):
									print (" " * 12 + "ERROR in Element: Model=%s / Face=%s / Attr=%s / Value=Empty" % (ModelName, FaceName, faceInfoAttr[i]))
								else:
									print (" " * 4 + "ERROR in Element: / Model=%s / Face=%s / Attr=%s / Value=Empty" % (ModelName, FaceName, faceInfoAttr[i]))
						else:
							noFaceInfoErrorsFound = False
							faceInfoErrorsFound = True
							errCtr += 1
							if (verbose):
								print (" " * 12 + "ERROR in Element: Model=%s / Face=%s / Attr=%s / Value=None" % (ModelName, FaceName, faceInfoAttr[i]))
							else:
								print (" " * 4 + "ERROR in Element: / Model=%s / Face=%s / Attr=%s / Value=None" % (ModelName, FaceName, faceInfoAttr[i]))
						
			# Errors Found?
			if (faceInfoErrorsFound):
				# Remove faceInfo Element?
				if (removeFaceInfoElement):
					model.remove(faceInfo)
					if (verbose):
						print (" " * 8 + "#" * 50)
						print (" " * 8 + "# End Face Info")
						print (" " * 8 + "# Removed faceInfo Element Model=%s / Face=%s" % (ModelName, FaceName))
						print (" " * 8 + "#" * 50)
					else:
						print ("#" * 4 + " Removed faceInfo Element Model=%s / Face=%s" % (ModelName, FaceName))
					xrgbEffectsXMLUpdated = True
					elementsRemovedCtr += 1
			else:
				if (verbose):
					print (" " * 8 + "#" * 50)
					print (" " * 8 + "End Face Info")
					print (" " * 8 + "#" * 50)
		if (verbose):
			print (" " * 4 + "#" * 50)
			print (" " * 4 + "# End Model %s" % ModelName)
			print (" " * 4 + "#" * 50)

	print ("#" * 50)
	if (noFaceInfoErrorsFound):
		print ("#" * 5 + " No errors in model faceInfo elements found")
	else:
		if (xrgbEffectsXMLUpdated):
			print ("#" * 5 + " Model faceInfo elements removed %s" % elementsRemovedCtr)
			timestamp = "\\xrgb_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_"
			newxrgbEffectsXMLFull = xShowFolder + timestamp + xrgbEffectsXMLFile
			xrgbEffectsTree.write(newxrgbEffectsXMLFull)
			print ("#" * 5 + " New RGB Effects XML file= %s" % newxrgbEffectsXMLFull)
		else:
			print ("#" * 5 + " Errors in model faceInfo elements found %s" % errCtr)
	print ("#" * 50)
	print ("#" * 5 + " checkFaceInfo End")
	print ("#" * 50)

if __name__ == "__main__":
    main()