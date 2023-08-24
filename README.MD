# xLightsAUTO
xLights Python Automation Scripts

Author: Bill Jenkins  
Date: 08/24/2023 
Vesion: 2.1  

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
        `pip install xlsxwriter
- JSON Files
  - xlightsparms.json
  - wbfmts.json
  - uploadfppconfigs.json
  - uploadsequences.json
- Images
  - default-image.png
 

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
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -o    --outputfolder         ; Output Folder                ; default = "NONE"                               ; Required = False
    -n    --notepadopen          ; Notepad Open                 ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportModelsCSV.py -f exportModels -s "g:\xLights\Show\2021\Christmas"`

# Script: exportControllers.py
## Description:
Get information from xLights Networks XML File & REST API getControllers and export to Excel workbook

## Arguments:
    -s    --xlightsshowfolder        ; xLights Show Folder          ;                                                ; Required = True
    -xc   --closexlights             ; Close xLights                ; action = "store_true"                          ; Required = False
    -fmt  --wbFmtsFileName           ; Workbook Formats JSON File   ; default = "wbFmts.json"                        ; Required = False
    -o    --outputfolder             ; Export Workbook Folder       ; default = "DEFAULT"                            ; Required = False
    -wb   --wbName                   ; Workbook Name                ; default = "DEFAULT"                            ; Required = False
    -v    --verbose                  ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportControllers.py -s "g:\xLights\Show\2023\Christmas" -xc -v 

## Example:
`python checkSequences.py -s "g:\xLights\Show\Test Show" -c -v`

# Script: exportModels.py  
## Description:
Perform xLights REST API exportModelsCSV and output to folder.  **NOTE** If Output folder = "DEFAULT" outputs to a sub folder "exportModelsCSV" in the show folder otherwise the folder specified is used

## Arguments:

    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -f    --exportfilename       ; Export Models File Name      ; default = "DEFAULT"                            ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False
                
# Script: exportVideoPreviews.py

## Description:
Perform xLights REST API exportVideoPreview on all sequences in a show folder.  **NOTE** If output folder = "DEFAULT" outputs to a sub folder "exportVideoPreview" in the show folder otherwise the folder specified is used

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -o    --outputfolder         ; Export Video Output Folder   ; default = "DEFAULT"                            ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python exportVideoPreviews.py -s "g:\xLights\Show\2021\Christmas"`

# Script: renderAll.py
## Description:
Perform xLights REST API renderAll on all sequences in a show folder and sub folders

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

# Script: uploadControllers.py
## Description:
Perform xLights REST API uploadController using REST API ControllerIPs to obtain IP address of each controller

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadControllers.py -s "g:\xLights\Show\2021\Christmas"`

# Script: uploadFPPConfigs.py
## Description:
Perform xLights REST API uploadFPPConfig using parameters from am upload FPP Config JSON file

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadFPPConfigs.py -s "g:\xLights\Show\2021\Christmas" -v

## JSON Format

    valid values:
                <ip>     Valid IPv4 Address of controller and defined in xLights
                <udp>    ["none", "all", "proxy"]
                <models> ["true", "false"]
                <map>    ["true", "false"]

## Example:
			{"controllers": [{
					"ip": "192.168.0.10",
					"udp": "all",
					"models": "true",
					"map": "false"
					},
					"ip": "192.168.0.11",
					"udp": "none",
					"models": "false",
					"map": "false"
					},					
			]}

# Script: uploadSequences.py
## Description:
Perform xLights REST API uploadSequence on selected sequences in a show folder and sub folders using parameters from an upload sequence JSON file

## Arguments:
    -s    --xlightsshowfolder    ; xLights Show Folder          ;                                                ; Required = True
    -c    --closexlights         ; Close xLights                ; action = "store_true"                          ; Required = False
    -v    --verbose              ; Verbose logging              ; action = "store_true"                          ; Required = False

## Example:
`python uploadSequences.py -s "g:\xLights\Show\2022\Halloween" -v`

    
## valid values:
    <ip>     Valid IPv4 Address of controller and defined in xLights
    <media>  ["true", "false"]
    <format> ["v1", "v2std", "v2zlib", "v2uncompressedsparse", "v2uncompressed", "v2stdsparse", "v2zlibsparse"]
                    
## Example:
			{"controllers": [{
				"ip": "192.168.0.10",
				"media": "false",
				"format": "v2stdsparse"
				},
				{
				"ip": "192.168.0.11",
				"media": "false",
				"format": "v2stdsparse"
				}
			
			]}
