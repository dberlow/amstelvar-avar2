#menuTitle: convert XTSP values to XUCS

import os, json

def XTSP2XUCS(XTSP_value):
    XTSP_min     = -100
    XTSP_default = 0
    XTSP_max     =  100
    XUCS_min     = 109
    XUCS_default = 145
    XUCS_max     = 195
    XTSP_value_normalized = (XTSP_value - XTSP_min) / ( XTSP_max - XTSP_min )
    XUCS_value = XUCS_min + XTSP_value_normalized * ( XUCS_max - XUCS_min )
    return XUCS_value

baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', 'Roman')
fencesPath    = os.path.join(sourcesFolder, 'fences.json')

with open(fencesPath, 'r', encoding='utf-8') as f:
    fences = json.load(f)

fences_new = {}

for styleName in fences.keys():
    fences_new[styleName] = {}
    for tag in fences[styleName].keys():
        if tag == 'XTSP':
            fences_new[styleName]['XUCS'] = {}
            for key, value in fences[styleName][tag].items():
                fences_new[styleName]['XUCS'][key] = int(XTSP2XUCS(value))
        else:
            fences_new[styleName][tag] = fences[styleName][tag]

with open(fencesPath, 'w', encoding='utf-8') as f:
    json.dump(fences_new, f, indent=2)
