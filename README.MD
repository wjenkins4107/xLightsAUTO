# xLightsAUTO
xLights Python Automation Scripts

Author: Bill Jenkins  
Date: 08/12/2023 
Vesion: 4.0  

# Environment

Windows 11 64bit  
Python: v3.11.1  
xLights: v2023.11 64bit  

# Requirements:
- xLights v2023.11+
  - Enable xLights REST API
    - File --> Preferences --> Output --> xFade/XSchedule --> Port A (49913) or Port B (49914)
- Python v3.11.1+
  - download and install python from python.org
  - install requests package
        `pip install requests`
  - install xlsxwriter package
        `pip install xlsxwriter`


# Script: checkSeqMedia.py       #
Check sequence media (audio, images, shaders and videos) and verify that they exist, list any errors found and a summary for each sequence

## Arguments:
    -s    --xShowFolder           ; xLights Show Folder          ;                                               ; Required = True
    -v    --verbose               ; Verbose logging              ; action = "store_true"                         ; Required = False
## Example:
    python checkSeqMedia.py -s "g:\xlights\show\2023\christmas" -v

# Script: checkSequences.py

## Description:
Perform xLights REST API check sequence on all sequences in a show folder and sub folders, optionally copy the output to an output folder and optionally open the output file in notepad.

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -o    --outputfolder         ; Output Folder                ; default = "NONE"                               ; Required = False
    -n    --notepadopen          ; Notepad Open                 ; action = "store_true"                          ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python checkSequences.py -s "g:\xLights\Show\Test Show" -c -v`

# Script: exportModelsCSV.py  
## Description:
Perform xLights REST API exportModelsCSV and output to folder.  **NOTE** If Output folder = "DEFAULT" outputs to a sub folder "exportModelsCSV" in the show folder otherwise the folder specified is used

## Arguments:
    -f    --exportfilename       ; Export Models File Name      ;                                                ; Required = True
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -o    --outputfolder         ; Export Output folder         ; default = "DEFAULT"                            ; Required = False
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportModelsCSV.py -f exportModels -s "g:\xLights\Show\2021\Christmas"`

# Script: exportControllers.py
## Description:
Get information from xLights Networks XML File & REST API getControllers and export to Excel workbook

## Arguments:
    -s    --xlightsshowfolder        ; xLights Show Folder          ;                                                ; Required = True
    -xi   --xlightsipaddress         ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -xp   --xlightsport              ; xLights REST API Port        ; default = "A" ; choices = "A", "B"             ; Required = False
    -xf   --xlightsprogramfolder     ; xLights Program Folder       ; default = "c:\\program files\\xlights"         ; Required = False
    -xpgm --xlightsprogram           ; xLights Program              ; default = "\\xlights.exe"                      ; Required = False
    -xc   --closexlights             ; Close xLights                ; action = "store_true"                          ; Required = False
    -xml  --xlightsNetworksXmlFile   ; xLights Networks XML File    ; default = "xlights_networks.xml"               ; Required = False
    -fmt  --dwbFmtsFileName          ; Workbook Formats JSON File   ; default = "dwbFmts.json"                       ; Required = False
    -wb   --wbName                   ; Workbook Name                ; default = "DEFAULT"                            ; Required = False
    -v    --verbose                  ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportControllers.py -s "g:\xLights\Show\2023\Christmas" -xc -v`
                  
# Script: exportVideoPreviews.py

## Description:
Perform xLights REST API exportVideoPreview on all sequences in a show folder.  **NOTE** If output folder = "DEFAULT" outputs to a sub folder "exportVideoPreview" in the show folder otherwise the folder specified is used

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -o    --outputfolder         ; Export Video Output Folder   ; default = "DEFAULT"                            ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportVideoPreviews.py -s "g:\xLights\Show\2021\Christmas"`

# Script: renderAll.py
## Description:
Perform xLights REST API renderAll on all sequences in a show folder and sub folders

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

# Script: uploadControllers.py
## Description:
Perform xLights REST API uploadController using REST API ControllerIPs to obtain IP address of each controller

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadControllers.py -s "g:\xLights\Show\2021\Christmas"`

# Script: uploadFPPConfigs.py
## Description:
Perform xLights REST API uploadFPPConfig using parameters from am upload FPP Config csv file

## Arguments:
    -u    --uploadcsvfile        ; Upload FPP Config CSV File   ;                                                ; Required = True
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadFPPConfigs.py -u "g:\xLights\Show\Auto\uploadfpp.csv" -s "g:\xLights\Show\2021\Christmas" -v`

## CSV Format

    <ip>,<udp>,<models>,<map>

    valid values:
                Comment  "#" must be first character
                <ip>     Valid IPv4 Address of controller and defined in xLights
                <udp>    ["none", "all", "proxy"]
                <models> ["true", "false"]
                <map>    ["true", "false"]
    Example:    
                ##############################
                # Upload FPP Config CSV File #
                ##############################
                # FPP Player
                10.222.50.7,all,true,false
                # FPP Remote
                10.222.50.8,none,true,false

# Script: uploadSequences.py
## Description:
Perform xLights REST API uploadSequence on all sequences in a show folder and sub folders using parameters from an upload sequence csv file

## Arguments:
    -u    --uploadcsvfile        ; Upload Sequence CSV File     ;                                                ; Required = True
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadSequences.py -u "g:\xLights\Show\Auto\uploadseq.csv" -s "g:\xLights\Show\2021\Christmas" -v`

## Upload CSV Upload Sequence File Format

    <ip>,<media>,<format>
    
## valid values:
    Comment  "#" must be first character
    <ip>     Valid IPv4 Address of controller and defined in xLights
    <media>  ["true", "false"]
    <format> ["v1", "v2std", "v2zlib", "v2uncompressedsparse", "v2uncompressed", "v2stdsparse", "v2zlibsparse"]
                    
## Example:    
    ############################
    # Upload Sequence CSV File #
    ############################
    # FPP Player
    10.222.50.7,true,v2std
    # FPP Remote
    10.222.50.8,false,v2stdsparse
