#########################
# DESCRIPCION: UI to rename select elements in the scene and also group with a input name
#
#
# AUTHOR: Isabel Diaz Dominguez
#

import maya.cmds as cmds
import functools

def lineSeparation():
    cmds.separator(h=10, style='none')
    cmds.separator(h=10, style='none')  

def createBody(windowID, pWindowTitle, pApplyCallback):
    cmds.window(windowID, title=pWindowTitle, sizeable=False)
    cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1,150), (2,150)], columnOffset=[(1, 'right',5), (2, 'left',5)]) 
    
    lineSeparation()  
    
    cmds.text(label="Name: ")
    nameReplaceField = cmds.textField()
    lineSeparation()
    
    cmds.text(label="Prefix to add: ")
    prefixField = cmds.textField()
    lineSeparation()
    
    cmds.text(label="Sufix to add: ")
    sufixField = cmds.textField()
    lineSeparation()
    
    cmds.text(label="Group name: ")
    groupNameField = cmds.textField()
    lineSeparation()
   
   
    cmds.text(label="Enumerate : ")
    enumerateControl = cmds.radioCollection()
    trueValue = cmds.radioButton( label='Yes')
    cmds.separator(h=10, style='none')
    falseValue = cmds.radioButton( label='No')
    enumerateControl = cmds.radioCollection(enumerateControl, edit=True, select=trueValue)
    lineSeparation()
  
    cmds.button( label='Apply', command= functools.partial(pApplyCallback, nameReplaceField, 
        prefixField, sufixField, groupNameField, enumerateControl))
      

def createUI(pWindowTitle, pApplyCallback):
    
    windowID = 'renameWindowID'
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
        
    createBody(windowID, pWindowTitle, pApplyCallback)
    
    def cancelCallback( *pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    
    cmds.button( label= 'Cancel', command= cancelCallback) 
    lineSeparation()
    
    cmds.showWindow()
   

def errorMessage(pWindowTitle, message):
    
    print('Error')
    
    windowID = "windowErrorID"
    
    if cmds.window(windowID, exists = True):
        cmds.deleteUI(windowID)
    
    cmds.window(windowID, title=pWindowTitle, sizeable=False)
    cmds.rowColumnLayout(numberOfColumns=1, columnWidth=[(1,100)], columnOffset=[(1, 'right',5), (1, 'left',2)]) 
    cmds.separator(h=10, style='none')
    
    cmds.text(label=message) 
    
    cmds.separator(h=10, style='none')
    
    cmds.showWindow()


def applyCallback ( nameReplaceField, prefixField, sufixField, groupNameField, enumerateControl, *pArgs):
    
    name = cmds.textField( nameReplaceField, query=True, text=True)
    prefix = cmds.textField( prefixField, query=True, text=True)
    sufix = cmds.textField( sufixField, query=True, text=True)   
    groupName = cmds.textField( groupNameField, query=True, text=True)
    enumerateCol = cmds.radioCollection(enumerateControl, query=True, sl=True)
    enumerateValue = cmds.radioButton(enumerateCol, query=True, label=True)    
    
    list = cmds.ls( selection=True )
    
    if len(list) > 0:
        if enumerateValue == 'Yes':
            enum = '_' + str(count+1)
        else: 
            enum = ''

        if groupName:
            cmds.group(list, name=groupName)
            
        for count,obj in enumerate(list):  
            if not name and prefix and sufix:
                cmds.rename(obj, prefix + '_' + obj + '_' + sufix + enum) 
            elif not name and prefix and not sufix:
                cmds.rename(obj, prefix + '_' + obj + enum)
            elif not name and not prefix and sufix:
                cmds.rename(obj, obj + sufix + enum)  
            elif name and prefix and sufix:
                cmds.rename(obj, prefix + '_' + name + '_' + sufix + enum)
            elif name and prefix and not sufix:
                cmds.rename(obj, prefix + '_' + name + enum)
            elif name and not prefix and sufix:
                cmds.rename(obj, name + '_' + sufix + enum)
            elif name and not prefix and not sufix:
                cmds.rename(obj, name + enum)             
    else:
       errorMessage('Warning', 'Nothing selected') 
             
    
createUI('Rename', applyCallback)