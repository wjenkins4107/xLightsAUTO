#!/usr/bin/env python

# Name: createShowFolder.py
# Purpose: Create a new show folder from an existing show folder
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/10/2022

###############################
# Imports                     #
###############################

import xml.etree.ElementTree as ET
import argparse
import sys
import os
import datetime
import re
from shutil import copy
from shutil import copytree

###############################
# createShowFolder            #
###############################

def createShowFolder(oldShowFolder, newShowFolder, xrgbEffectsFile, backupFolder, fseqFolder, renderCacheFolder, shadersFolder, verbose):

	# Making New Show Folder
	if (verbose):
		print ("Making New Show Folder %s" % newShowFolder)
	os.mkdir(newShowFolder)

	# Copy xLights keybindings file from Old Show Folder to New Show Folder
	oldKeyBindingsFile = oldShowFolder + "\\xlights_keybindings.xml"
	newKeyBindingsFile = newShowFolder + "\\xlights_keybindings.xml"
	if (verbose):
		print ("Copying %s to %s" % (oldKeyBindingsFile, newKeyBindingsFile))
	copy(oldKeyBindingsFile, newKeyBindingsFile)

	# Copy xLights networks file from Old Show Folder to New Show Folder
	oldNetworksFile = oldShowFolder + "\\xlights_networks.xml"
	newNetworksFile = newShowFolder + "\\xlights_networks.xml"
	if (verbose):
		print ("Copying %s to %s" % (oldNetworksFile, newNetworksFile))
	copy(oldNetworksFile, newNetworksFile)
	
	# Copy Shaders Folder?
	oldShadersFolder = oldShowFolder + "\\" + shadersFolder
	newShadersFolder = newShowFolder + "\\" + shadersFolder
	if os.path.isdir(oldShadersFolder):
		copytree(oldShadersFolder, newShadersFolder)

	# RGB Effects XML Tree
	treeparse = oldShowFolder + "\\" + "xlights_rgbeffects.xml"
	rgbeffectstree = ET.parse(treeparse)
	# RGB Effects XML Root
	rgbeffectsroot = rgbeffectstree.getroot()
	if (verbose):
		print ("rgbeffectsroot.tag = %s" % rgbeffectsroot.tag)
		print ("rgbeffectsroot.attrib = %s" % rgbeffectsroot.attrib)
	# Parse RGB Effects XML for settings
	settings = rgbeffectsroot.find("settings")
	for setting in settings:
		if (verbose):
			print ("*" * 4 + " setting.tab=%s setting.value=%s" % (setting.tag, setting.attrib))
		mtag = str(setting.tag)
		match mtag:

			# backgroundImage?
			case "backgroundImage":
				if (verbose):
					print ("*" * 8 + " Background Image Setting Found %s" % setting.attrib["value"])
				oldbackgroundImage = setting.attrib["value"]
				# Get New Background Image File Name
				attribsplit = setting.attrib["value"].split("\\")
				newbackgroundImage = newShowFolder + "\\" + attribsplit[-1]
				# Copy Background Image File to New Show Folder 
				copy(oldbackgroundImage, newbackgroundImage)
				# Update backgroundImage
				setting.set("value", newbackgroundImage)

			# backupDir?
			case "backupDir":
				oldbackupFolder = setting.attrib["value"]
				if (verbose):
					print ("*" * 8 + " backupDir Setting Found %s" % oldbackupFolder)
				if (backupFolder == "DEFAULT"):
					if (oldbackupFolder.upper() == oldShowFolder.upper()):
						newbackupFolder = newShowFolder
					else:
						newbackupFolder = newShowFolder + "\\Backup"
				elif (backupFolder == "SAME"):
					newbackupFolder = oldbackupFolder 
				else:
					newbackupFolder = backupFolder
				# Folder does not exist?
				if not os.path.isdir(newbackupFolder):
					if (verbose):
						print ("Creating New Backup Folder %s" % newbackupFolder)
					os.mkdir(newbackupFolder)
				# Update backupDir
				if (verbose):
					print ("New backupDir setting =%s" % newbackupFolder)
				setting.set("value", newbackupFolder)

			# fseqDir?
			case "fseqDir":
				oldfseqFolder = setting.attrib["value"]
				if (verbose):
					print ("*" * 8 + " fseqDir Setting Found %s" % oldfseqFolder)
				if (fseqFolder == "DEFAULT"):
					if (oldfseqFolder.upper() == oldShowFolder.upper()):
						newfseqFolder = newShowFolder
					else:
						newfseqFolder = newShowFolder + "\\FSEQ"
				elif (fseqFolder == "SAME"):
					newfseqFolder = oldfseqFolder 
				else:
					newfseqFolder = fseqFolder
				# Folder does not exist?
				if not os.path.isdir(newfseqFolder):
					if (verbose):
						print ("Creating New FSEQ Folder %s" % newfseqFolder)
					os.mkdir(newfseqFolder)
				# Update fseqDir
				if (verbose):
					print ("New fseqDir setting =%s" % newfseqFolder)
				setting.set("value", newfseqFolder)

			case "renderCacheDir":
				oldrenderCacheFolder = setting.attrib["value"]
				if (verbose):
					print ("*" * 8 + " renderCacheDir Setting Found %s" % oldrenderCacheFolder)
				if (renderCacheFolder == "DEFAULT"):
					if (oldrenderCacheFolder.upper() == oldShowFolder.upper()):
						newrenderCacheFolder = newShowFolder
					else:
						newrenderCacheFolder = newShowFolder + "\\RenderCache"
				elif (renderCacheFolder == "SAME"):
					newrenderCacheFolder = oldrenderCacheFolder
				else:
					newrenderCacheFolder = renderCacheFolder
				# Folder does not exist?
				if not os.path.isdir(newrenderCacheFolder):
					if (verbose):
						print ("Creating New Render Cache Folder %s" % newrenderCacheFolder)
					os.mkdir(newrenderCacheFolder)
				# Update renderCache value
				if (verbose):
					print ("New renderCacheDir setting =%s" % newrenderCacheFolder)
				setting.set("value", newrenderCacheFolder)

	# Write New RGB Effects XML File
	newxrgbEffectsFull = newShowFolder + "\\" + xrgbEffectsFile
	# Write New RGB Effects File
	rgbeffectstree.write(newxrgbEffectsFull)
	print ("#" * 5 + " New RGB Effects XML file= %s" % newxrgbEffectsFull)

	return()

###############################
# main                        #
###############################

def main():

	print ("#" *5 + " createShowFolder Begin")

	cli_parser = argparse.ArgumentParser(prog = 'createShowFolder',
		description = '''%(prog)s is a tool to create a new show folder from an existing show folder,''')
	
	### Define Arguments

	cli_parser.add_argument('-o', '--oldShowFolder', help = 'Old Show Folder',
		required = True)

	cli_parser.add_argument('-n', '--newShowFolder', help = 'New Show Folder',
		required = True)

	cli_parser.add_argument('-b', '--backupFolder', default="DEFAULT", help = 'Backup Folder',
		required = False)

	cli_parser.add_argument('-f', '--fseqFolder', default="DEFAULT", help = 'FSEQ Folder',
		required = False)

	cli_parser.add_argument('-r', '--renderCacheFolder', default="DEFAULT", help = 'Render Cache Folder',
		required = False)

	cli_parser.add_argument('-s', '--shadersFolder', default="Shaders", help = 'Shaders Folder',
		required = False)

	cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
		required = False)

	### Get Arguments

	args = cli_parser.parse_args()

	oldShowFolder = os.path.abspath(args.oldShowFolder)
	newShowFolder = os.path.abspath(args.newShowFolder)
	backupFolder  = args.backupFolder
	fseqFolder  = args.fseqFolder
	renderCacheFolder = args.renderCacheFolder
	shadersFolder  = args.shadersFolder
	verbose = args.verbose

	if (verbose):
		print ("Old Show Folder = %s" % oldShowFolder)
		print ("New Show Folder = %s" % newShowFolder)
		print ("Backup Folder = %s" % backupFolder)
		print ("FSEQ Folder = %s" % fseqFolder)
		print ("Render Cache Folder = %s" % renderCacheFolder)
		print ("Shaders Folder = %s" % shadersFolder)
	
	xkeyBindingsFile = "xlights_keybindings.xml"
	xNetworksFile = "xlights_networks.xml"
	xrgbEffectsFile = "xlights_rgbeffects.xml"

	# Verify Old Show Folder
	if not os.path.isdir(oldShowFolder):
		print("Error: Old Show Folder not found %s" % oldShowFolder)
		sys.exit(-1)

	# Verify xLights xlights_keybindings.xml file
	oldxLightsKeyBindingsFile = oldShowFolder + "\\" + xkeyBindingsFile
	if not os.path.isfile(oldxLightsKeyBindingsFile):
		print("Error: xlights_keybindings.xml not found in %s" % oldShowFolder)
		sys.exit(-1)

	# Verify xLights xlights_networks.xml file
	oldxLightsNetworksFile = oldShowFolder + "\\" + xNetworksFile
	if not os.path.isfile(oldxLightsNetworksFile):
		print("Error: xlights_networks.xml not found in %s" % oldShowFolder)
		sys.exit(-1)

	# Verify xLights xlights_rgbeffects.xml file
	oldxLightsRgbEffectsFile = oldShowFolder + "\\" + xrgbEffectsFile
	if not os.path.isfile(oldxLightsRgbEffectsFile):
		print("Error: xlights_rgbeffects.xml not found in %s" % oldShowFolder)
		sys.exit(-1)

	# Verify New Show Folder
	if os.path.isdir(newShowFolder):
		print("Error: New Show Folder already exists %s" % newShowFolder)
		sys.exit(-1)

	createShowFolder(oldShowFolder, newShowFolder, xrgbEffectsFile, backupFolder, fseqFolder, renderCacheFolder, shadersFolder, verbose)
	print ("#" * 5 + " New Show Folder %s Created" % newShowFolder)
	print ("#" *5 + " createShowFolder End")

if __name__ == "__main__":
	main()