# menuTitle: build glyphs in sources

from importlib import reload
import hTools3.modules.accents
reload(hTools3.modules.accents)

import os, glob
from glyphConstruction import ParseGlyphConstructionListFromString, GlyphConstructionBuilder
from hTools3.modules.accents import buildAccentedGlyphs

familyName    = 'AmstelvarA2'
subFamilyName = 'Roman'
baseFolder    = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(baseFolder, 'Sources', subFamilyName)
glyphConstructionPath = os.path.join(baseFolder, 'Sources', subFamilyName, f'{familyName}-{subFamilyName}.glyphConstruction')

glyphNames = ['esdescendercyr']
    
targetStyles = [os.path.splitext(os.path.split(f)[-1])[0].split('_')[-1] for f in glob.glob(f'{sourcesFolder}/*.ufo')]

# get glyph constructions
with open(glyphConstructionPath, 'r') as f:
    glyphConstructions = f.read()

for styleName in targetStyles:
    dstPath = os.path.join(sourcesFolder, f'{familyName}-{subFamilyName}_{styleName}.ufo')
    if not os.path.exists(dstPath):
        print(f'target font {dstPath} does not exist.\n')
    dstFont = OpenFont(dstPath, showInterface=False)

    print(f'building glyphs in {dstPath}...')
    buildAccentedGlyphs(dstFont, glyphNames, glyphConstructions, clear=True, verbose=True, autoUnicodes=False, indentLevel=1)

    print(f'\tsaving font...')
    dstFont.save()
    # dstFont.close()
    print()

