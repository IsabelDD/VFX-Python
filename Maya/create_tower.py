#Create a tower with input parameters
#The tower create with a 90% of diference in width and dept between levels but the same heigth
#
#Parameters: number of levels (number of levels of the tower, min 3, max 40). Width, Heigth, Depth (w,h,d min of 5 and max of 100)
#
#Author: Isabel Diaz Dominguez
#

import maya.cmds as cmds
import functools

def create_tower(name, width, heigth, depth, number_levels):
    levels_list = create_levels(width, heigth, depth, number_levels)

    final_tower = assemble_tower(name, levels_list)
    
    return final_tower


def create_levels(width, heigth, depth, number):
    
    levels_list = base_level(width, heigth, depth, number)
    
    for i in range(1, number):
         width_l = (0.8**i) * width
         depth_l= (0.8**i) * depth
         name_l = "level{0}".format(str(i))
         level = cmds.polyCube(w=width_l, h=heigth, d=depth_l, n=name_l) 

         ty = (heigth* i) + (heigth/2.0)
         cmds.setAttr("{0}.translate".format(level[0]), 0, ty, 0)
         levels_list[i]= level[0]
      
    return levels_list
    
def base_level(width, heigth, depth, number):
    
    levels_list = list(range(number))
    
    name_l = "level0"
    level = cmds.polyCube(w=width, h=heigth, d=depth, n=name_l) 
    ty = (heigth/2.0)
    cmds.setAttr("{0}.translate".format(level[0]), 0, ty, 0)
    levels_list[0]= level[0]
    
    return levels_list
   
  
def assemble_tower(name, levels):
    levels_grp=cmds.group(levels, name="levels_grp")
    
    return levels_grp

#
#UI FUNCTIONS
#
   
def createUI( pWindowTitle, pApplyCallback):
    
    windowID = "myWindowId"
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
        
    createBody(windowID, pWindowTitle, pApplyCallback)
    
    def cancelCallback ( *pArgs ):
        if cmds.window (windowID, exists=True):
            cmds.deleteUI(windowID)
            
    cmds.button( label='Cancel', command=cancelCallback)
    
    cmds.showWindow()
    
    
def createBody(windowID, pWindowTitle, pApplyCallback):
    cmds.window(windowID, title=pWindowTitle, sizeable=False)
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,125), (2,75)], columnOffset=[(1, 'right',5)]) 
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')  
    
    cmds.text(label="Number of levels: ") 
    numberField = cmds.intField( minValue=3, maxValue=40, value=3)   
    
    cmds.text(label="Width: ")
    widthField = cmds.intField( minValue=5, maxValue=100, value=5)  
     
    cmds.text(label="Heigth: ")
    heigthField = cmds.intField( minValue=5, maxValue=100, value=5)  
    
    cmds.text(label="Depth: ")
    depthField = cmds.intField( minValue=5, maxValue=100, value=5)  
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')
    
    cmds.button( label='Apply', command= functools.partial(pApplyCallback, numberField, widthField, heigthField, depthField))
    

def errorMessage(pWindowTitle, pApplyCallback):
    
    windowID = "windowErrorID"
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID, title=pWindowTitle, sizeable=False)
    cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,200)], columnOffset=[(1, 'right',5)]) 
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')  
    
    cmds.text(label="Input values incorrect") 
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')  
    
       
    def cancelCallback ( *pArgs ):
        if cmds.window (windowID, exists=True):
            cmds.deleteUI(windowID)
            
    cmds.button( label='Accept', command=cancelCallback)
    
    cmds.showWindow()
    
    
def applyCallback ( numberField, widthField, heigthField, depthField, *pArgs ):
    
    try:
    
        number = cmds.intField(numberField, query=True, value=True )
        width = cmds.intField(widthField, query=True, value=True )
        heigth = cmds.intField(heigthField, query=True, value=True )
        depth = cmds.intField(depthField, query=True, value=True )
        
        print ("Tower number levels {0}, width {1}, heigth {2}, depth {3}".format(number, width, heigth, depth))
        
        if (width or heigth or depth) < 5 :
             errorMessage('Error', applyCallback)
        elif (width or heigth or depth) > 100:
             errorMessage('Error', applyCallback)
        elif number < 3 or number > 40:
             errorMessage('Error', applyCallback) 
        else:
            final_tower = create_tower("test_tower", width, heigth, depth, number)
            print("Create final tower {0}".format(final_tower))
        
    except:
        errorMessage('Error', applyCallback)
    
    
    
createUI('Tower', applyCallback)