from importlib import reload
import variableValues.measurements
reload(variableValues.measurements)

import os, glob, shutil
from variableValues.measurements import FontMeasurements

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

allUFOs = glob.glob(f'{sourcesFolder}/*.ufo')

ignoreTags = ['wght', 'GRAD', 'XTSP']

preflight = False

for ufo in allUFOs:
    tag = os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][:4]
    if tag in ignoreTags:
        continue

    print(f'measuring {tag} in {os.path.split(ufo)[-1]}...')
    f = OpenFont(ufo, showInterface=False)

    # set family name
    f.info.familyName = f'{familyName} {subFamilyName}'

    m = FontMeasurements()
    m.read(measurementsPath)
    m.measure(f)
    newValue = m.values[tag]
    newValue1000 = round(newValue * 1000 / f.info.unitsPerEm)
    print(f'\tunits  = {newValue}')
    print(f'\tpermil = {newValue1000}')

    # set style name
    newStyleName = f'{tag}{newValue1000}'
    if newStyleName != f.info.styleName:
        print(f'\tstyle name: {f.info.styleName} --> {newStyleName}' )
        f.info.styleName = newStyleName

    # rename file name
    newFileName = f'{familyName}-{subFamilyName}_{newStyleName}.ufo'
    newFilePath = os.path.join(sourcesFolder, newFileName)
    if not preflight:
        f.save()
    f.close()

    if ufo != newFilePath:
        print(f'\tfile name: {os.path.split(ufo)[-1]} --> {newFileName}' )
        if not preflight:
            shutil.move(ufo, newFilePath)   

    print()
