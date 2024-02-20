import glob
from hTools3.modules.encoding import setGlyphOrder

encFilePath  = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/AmstelvarA2.enc'
targetFolder = '/Users/gferreira/hipertipo/fonts/amstelvar-avar2/Source/Parametric-avar2/Roman'

ufoPaths = glob.glob(f'{targetFolder}/*.ufo')

for ufoPath in ufoPaths:
    font = OpenFont(ufoPath, showInterface=False)
    print(f'setting glyph order in {ufoPath}…')
    setGlyphOrder(font, encFilePath, verbose=False, createGlyphs=False)
    font.save()
    font.close()
