# menuTitle: update sub-sources

import os, glob
from mojo.smartSet import readSmartSets
from variableValues.linkPoints import readMeasurements


class AmstelvarSubSourceUpdater:

    baseFolder       = os.getcwd()
    familyName       = 'AmstelvarA2'
    subFamilyName    = ['Roman', 'Italic'][0]
    defaultName      = 'wght400'
    sourcesFolder    = os.path.join(baseFolder, subFamilyName)
    smartSetsPath    = os.path.join(baseFolder, 'AmstelvarA2.roboFontSets')
    measurementsPath = os.path.join(sourcesFolder, 'measurements.json')

    def __init__(self):
        self.smartSets    = readSmartSets(self.smartSetsPath, useAsDefault=False, font=None)
        self.measurements = readMeasurements(self.measurementsPath)

    @property
    def sources(self):
        return glob.glob(f'{self.sourcesFolder}/*.ufo')

    @property
    def defaultUFO(self):
        return os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{self.defaultName}.ufo')

    def _updateAllGlyphsExcept(self, subAxis, setsExcept):

        # get min/max sources
        subValues = []
        for src in self.sources:
            if subAxis in src:
                value = int(os.path.splitext(os.path.split(src)[-1])[0].split('_')[-1][4:])
                subValues.append(value)
        assert len(subValues)
        subValues.sort()

        srcFont = OpenFont(self.defaultUFO, showInterface=False)

        exceptGlyphs = []
        for smartSet in self.smartSets:
            for group in smartSet.groups:
                if group.name in setsExcept:
                    exceptGlyphs += group.glyphNames

        for subValue in subValues:
            dstName = f'{subAxis}{subValue}'
            dstPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{dstName}.ufo')
            assert os.path.exists(dstPath)
            dstFont = OpenFont(dstPath, showInterface=False)
            print(f'copying default glyphs from {self.defaultName} to {dstName}...')
            for glyphName in srcFont.glyphOrder:
                if glyphName not in exceptGlyphs:
                    # print(f'\tcopying {glyphName}...')
                    dstFont.insertGlyph(srcFont[glyphName])
            # dstFont.save()
            dstFont.close()
            print()

        srcFont.close()

    def _updateSubGlyphs(self, subAxis, parentAxis, setsCopy, copyParent=True, copyDefault=False):

        # get min/max sources
        subValues = []
        for src in self.sources:
            if subAxis in src:
                value = int(os.path.splitext(os.path.split(src)[-1])[0].split('_')[-1][4:])
                subValues.append(value)
        assert len(subValues)
        subValues.sort()

        if copyParent:
            # get min/max parents
            parentValues = []
            for src in self.sources:
                if parentAxis in src:
                    value = int(os.path.splitext(os.path.split(src)[-1])[0].split('_')[-1][4:])
                    parentValues.append(value)
            assert len(parentValues)
            parentValues.sort()

            for i in range(len(subValues)):

                # get source font (parent)
                srcName = f'{parentAxis}{parentValues[i]}'
                srcPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{srcName}.ufo')
                assert os.path.exists(srcPath)
                srcFont = OpenFont(srcPath, showInterface=False)

                # get target font (sub-source)
                dstName = f'{subAxis}{subValues[i]}'
                dstPath = os.path.join(self.sourcesFolder, f'{self.familyName}-{self.subFamilyName}_{dstName}.ufo')
                assert os.path.exists(dstPath)
                dstFont = OpenFont(dstPath, showInterface=False)

                # copy glyphs from parent to sub-source
                print(f'copying parent glyphs from {srcName} to {dstName}...')
                for smartSet in self.smartSets:
                    for group in smartSet.groups:
                        if group.name in setsCopy:
                            print(f'\tcopying {group.name}...')
                            for glyphName in group.glyphNames:
                                if glyphName not in srcFont:
                                    continue
                                dstFont.insertGlyph(srcFont[glyphName])
                srcFont.close()
                # dstFont.save()
                dstFont.close()
                print()

        if copyDefault:
            self._updateAllGlyphsExcept(subAxis, setsCopy)

    # XOPQ

    def XOUC(self, copyParent=True, copyDefault=False):
        subAxis    = 'XOUC'
        parentAxis = 'XOPQ'
        copySets   = ['uppercase latin']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    def XOLC(self, copyParent=True, copyDefault=False):
        subAxis    = 'XOLC'
        parentAxis = 'XOPQ'
        copySets   = ['lowercase latin']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    def XOFI(self, copyParent=True, copyDefault=False):
        subAxis    = 'XOFI'
        parentAxis = 'XOPQ'
        copySets   = ['figures']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    # XTRA

    def XTUC(self, copyParent=True, copyDefault=False):
        subAxis    = 'XTUC'
        parentAxis = 'XTRA'
        copySets   = ['uppercase latin']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    def XTLC(self, copyParent=True, copyDefault=False):
        subAxis    = 'XTLC'
        parentAxis = 'XTRA'
        copySets   = ['lowercase latin']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    def XTFI(self, copyParent=True, copyDefault=False):
        subAxis    = 'XTFI'
        parentAxis = 'XTRA'
        copySets   = ['figures']
        self._updateSubGlyphs(subAxis, parentAxis, copySets, copyParent=copyParent, copyDefault=copyDefault)

    # YOPQ

    def YOUC(self, copyParent=True, copyDefault=False):
        pass

    def YOLC(self, copyParent=True, copyDefault=False):
        pass

    def YOFI(self, copyParent=True, copyDefault=False):
        pass

    # YTRA

    def YTUC(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'YTUC'
            exceptSets  = ['uppercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YTLC(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'YTLC'
            exceptSets  = ['lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YTAS(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'YTAS'
            exceptSets  = ['ascenders latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YTFI(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'YTFI'
            exceptSets  = ['figures']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    # XSHA

    def XSHU(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSHU'
            exceptSets = ['uppercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def XSHL(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSHL'
            exceptSets = ['lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def XSHF(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSHF'
            exceptSets = ['figures']
            self._updateAllGlyphsExcept(subAxis, exceptSets)
    # YSHA

    def YSHU(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSHU'
            exceptSets = ['uppercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YSHL(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSHL'
            exceptSets = ['lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YSHF(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSHF'
            exceptSets = ['figures']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    # XSVA

    def XSVU(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSVU'
            exceptSets = ['uppercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def XSVL(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSVL'
            exceptSets = ['lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def XSVF(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'XSVF'
            exceptSets = ['figures']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    # YSVA

    def YSVU(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSVU'
            exceptSets = ['uppercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YSVL(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSVL'
            exceptSets = ['lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YSVF(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis    = 'YSVF'
            exceptSets = ['figures']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    # traps

    def XTTW(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'XTTW'
            exceptSets  = ['traps uppercase latin', 'traps lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    def YTTL(self, copyDefault=True, **kwargs):
        if copyDefault:
            subAxis     = 'YTTL'
            exceptSets  = ['traps uppercase latin', 'traps lowercase latin']
            self._updateAllGlyphsExcept(subAxis, exceptSets)

    # overshoots

    def YTOS(self, copyDefault=True, **kwargs):
        pass

    # general methods

    def update(self, parameters, copyParent=True, copyDefault=False):
        for parameter in parameters:
            func = getattr(self, parameter)
            func(copyParent=copyParent, copyDefault=copyDefault)



if __name__ == '__main__':

    parameters = [
        "XOUC",
        "XOLC",
        "XOFI",
        "XTUC",
        "XTLC",
        "XTFI",
        "YTUC",
        "YTLC",
        "YTAS",
        "YTDE",
        "YTFI",
        "XSHU",
        "YSHU",
        "XSVU",
        "YSVU",
        "XSHL",
        "YSHL",
        "XSVL",
        "YSVL",
        "XSHF",
        "YSHF",
        "XSVF",
        "YSVF",
        "XTTW",
        "YTTL",
        "YTOS",
    ]

    U = AmstelvarSubSourceUpdater()
    U.update(parameters, copyParent=True, copyDefault=True)

