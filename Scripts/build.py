import os, glob, shutil, json
from fontTools.designspaceLib import DesignSpaceDocument, AxisDescriptor, SourceDescriptor, InstanceDescriptor, AxisMappingDescriptor
from fontTools.subset import Subsetter
from fontTools.ttLib import TTFont
from defcon import Font
from ufo2ft import compileTTF, compileVariableTTF
import ufoProcessor # upgrade to UFOOperator
from variableValues.measurements import FontMeasurements, permille


SUBFAMILY = ['Roman', 'Italic'][0]


class AmstelvarA2DesignSpaceBuilder:
    '''
    Simple parametric designspace for use while designing.

    Specialized designspaces for output are created by subclassing this object.

    - parametric axes

    + builds instances from blends.json file
    + builds variable font

    '''
    familyName      = 'AmstelvarA2'
    subFamilyName   = SUBFAMILY
    defaultName     = 'wght400'
    parametricAxes  = 'XOPQ XTRA YOPQ YTUC YTLC YTAS YTDE YTFI XSHU YSHU XSVU YSVU XSHL YSHL XSVL YSVL XSHF YSHF XSVF YSVF XTTW YTTL YTOS XUCS'.split()
    designspaceName = f'{familyName}-{subFamilyName}.designspace'

    def __init__(self):
        # get measurements for default source
        f = OpenFont(self.defaultUFO, showInterface=False)
        self.unitsPerEm = f.info.unitsPerEm
        self.measurementsDefault = FontMeasurements()
        self.measurementsDefault.read(self.measurementsPath)
        self.measurementsDefault.measure(f)
        f.close()

    @property
    def baseFolder(self):
        return os.path.dirname(os.getcwd())

    @property
    def sourcesFolder(self):
        return os.path.join(self.baseFolder, 'Sources', self.subFamilyName)

    @property
    def instancesFolder(self):
        return os.path.join(self.sourcesFolder, 'instances')

    @property
    def varFontsFolder(self):
        return os.path.join(self.baseFolder, 'Fonts')

    @property
    def varFontPath(self):
        return os.path.join(self.varFontsFolder, self.designspaceName.replace('.designspace', '.ttf'))

    @property
    def measurementsPath(self):
        return os.path.join(self.sourcesFolder, 'measurements.json')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    @property
    def designspacePath(self):
        return os.path.join(self.sourcesFolder, self.designspaceName)

    @property
    def parametricSources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultLocation(self):
        return { name: permille(self.measurementsDefault.values[name], self.unitsPerEm) for name in self.parametricAxes }

    @property
    def amstelvarFolder(self):
        # path to a local copy of http://github.com/gferreira/amstelvar
        return os.path.join(os.path.dirname(self.baseFolder), 'amstelvar')

    @property
    def amstelvarBlendsPath(self):
        return os.path.join(self.amstelvarFolder, self.subFamilyName, 'blends.json')

    @property
    def blendsPath(self):
        return os.path.join(self.sourcesFolder, 'blends.json')

    @property
    def blendedAxes(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['axes']

    @property
    def blendedSources(self):
        with open(self.blendsPath, 'r', encoding='utf-8') as f:
            blendsData = json.load(f)
        return blendsData['sources']

    def buildBlendsFile(self):
        # import blends data from the original Amstelvar
        with open(self.amstelvarBlendsPath, 'r', encoding='utf-8') as f:
            blendsDict = json.load(f)
        # redefine wght wdth extrema
        blendsDict['axes']['wght']['min'] = 200
        blendsDict['axes']['wght']['max'] = 800
        blendsDict['axes']['wdth']['min'] = 85
        # add XTSP axis
        blendsDict['axes']['XTSP'] = {
            "name"    : "XTSP",
            "default" : 0,
            "min"     : -100,
            "max"     : 100,
        }
        # get min/max values from file names
        values = []
        for ufo in self.parametricSources:
            if 'XUCS' in ufo:
                value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                values.append(value)
        assert len(values)
        values.sort()
        # add XTSP min source
        blendsDict['sources']['XTSP-100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP-100']['XUCS'] = values[0]
        # add XTSP max source
        blendsDict['sources']['XTSP100'] = self.defaultLocation.copy()
        blendsDict['sources']['XTSP100']['XUCS'] = values[1]
        # save modified data to AmstelvarA2 blends.json
        with open(self.blendsPath, 'w', encoding='utf-8') as f:
            json.dump(blendsDict, f, indent=2)

    def addParametricAxes(self):
        for name in self.parametricAxes:
            # get min/max values from file names
            values = []
            for ufo in self.parametricSources:
                if name in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    values.append(value)
            assert len(values)
            values.sort()

            # create axis
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = values[0]
            a.maximum = values[1]
            a.default = permille(self.measurementsDefault.values[name], self.unitsPerEm)

            self.designspace.addAxis(a)

    def addDefaultSource(self):
        src = SourceDescriptor()
        src.path       = self.defaultUFO
        src.familyName = self.familyName
        src.styleName  = self.defaultName
        src.location   = self.defaultLocation
        self.designspace.addSource(src)

    def addParametricSources(self):
        for name in self.parametricAxes:
            for ufo in self.parametricSources:
                if name in ufo:
                    src = SourceDescriptor()
                    src.path       = ufo
                    src.familyName = self.familyName
                    L = self.defaultLocation.copy()
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    src.styleName  = f'{name}{value}'
                    L[name] = value
                    src.location = L
                    self.designspace.addSource(src)

    def addInstances(self):
        for styleName in self.blendedSources.keys():
            L = self.defaultLocation.copy()
            for axis, value in self.blendedSources[styleName].items():
                L[axis] = value

            I = InstanceDescriptor()
            I.familyName     = self.familyName
            I.styleName      = styleName
            I.name           = styleName
            I.designLocation = L
            I.filename       = os.path.join('instances', f'{self.familyName}-{self.subFamilyName}_{styleName}.ufo')

            self.designspace.addInstance(I)

    def buildInstances(self, clear=True):

        if clear:
            instances = glob.glob(f'{self.instancesFolder}/*.ufo')
            for instance in instances:
                shutil.rmtree(instance)

        ufoProcessor.build(self.designspacePath)
        ufos = glob.glob(f'{self.instancesFolder}/*.ufo')

        # copy glyph order from default
        f = OpenFont(self.defaultUFO, showInterface=False)
        glyphOrder = f.glyphOrder
        f.close()

        for ufo in ufos:
            f = OpenFont(ufo, showInterface=False)
            f.glyphOrder = glyphOrder
            f.save()
            f.close()

    def addBlendedAxes(self):
        for tag in self.blendedAxes.keys():
            a = AxisDescriptor()
            a.name    = self.blendedAxes[tag]['name']
            a.tag     = tag
            a.minimum = self.blendedAxes[tag]['min']
            a.maximum = self.blendedAxes[tag]['max']
            a.default = self.blendedAxes[tag]['default']
            self.designspace.addAxis(a)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.buildBlendsFile()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addInstances()

    def save(self):

        if not self.designspace:
            return
        self.designspace.write(self.designspacePath)

    def buildVariableFont(self, subset=False):

        print(f'generating variable font for {self.designspaceName}...')

        D = DesignSpaceDocument()
        D.read(self.designspacePath)
        print(f'\tloading sources...')
        for src in D.sources:
            src.font = Font(src.path)

        print(f'\tcompiling variable font...')
        f = compileVariableTTF(D, featureWriters=[])
        f.save(self.varFontPath)

        assert os.path.exists(self.varFontPath)

        # subset ascii variable font with pyftsubset
        if subset:
            print('\tsubsetting variable font...')
            asciiGlyphs = 'space exclam quotedbl numbersign dollar percent ampersand quotesingle parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde'.split()
            font = TTFont(self.varFontPath)
            subsetter = Subsetter()
            subsetter.populate(glyphs=asciiGlyphs)
            subsetter.subset(font)
            font.save(self.varFontPath)

        print('...done.\n')


class AmstelvarA2DesignSpaceBuilder_avar1(AmstelvarA2DesignSpaceBuilder):
    '''
    Designspace for building an avar1 variable font.

    - parametric axes
    - blended axes: opsz wght wdth (XTSP)
    - wght/wdth extrema defined by instances

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar1.designspace')

    def addBlendedSources(self):
        for tag in self.blendedAxes.keys():
            axisName = self.blendedAxes[tag]['name']
            valueMin = self.blendedAxes[tag]['min']
            valueMax = self.blendedAxes[tag]['max']
            for value in [valueMin, valueMax]:
                ufoPath = os.path.join(self.instancesFolder, f'{self.familyName}-{self.subFamilyName}_{tag}{value}.ufo')
                if not os.path.exists(ufoPath):
                    print(f'font {ufoPath} does not exist')
                L = self.defaultLocation.copy()
                L[axisName] = value
                src = SourceDescriptor()
                src.path       = ufoPath
                src.familyName = self.familyName
                src.styleName  = f'{tag}{value}'
                src.location   = L
                self.designspace.addSource(src)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.addBlendedSources()


class AmstelvarA2DesignSpaceBuilder_avar2(AmstelvarA2DesignSpaceBuilder):
    '''
    Designspace for building an avar2 variable font.

    - parametric axes
    - XTSP
    - blended axes: wght wdth
    - wght/wdth extrema defined by avar2 <mappings>

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2.designspace')

    def addMappings(self):

        blendedAxes    = self.blendedAxes
        blendedSources = self.blendedSources

        for styleName in blendedSources.keys():
            m = AxisMappingDescriptor()

            # get input value from style name
            inputLocation = {}
            for param in styleName.split('_'):
                tag   = param[:4]
                value = int(param[4:])
                axisName  = blendedAxes[tag]['name']
                inputLocation[axisName] = value

            # get output value from blends.json file
            outputLocation = {}
            for axisName in blendedSources[styleName]:
                outputLocation[axisName] = int(blendedSources[styleName][axisName])

            m.inputLocation  = inputLocation
            m.outputLocation = outputLocation

            self.designspace.addAxisMapping(m)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addDefaultSource()
        self.addParametricSources()


class AmstelvarA2DesignSpaceBuilder_avar2_fences(AmstelvarA2DesignSpaceBuilder_avar2):
    '''
    Designspace which adds fences to the avar2 variable font.

    same as the avar2 build plus:

    - fences for the default (wght400)
    - fences for blended extrema (wght200 wght800 wdth85 wdth125)
    - limit min/max values for XOPQ YOPQ XTRA XTSP only

    '''

    designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_avar2_fences.designspace')

    @property
    def fencesPath(self):
        return os.path.join(self.sourcesFolder, 'fences.json')

    @property
    def fences(self):
        with open(self.fencesPath, 'r', encoding='utf-8') as f:
            fences = json.load(f)
        return fences

    def addMappingsFences(self):

        defaultName = 'wght400'

        # add fences for default (monovar)

        blendTag    = defaultName[:4]
        blendValue  = int(defaultName[4:])
        blendName   = self.blendedAxes[blendTag]['name']
        for tag in self.fences[defaultName]:
            # get min/max fence values
            valuesFence = [
                self.fences[defaultName][tag]['min'],
                self.fences[defaultName][tag]['max'],
            ]
            # get min/max parametric axis value from file names
            valuesAxis = []
            for ufo in self.parametricSources:
                if tag in ufo:
                    value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
                    valuesAxis.append(value)
            assert len(valuesAxis)
            valuesAxis.sort()
            # create mapping elements
            for i, valueFence in enumerate(valuesFence):
                valueAxis  = valuesAxis[i]
                m = AxisMappingDescriptor()
                m.inputLocation = {
                    blendName : blendValue,
                    tag       : valueAxis,
                }
                m.outputLocation = {
                    blendName : blendValue,
                    tag       : valueFence,
                }
                self.designspace.addAxisMapping(m)

        # add fences for extrema

        # for styleName in self.fences.keys():
        #     if styleName == defaultName:
        #         continue
        #     blendTag    = styleName[:4]
        #     blendValue  = int(styleName[4:])
        #     blendName   = self.blendedAxes[blendTag]['name']
        #     for tag in self.fences[styleName]:
        #         # get min/max fence values
        #         valuesFence = [
        #             self.fences[defaultName][tag]['min'],
        #             self.fences[defaultName][tag]['max'],
        #         ]
        #         # get min/max parametric axis value from file names
        #         valuesAxis = []
        #         for ufo in self.parametricSources:
        #             if tag in ufo:
        #                 value = int(os.path.splitext(os.path.split(ufo)[-1])[0].split('_')[-1][4:])
        #                 valuesAxis.append(value)
        #         assert len(valuesAxis)
        #         valuesAxis.sort()
        #         # create null mappings
        #         for i, valueFence in enumerate(valuesFence):
        #             valueAxis  = valuesAxis[i]
        #             m = AxisMappingDescriptor()
        #             m.inputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             m.outputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueFence,
        #             }
        #             self.designspace.addAxisMapping(m)

        #             m = AxisMappingDescriptor()
        #             m.inputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             m.outputLocation = {
        #                 blendName : blendValue,
        #                 tag       : valueAxis,
        #             }
        #             self.designspace.addAxisMapping(m)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addBlendedAxes()
        self.addParametricAxes()
        self.addMappings()
        self.addMappingsFences()
        self.addDefaultSource()
        self.addParametricSources()


class AmstelvarA2DesignSpaceInitializer(AmstelvarA2DesignSpaceBuilder):

    # designspaceName = AmstelvarA2DesignSpaceBuilder.designspaceName.replace('.designspace', '_init.designspace')

    @property
    def defaultLocation(self):
        return { name: 0 for name in self.parametricAxes }

    def addParametricAxes(self):
        for name in self.parametricAxes:
            a = AxisDescriptor()
            a.name    = name
            a.tag     = name
            a.minimum = -1.0
            a.maximum = 1.0
            a.default = 0
            self.designspace.addAxis(a)

    def addParametricSources(self):
        for name in self.parametricAxes:
            for value in ['min', 'max']:
                ufoPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{name}{value}.ufo')
                src = SourceDescriptor()
                src.path       = ufoPath
                src.familyName = self.familyName
                L = self.defaultLocation.copy()
                src.styleName  = f'{name}{value}'
                L[name] = -1.0 if value == 'min' else 1.0
                src.location = L
                self.designspace.addSource(src)

    def buildParametricSources(self):
        for name in self.parametricAxes:
            for value in ['min', 'max']:
                ufoPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{name}{value}.ufo')
                if os.path.exists(ufoPath):
                    shutil.rmtree(ufoPath)
                shutil.copytree(self.defaultUFO, ufoPath)

    def build(self):
        self.designspace = DesignSpaceDocument()
        self.addParametricAxes()
        self.addDefaultSource()
        self.addParametricSources()
        self.buildParametricSources()


# -----
# build
# -----

if __name__ == '__main__':

    # D = AmstelvarA2DesignSpaceBuilder()
    # D.build()
    # D.save()
    # D.buildInstances()

    # D0 = AmstelvarA2DesignSpaceInitializer()
    # D0.build()
    # D0.save()

    D1 = AmstelvarA2DesignSpaceBuilder_avar1()
    D1.build()
    D1.save()
    D1.buildVariableFont()

    D2 = AmstelvarA2DesignSpaceBuilder_avar2()
    D2.build()
    D2.save()
    D2.buildVariableFont()

    # D3 = AmstelvarA2DesignSpaceBuilder_avar2_fences()
    # D3.build()
    # D3.save()
    # D3.buildVariableFont()
