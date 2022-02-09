Python xLights REST API Scripts
Author: Bill Jenkins
Date: 02/07/2022
Vesion: 1.0

Environment:

    Windows 10 64bit
    Python: v3.10.2
    xLights: v2022.04 64bit

Requirements:
    xLights v2022.04+
        Enable xLights REST API
            File --> Preferences --> Output --> xFade/XSchedule --> Port A (49913) or Port B (49914)
    Python v3.10.2+
        download and install from python.org
        install requests package
            pip install requests

##################################
# Script: checkSequences.py      #
##################################

    Description:
            Perfom xLights REST API check sequence on all sequences in a specfied show folder and sub folders and copy output to a specified folder

    Arguments:
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

    Example(s):
    python checkSequences.py -s "g:\xlights\show\test show" -v

##################################
# Script: exportVideoPreviews.py #
##################################
    Description:
            Perfom xLights REST API exportVideoPreview on all sequences in a specfied show folder and sub folders to a specified folder

    Arguments:
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -o     --outputfolder        ; Check Sequence Output Folder ; default = "DEFAULT"                            ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

##################################
# Script: packageSequences.py    #
##################################
    Description:
            Perfom xLights REST API packageSequence on all sequences in a specfied show folder and sub folders

    Arguments:
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

##################################
# Script: remderAll.py           #
##################################
    Description:
            Perfom xLights REST API renderAll on all sequences in a specfied show folder and sub folders

    Arguments:
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

##################################
# Script: uploadSequences.py     #
##################################
    Description:
            Perfom xLights REST API uploadSequence on all sequences in a specfied show folder and sub folders using upload sequence csv file for parms

    Arguments:
        -u    --uploadcsvfile        ; Upload Sequence CSV File     ;                                                ; Required = True
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False


    Upload CSV Upload Sequence File Format

            <ip>,<media>,<format>
        
            valid values:
                        Comment  "#" must be first character
                        <ip>     Valid IPv4 Address of controller and defined in xLights
                        <media>  ["true", "false"]
                        <format> ["v1", "v2std", "v2zlib", "v2uncompressedsparse", "v2uncompressed", "v2stdsparse", "v2zlibsparse"]
                        
            example:    
                        ############################
                        # Upload Sequence CSV File #
                        ############################
                        # FPP Player
                        10.222.50.7,true,v2std
                        # FPP Remote
                        10.222.50.8,false,v2stdsparse

##################################
# Script: uploadFPPConfigs.py    #
##################################
    Description:
            Perfom xLights REST API uploadFPPConfigs using FPP Config csv file for parms

    Arguments:
        -u    --uploadcsvfile        ; Upload FPP Config CSV File   ;                                                ; Required = True
        -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
        -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
        -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
        -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
        -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

    Upload CSV FPP Config File Format

            <ip>,<udp>,<models>,<map>
        
            valid values:
                        Comment  "#" must be first character
                        <ip>     Valid IPv4 Address of controller and defined in xLights
                        <udp>    ["none", "all", "proxy"]
                        <models> ["true", "false"]
                        <map>    ["true", "false"]
            example:    
                        ##############################
                        # Upload FPP Config CSV File #
                        ##############################
                        # FPP Player
                        10.222.50.7,all,true,false
                        # FPP Remote
                        10.222.50.8,none,true,false



