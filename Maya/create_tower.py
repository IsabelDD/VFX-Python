import maya.cmds as cmds

def create_tower(name, width, heigth, number_levels):
    levels_list = create_levels(width, heigth, number_levels)

    final_tower = assemble_tower(name, levels_list)
    
    return final_tower


def create_levels(width, heigth, number):
    
    levels_list = base_level(width, heigth, number)
    
    for i in range(1, number):
         width_l = (0.8**i) * width
         name_l = "level{0}".format(str(i))
         level = cmds.polyCube(w=width_l, h=heigth, d=width_l, n=name_l) 

         ty = (heigth* i) + (heigth/2.0)
         cmds.setAttr("{0}.translate".format(level[0]), 0, ty, 0)
         levels_list[i]= level[0]
      
    return levels_list
    
def base_level(width, heigth, number):
    
    levels_list = list(range(number))
    
    name_l = "level0"
    level = cmds.polyCube(w=width, h=heigth, d=width, n=name_l) 
    ty = (heigth/2.0)
    cmds.setAttr("{0}.translate".format(level[0]), 0, ty, 0)
    levels_list[0]= level[0]
    
    return levels_list
   
  
def assemble_tower(name, levels):
    levels_grp=cmds.group(levels, name="levels_grp")
    
    return levels_grp


if __name__ == "__main__":
	#Create tower. Parameters: name, width/depth, heigth, number_levels
    final_tower = create_tower("test_tower", 20, 10, 10)
    print("Create final tower {0}".format(final_tower))