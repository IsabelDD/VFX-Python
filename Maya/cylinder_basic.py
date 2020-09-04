import maya.cmds as cmds

#create cylinder 8 subdivisions axis
cylinder = cmds.polyCylinder(sx=8, sy=1, sz=1);

#select edges
cmds.polySelect( cylinder, edgeRing=(24, 26, 28, 30, 32, 34, 36, 38));

#delete selection
cmds.delete();