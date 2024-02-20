# menuTitle: expand parametric range

import os, shutil, glob
import ufoProcessor
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, InstanceDescriptor, SourceDescriptor
from variableValues.measurements import FontMeasurements, permille

# see http://github.com/gferreira/amstelvar-avar2/issues/12

'''
set up a mini-designspace with three corner extrapolating the fourth. 
depending on the slightness factor and the below variable procedure;

blend an instance of the regular that's is 110% e.g. a value larger than the needed extension.

this forms the third side with:

a. default
b. current XTRA max
c. new 110% of default
d. get the corner and test.

'''

familyName       = 'AmstelvarA2'
subFamilyName    = ['Roman', 'Italic'][0]
baseFolder       = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder    = os.path.join(baseFolder, 'Sources', subFamilyName)
defaultName      = 'wght400'
defaultPath      = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{defaultName}.ufo')
measurementsPath = os.path.join(sourcesFolder, 'measurements.json')
designspacePath  = os.path.join(sourcesFolder, 'expand-range.designspace')

sources = glob.glob(f'{sourcesFolder}/*.ufo')

axisName1 = 'XTRA'
factor    = 0.9
direction = 1

# make new designspace document
D = DesignSpaceDocument()

# get axis min/max values from ufo file names
axisSources = []
values = []
for ufo in sorted(sources):
    if axisName1 in ufo:
        axisSources.append(ufo)
        value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
        values.append(value)

axisSource = axisSources[direction]
axisValueCurrent = values[direction]

# add main axis
a1 = AxisDescriptor()
a1.name    = axisName1
a1.tag     = axisName1
a1.minimum = 0.0
a1.maximum = 1.0
a1.default = 0.0
D.addAxis(a1)

# add default source
src1 = SourceDescriptor()
src1.path       = defaultPath
src1.familyName = familyName
src1.location = { axisName1 : 0.0 }
D.addSource(src1)

# add max source
src2 = SourceDescriptor()
src2.path       = axisSource
src2.familyName = familyName
src2.location = { axisName1 : 1.0 }
D.addSource(src2)

# add instance
styleName1 = 'instance1'
i1 = InstanceDescriptor()
i1.familyName     = familyName
i1.styleName      = styleName1
i1.name           = styleName1
i1.designLocation = { axisName1 : factor }
i1.filename       = os.path.join('instances', f'{styleName1}.ufo')
D.addInstance(i1)

# save designspace
D.write(designspacePath)

ufoProcessor.build(designspacePath)
instancePath1 = os.path.join(sourcesFolder, 'instances', f'{styleName1}.ufo')

assert os.path.exists(instancePath1)

# add scale axis
axisName2 = 'scale'
a2 = AxisDescriptor()
a2.name    = axisName2
a2.tag     = axisName2
a2.minimum = 0.0
a2.maximum = 1.0
a2.default = 0.0

D.addAxis(a2)

# add default scale location to current sources
for source in D.sources:
    source.location[axisName2] = a2.default

# add instance1 as source at max scale
src3 = SourceDescriptor()
src3.path       = instancePath1
src3.familyName = familyName
src3.location = { axisName1 : 0.0 , axisName2 : 1.0 }
D.addSource(src3)

# clear existing instance
D.instances = []

# add instance2 as new source at max scale
styleName2 = f"{axisName1}{['min', 'max'][direction]}"
i2 = InstanceDescriptor()
i2.familyName = familyName
i2.styleName  = styleName2
i2.name       = styleName2
i2.location   = { axisName1 : 1.0 , axisName2 : 1.0 }
i2.filename   = os.path.join('instances', f'{familyName}-{subFamilyName}_{styleName2}.ufo')
D.addInstance(i2)

# save the designspace again
D.write(designspacePath)

ufoProcessor.build(designspacePath)
instancePath2 = os.path.join(sourcesFolder, 'instances', f'{familyName}-{subFamilyName}_{styleName2}.ufo')

assert os.path.exists(instancePath2)

# get glyph order from default font
defaultFont = OpenFont(defaultPath, showInterface=False)
glyphOrder = defaultFont.glyphOrder
defaultFont.close()

# open generated font and set glyph order
f = OpenFont(instancePath2, showInterface=False)
f.glyphOrder = glyphOrder
f.save()

# get measurements from generated font
measurements = FontMeasurements()
measurements.read(measurementsPath)
measurements.measure(f)

print('old value:', axisValueCurrent)
print('new value:', permille(measurements.values[axisName1], f.info.unitsPerEm))
print()

# remove all generated files 
os.remove(designspacePath)
shutil.rmtree(instancePath1)
# shutil.rmtree(instancePath2)

# f.openInterface()
