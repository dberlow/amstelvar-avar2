import os, glob
from fontTools.ttLib import TTFont

baseFolder  = os.path.dirname(os.path.dirname(os.getcwd()))
fontsFolder = os.path.join(baseFolder, 'Fonts')

ttfPaths = glob.glob(f'{fontsFolder}/*.ttf')

for ttfPath in ttfPaths:
    ttxPath = ttfPath.replace('.ttf', '.ttx')
    f = TTFont(ttfPath)
    f.saveXML(ttxPath)
    f.close()
