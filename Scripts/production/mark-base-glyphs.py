# menuTitle: find unused components

f = CurrentFont()

color = 1, 0, 1, 0.5

baseGlyphs = []

for g in f:
    g.markColor = None
    for c in g.components:
        if c.baseGlyph in baseGlyphs:
            continue
        baseGlyphs.append(c.baseGlyph)

for baseGlyph in baseGlyphs:
    f[baseGlyph].markColor = color