# menuTitle: copy default glyphs to other sources

import os, glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from hTools3.modules.accents import buildAccentedGlyphs

familyName    = 'AmstelvarA2'
subFamilyName = ['Roman', 'Italic'][1]
sourceName    = 'wght400'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
sourcePath    = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{sourceName}.ufo')

assert os.path.exists(sourcePath)

glyphNames = [
    'Q',
]

targetStyles = [
    'XOPQmax',
    'XOPQmin',
    'XSHFmax',
    'XSHFmin',
    'XSHLmax',
    'XSHLmin',
    'XSHUmax',
    'XSHUmin',
    'XSVFmax',
    'XSVFmin',
    'XSVLmax',
    'XSVLmin',
    'XSVUmax',
    'XSVUmin',
    'XTRAmax',
    'XTRAmin',
    'XTTWmax',
    'XTTWmin',
    'XUCSmax',
    'XUCSmin',
    'YOPQmax',
    'YOPQmin',
    'YSHFmax',
    'YSHFmin',
    'YSHLmax',
    'YSHLmin',
    'YSHUmax',
    'YSHUmin',
    'YSVFmax',
    'YSVFmin',
    'YSVLmax',
    'YSVLmin',
    'YSVUmax',
    'YSVUmin',
    'YTASmax',
    'YTASmin',
    'YTDEmax',
    'YTDEmin',
    'YTFImax',
    'YTFImin',
    'YTLCmax',
    'YTLCmin',
    'YTOSmax',
    'YTOSmin',
    'YTTLmax',
    'YTTLmin',
    'YTUCmax',
    'YTUCmin',
]

sourceFont = OpenFont(sourcePath, showInterface=False)

for styleName in targetStyles:
    dstPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{styleName}.ufo')
    if not os.path.exists(dstPath):
        print(f'target font {dstPath} does not exist.\n')
    dstFont = OpenFont(dstPath, showInterface=False)

    print(f'copying glyphs to {dstPath}...')
    for glyphName in glyphNames:
        print(f'\tcopying {glyphName}...')
        dstFont.insertGlyph(sourceFont[glyphName], name=glyphName)

    print(f'\tsaving font...')
    dstFont.save()
    # dstFont.close()
    print()

