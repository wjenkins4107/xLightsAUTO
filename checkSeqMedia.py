#!/usr/bin/env python

# Name: checkSeqMedia.py
# Purpose: Parse xLights Sequence XML file and check for media errors
# Author: Bill Jenkins
# Version: v2.0
# Date: 08/16/2023

###########################
# Imports                 #
###########################

import xml.etree.ElementTree as ET
import argparse
import os
import sys
import re

###########################
# From Imports            #
###########################

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
# main                        #
###############################

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

    showFolder = os.path.abspath(args.showFolder)
    verbose = args.verbose
    if (verbose):
        print ("Show Folder = %s" % showFolder)

    if not os.path.isdir(showFolder):
        print ("Show folder not found %s" % showFolder)
        sys.exit(-1)

    # Path Case Sensitive Check
    if not (path_exists_case_sensitive(showFolder, verbose)):
        print("Error: xLights Show Folder case does not match %s" % showFolder)
        sys.exit(-1)

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
                                beginKey = EffectText.find(EffectKeyList[i])
                                if (beginKey > -1):
                                    endKey = EffectText[beginKey:lenEffectText].find("=")
                                    beginValue = beginKey + endKey + 1
                                    endValue = beginValue + EffectText[beginValue:lenEffectText].find(",")
                                    #if (verbose):
                                    #    print (" "* 4  + "EffectText=%s" % EffectText)
                                    #    print (" "* 4  + "i=%s beginKey=%s endKey=%s beginValue=%s endValue=%s" % (i, beginKey, endKey, beginValue, endValue))
                                    fullmediafile = EffectText[beginValue:endValue]
                                    splitfullmediafile = fullmediafile.split("\\")
                                    mediafile = splitfullmediafile[-1]
                                    #if (verbose):
                                    #    print (" "* 4  + "fullmediafile=%s" % fullmediafile)
                                    #    print (" "* 4  + "mediafile=%s" % mediafile)
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