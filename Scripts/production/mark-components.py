# menuTitle: mark glyphs with components

'''
red    : nested components
blue   : multiple components
yellow : one component only

'''

alpha = 0.5

f = CurrentFont()

def getNestingLevels(g, levels=0):
    if g.components:
        levels += 1
        for c in g.components:
            if c.baseGlyph not in f:
                print(f'ERROR in "{g.name}": glyph {c.baseGlyph} not in font')
                continue
            baseGlyph = f[c.baseGlyph]
            levels = getNestingLevels(baseGlyph, levels)
    return levels

for g in f:
    g.markColor = None
    if not(g.components):
        continue
    if len(g.components) == 1:
        g.markColor = 1, 0.8, 0, alpha
    else:
        levels = getNestingLevels(g)
        if levels > 1:
            g.markColor = 1, 0, 0, alpha
        else:
            g.markColor = 0, 0.6, 1, alpha

f.changed()