#!/usr/bin/env python

# Name: checkSeqMedia.py
# Purpose: Parse xLights Sequence XML file and check for media errors
# Author: Bill Jenkins
# Version: v1.0
# Date: 02/21/2022

###########################
# Imports                 #
###########################

import xml.etree.ElementTree as ET
import argparse
import os
import sys
import re



def main():

	cli_parser = argparse.ArgumentParser(prog = 'createShowFolder',
		description = '''%(prog)s is a tool to search a file for media references and list any errors,''')
   
	### Define Arguments

	cli_parser.add_argument('-s', '--showFolder' , help = 'xLights Show Folder',
		required = True)

	cli_parser.add_argument('-v', '--verbose', help = 'Verbose Logging', action='store_true',
		required = False)

	### Get Arguments
	args = cli_parser.parse_args()

	showFolder = args.showFolder
	verbose = args.verbose

	if not os.path.isdir(showFolder):
		print ("Show folder not found %s" % showFolder)

	EffectKeyList = ["E_FILEPICKER_Pictures_Filename", "E_0FILEPICKERCTRL_IFS" ,"E_FILEPICKERCTRL_Video_Filename"]
	lenEffectKeyList = len(EffectKeyList)

	for root, dir, files in os.walk(showFolder):
		for file in files:
			# xLights Sequence File?
			if (file.endswith(".xsq")):
				fullsequence = os.path.join(root, file)
				found = fullsequence.find("Backup\\")
				# xLights Sequence File not in the Backup folder?
				if (found < 0):
					print ("*" * 5)
					print ("Sequence=%s" % fullsequence)
					xsqtree = ET.parse(fullsequence)
					xsqroot = xsqtree.getroot()
					sequenceType = xsqroot.find("head/sequenceType")
					print (" " * 2 + "sequenceType=%s" % sequenceType.text)
					if (sequenceType.text == "Media"):
						mediaFile = xsqroot.find("head/mediaFile")
						print (" " * 2 + "mediaFile=%s" % mediaFile.text)
					imagesCtr = 0
					shadersCtr = 0
					videosCtr = 0
					refCtr = 0
					for Effect in xsqroot.findall("EffectDB/Effect"):
						if (Effect is not None):
							EffectText = str(Effect.text)
							lenEffectText = len(EffectText)
							refCtr += 1
							for i in range(lenEffectKeyList):
								beginKey = beginKey = EffectText.find(EffectKeyList[i])
								if (beginKey > -1):
									endKey = EffectText[beginKey:lenEffectText].find("=")
									beginValue = beginKey + endKey + 1
									endValue = beginValue + EffectText[beginValue:lenEffectText].find(",")
									#if (verbose):
									#	print (" "* 4  + "EffectText=%s" % EffectText)
									#	print (" "* 4  + "i=%s beginKey=%s endKey=%s beginValue=%s endValue=%s" % (i, beginKey, endKey, beginValue, endValue))
									fullmediafile = EffectText[beginValue:endValue]
									splitfullmediafile = fullmediafile.split("\\")
									mediafile = splitfullmediafile[-1]
									#if (verbose):
									#	print (" "* 4  + "fullmediafile=%s" % fullmediafile)
									#	print (" "* 4  + "mediafile=%s" % mediafile)
									match i:
										# Images?
											case 0:
												if os.path.isfile(fullmediafile):
													if (verbose):
														print (" "* 4 + "Image=%s ref=%s" % (fullmediafile, refCtr))
												else:
													print (" "* 4 + "ERROR: Image %s not Found" % (fullmediafile))
												imagesCtr += 1
												break
										# Shaders?
											case 1:
												if os.path.isfile(fullmediafile):
													if (verbose):
														print (" "* 4 + "Shader=%s ref=%s" % (fullmediafile, refCtr))
												else:
													print (" "* 4 + "ERROR: Shader %s not Found" % (fullmediafile))
												shadersCtr += 1
												break
										# Videos?
											case 2:
												if os.path.isfile(fullmediafile):
													if (verbose):
														print (" "* 4 + "Video=%s ref=%s" % (fullmediafile, refCtr))
												else:
													print (" "* 4 + "ERROR: Video %s not Found" % (fullmediafile))
												videosCtr += 1
												break
					print (" " * 4 + "Total Images=%s Total Shaders=%s Total Videos=%s" % (imagesCtr, shadersCtr, videosCtr))
					print ("*" * 5)

if __name__ == "__main__":
    main()