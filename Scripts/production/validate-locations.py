import os
from fontTools.designspaceLib import DesignSpaceDocument

folder = os.path.dirname(os.path.dirname(os.getcwd()))
sourcesFolder = os.path.join(folder, 'Sources', 'Roman')
designspacePath = os.path.join(sourcesFolder, 'AmstelvarA2-Roman.designspace')

_instances = True
_sources   = False

assert os.path.exists(designspacePath)

doc = DesignSpaceDocument()
doc.read(designspacePath)

# validate instances
if _instances:
    axes = { axis.tag: axis for axis in doc.axes }
    for instance in doc.instances:
        print(instance.name)
        for axisName, value in instance.designLocation.items():
            axis = axes[axisName]
            if not axis.minimum <= value <= axis.maximum:
                print(f"!! {axisName} {value} ({axis.minimum} {axis.maximum}) {'-' if value < axis.minimum else '+' if value > axis.maximum else ''} ")
        print()

# validate sources
if _sources:
    locations = []
    for src in doc.sources:
        if src not in locations:
            locations.append(src.location)
        else:
            print(src.name, src.location)

