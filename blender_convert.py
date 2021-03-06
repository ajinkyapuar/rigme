import bpy
import os
import glob
import argparse

def loadInfo(info_name, geo_name):
	#setting up the blender rig
	armature = bpy.data.armatures.new("Armature")
	rig = bpy.data.objects.new("Armature", armature)
	context.scene.collection.objects.link(rig)

	context.view_layer.objects.active = rig
	bpy.ops.object.editmode_toggle()
	current_bone = armature.edit_bones.new(bone[0])

    f_info = open(info_name,'r')
    joint_pos = {}
    joint_hier = {}
    joint_skin = []
    for line in f_info:
        word = line.split()
        if word[0] == 'joints':
            joint_pos[word[1]] = [float(word[2]),  float(word[3]), float(word[4])]
        if word[0] == 'root':
            root_pos = joint_pos[word[1]]
            root_name = word[1]
            # this is setting up the root position of the joint
            #cmds.joint(p=(root_pos[0], root_pos[1],root_pos[2]), name = root_name)
            # root bone in chain
			# create bone at armature origin and set its length
			
			current_bone.head = root_pos
			#need to figure out how the rest of the ifnormation belo needs to be filled out
			'''
			length = list(bones.values())[i+1][0][1]
			current_bone.tail = [0, 0, length]

			# rotate bone
			quat_armature_space = Quaternion(bone[1][1])
			current_bone.transform(quat_armature_space.to_matrix())
			        
			# set position
			current_bone.translate(Vector(bone[1][0]))

			# save bone, its tail position (next bone will be moved to it) and quaternion rotation
			parent_bone = current_bone
			parent_bone_tail = current_bone.tail
			parent_bone_quat_armature_space = quat_armature_space'''
        if word[0] == 'hier':
            if word[1] not in joint_hier.keys():
                joint_hier[word[1]] = [word[2]]
            else:
                joint_hier[word[1]].append(word[2])
        if word[0] == 'skin':
            skin_item = word[1:]
            joint_skin.append(skin_item)
    f_info.close()

    # below is the code in order to implement bone making in the rig for blender need to implement for the current problem
    '''
	for i, bone in enumerate(bones.items()):
	    # create new bone
	    current_bone = armature.edit_bones.new(bone[0])
	        
	    # last bone in chain
	    elif i == (len(bones) - 1):
	        # create bone at armature origin and set its length
	        current_bone.head = [0, 0, 0]
	        current_bone.tail = [0, 0, 1]
	        
	        # rotate bone
	        current_bone_quat_parent_space = Quaternion(bone[1][1])
	        # like matrices, quaternions can be multiplied to accumulate rotational values
	        transform_quat = parent_bone_quat_armature_space @ current_bone_quat_parent_space
	        current_bone.transform(transform_quat.to_matrix())

	        # set position
	        current_bone.translate(Vector(parent_bone_tail))
	        
	        # connect
	        current_bone.parent = parent_bone
	        current_bone.use_connect = True
	        
	    else:
	        # create bone at armature origin and set its length
	        current_bone.head = [0, 0, 0]
	        length = list(bones.values())[i+1][0][1]
	        current_bone.tail = [0, 0, length]
	        
	        # rotate bone
	        current_bone_quat_parent_space = Quaternion(bone[1][1])
	        # like matrices, quaternions can be multiplied to accumulate rotational values
	        transform_quat = parent_bone_quat_armature_space @ current_bone_quat_parent_space
	        current_bone.transform(transform_quat.to_matrix())
	        
	        # set position
	        current_bone.translate(Vector(parent_bone_tail))
	        
	        # connect
	        current_bone.parent = parent_bone
	        current_bone.use_connect = True
	        
	        # save bone, its tail position (next bone will be moved to it) and quaternion rotation
	        parent_bone = current_bone
	        parent_bone_tail = current_bone.tail
	        parent_bone_quat_armature_space = transform_quat

	bpy.ops.object.editmode_toggle()
	'''

    '''
    keeping the above code because it parses the _rig.txt file into its appropriate dictionary/list
    ToDo: must fix the below code into belender using the parsing above.
    this_level = [root_name]
    while this_level:
        next_level = []
        for p_node in this_level:
            if p_node in joint_hier.keys():
                for c_node in joint_hier[p_node]:
                    cmds.select(p_node, r=True)
                    child_pos = joint_pos[c_node]
                    cmds.joint(p=(child_pos[0], child_pos[1],child_pos[2]), name = c_node)
                    next_level.append(c_node)
        this_level = next_level         
    
    cmds.skinCluster( root_name, geo_name)
    #print len(joint_skin)
    for i in range(len(joint_skin)):
        vtx_name = geo_name + '.vtx['+joint_skin[i][0]+']'
        transValue = []
        for j in range(1,len(joint_skin[i]),2):
            transValue_item = (joint_skin[i][j], float(joint_skin[i][j+1]))
            transValue.append(transValue_item) 
        #print vtx_name, transValue
        cmds.skinPercent( 'skinCluster1', vtx_name, transformValue=transValue)
    cmds.skinPercent( 'skinCluster1', geo_name, pruneWeights=0.01, normalize=False )
    '''
    return root_name, joint_pos


def getGeometryGroups():
	#right now my understanding of the code below is that we are finding the shape origin coordinates
    geo_list = []
    bpy.ops.object.select_all( action = 'SELECT' )
	bpy.ops.object.origin_set( type = 'ORIGIN_GEOMETRY' )

	obj_object = bpy.context.selected_objects[0]
	geo_list.append(obj_object.location)
    '''
	Need to replace below code into blender

    geometries = cmds.ls(type='surfaceShape')
    for geo in geometries:
        if 'ShapeOrig' in geo:
            '''
            #we can also use cmds.ls(geo, l=True)[0].split("|")[0]
            #to get the upper level node name, but stick on this way for now
            '''
            geo_name = geo.replace('ShapeOrig', '')
            geo_list.append(geo_name)
    if not geo_list:
        geo_list = cmds.ls(type='surfaceShape')
        '''
    return geo_list

def run(model_id,input_folder):
    print(model_id)
    obj_name = os.path.join(input_folder, '{:s}_remesh.obj'.format(model_id))
    info_name = os.path.join(input_folder, '{:s}_remesh_rig.txt'.format(model_id))
    out_name = os.path.join(input_folder, '{:s}.fbx'.format(model_id))
       
    # import obj
    #cmds.file(new=True,force=True)
    #cmds.file(obj_name, o=True)
    imported_object = bpy.ops.import_scene.obj(filepath=obj_name)

    # import info
    geo_list = getGeometryGroups()
    root_name, _ = loadInfo(info_name, geo_list[0])
    
    '''
    need to convert below code into blender
    for j in cmds.ls(type="joint"):
        cmds.setAttr(j + ".segmentScaleCompensate", 0)
        #otherwise try Scale instead of .segmentScale
        cmds.scale(1, 1, 1, j)

    selObj = root_name
    cmds.scale(1, 1, 1, selObj)

    # export fbx
    pm.mel.FBXExport(f=out_name)'''

if __name__ == '__main__':
    #model_id = "17872"
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=str, required=True)
    parser.add_argument('-i', '--input_folder', type=str, required=True)
    args = parser.parse_args()
    run(args.id, args.input_folder)