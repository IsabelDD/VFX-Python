#
# DESCRIPTION: Code that call to three diferent fuctions in Nuke to know some
# functionalities on it.
# AUTHOR: Isabel Diaz Dominguez
#

import nuke
import os
import webbrowser

#create two node network
def create_network():
    read_fg = nuke.nodes.Read()
    read_bg = nuke.nodes.Read()
    
    merge = nuke.nodes.Merge()
    write = nuke.nodes.Write()

    merge.setInput(0, read_bg)
    merge.setInput(1, read_fg)
    write.setInput(0, merge)

    #set path nodes // uncomment with a path avaliable
    #read_bg.knob('file').setValue('D:/Nuke/Durin_Door.png')
    #read_fg.knob('file').setValue('D:/Nuke/fog_1.jpg')
    #write.knob('file').setValue('D:/Nuke/finalResult.jpg')


#Open current scene folder
def open_sceneFolder():
    path = nuke.root().knob('name').value()
    print path
    path = os.path.dirname(path)  # withou path name
    print path
    webbrowser.open(path)


#Save
def save_scene():
    nuke.scriptSaveAs("D:/Nuke/test_nuke.nk")


create_network()
save_scene()
open_sceneFolder()