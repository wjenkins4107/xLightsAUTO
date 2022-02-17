# xLightsAUTO
xLights Python Automation Scripts

Author: Bill Jenkins
Date: 02/15/2022
Vesion: 1.1

# Environment

Windows 10 64bit
Python: v3.10.2
xLights: v2022.04 64bit

# Requirements:
- xLights v2022.04+
  - Enable xLights REST API
    - File --> Preferences --> Output --> xFade/XSchedule --> Port A (49913) or Port B (49914)
- Python v3.10.2+
  -   download and install from python.org
  - install requests package
        `pip install requests`

# Script: checkFaceInfo.py
## Description:
Check faceInfo element attributes in models/model of the xlights_rgbeffects.xml file that are for a matrix type,  list any errors found and optionally remove any faceInfo elements with errors and write updated RGB Effects File to a new timestamped xrgb_<timestamp>_xlights_rgbeffects.xml in the show folder

## Arguments:
    -s    --xShowFolder           ; xLights Show Folder          ;                                               ; Required = True
    -x    --xrgbEffectsXMLFile    ; xLights RGB Effects XML File ; default = "xlights_rgbeffects.xml"            ; Required = False
    -r    --removeFaceInfoElement ; FSEQ Folder                  ; default = "FSEQ"                              ; Required = False
    -v    --verbose               ; Verbose logging              ; action = "store_true"                         ; Required = False

## Example:
`python checkFaceInfo.py -s "g:\xlights\show\2021\christmas"`

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
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python checkSequences.py -s "g:\xlights\show\test show" -v`

# Script: createShowFolder.py
## Description:
Create new show folder from existing show folder, create folders for backup, FSEQ, Render Cache if needed, copy shaders from old show folder to new show folder, copy background image file to new show folder, update backgroundImage, backupDir, fseqDir and renderCacheDir settings and write updated XML tree to xlights_rgbeffects.xml file in new show folder.

## Arguments:
    -o    --oldShowFolder        ; Old Show Folder              ;                                                ; Required = True
    -n    --newShowFolder        ; New Show Folder              ;                                                ; Required = True
    -b    --backupFolder         ; Backup Folder                ; default = "Backup"                             ; Required = False
    -f    --fseqFolder           ; FSEQ Folder                  ; default = "FSEQ"                               ; Required = False
    -r    --renderCachefolder    ; Render Cache Folder          ; default = "RenderCache"                        ; Required = False
    -s    --shadersfolder        ; shaders Folder               ; default = "Shaders"                            ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python createShowFolder.py -o "g:\xlights\show\2021\christmas" -n "g:\xlights\show\2022\christmas"`

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
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportModelsCSV.py -f exportModels -s "g:\xlights\show\2021\christmas"`

# Script: exportVideoPreviews.py

## Description:
Perform xLights REST API exportVideoPreview on all sequences in a show folder.  **NOTE** If output folder = "DEFAULT" outputs to a sub folder "exportVideoPreview" in the show folder otherwise the folder specified is used

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -o    --outputfolder         ; Export Video Output Folder   ; default = "DEFAULT"                            ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportVideoPreviews.py -s "g:\xlights\show\2021\christmas"`


# Script: mergeFaces.py
## Description:
Parse the faceinFo element attributes for type matrix and merge face image files into one folder, update the faceinFo element attributes and write to a new timestamped xrgb_<timestamp>_xlights_rgbeffects.xml file in the show folder.  **NOTE** If faces folder = "DEFAULT" a "Faces" subfolder in the show folder is used otherwise the specified folder is used

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -f   --facesFolder           ; Merged Faces Folder          ; default = "DEFAULT"                            ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python mergeFaces.py -s "g:\xlights\show\2021\christmas" -v`


# Script: remderAll.py
## Description:
Perform xLights REST API renderAll on all sequences in a show folder and sub folders

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

# Script: uploadControllers.py
## Description:
Perform xLights REST API uploadController using REST API ControllerIPs to obtain IP address of each controller

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadControllers.py -s "g:\xlights\show\2021\christmas"`

# Script: uploadFPPConfigs.py
## Description:
Perform xLights REST API uploadFPPConfig using parameters from am upload FPP Config csv file

## Arguments:
    -u    --uploadcsvfile        ; Upload FPP Config CSV File   ;                                                ; Required = True
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -i    --xlightsipaddress     ; xLights REST API IP Address  ; default = "127.0.0.1"                          ; Required = False
    -p    --xlightsport          ; xLights REST API Port        ; default = "49913" ; choices = "49913", "49914" ; Required = False
    -x    --xlightsprogramfolder ; xLights Program Folder       ; default = "c:\program files\xlights"           ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadFPPConfigs.py -u "g:\xlights\show\auto\uploadfpp.csv" -s "g:\xlights\show\2021\christmas" -v`

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
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadSequences.py -u "g:\xlights\show\auto\uploadseq.csv" -s "g:\xlights\show\2021\christmas" -v`

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