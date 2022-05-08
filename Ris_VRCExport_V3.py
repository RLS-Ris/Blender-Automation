'''
2021 RLS - @VR_Ris
Automated Blender Export for VRChat
Version 3.0

What this does:
Automatically selects, applies modifiers on, and joins the objects you wish to export, as well as converts the poses in your pose-library into shapekeys. This is meant to be used alongside a face rig to make visemes a lot easier to work with.

How to:
This script requires a collection in your scene named "Export", which within all meshes will have their modifiers applied using the prefix rules below. A mesh that has children in this collection will have their children joined on to them, so you can export more than one parent mesh if you need to.

Prefix rules for modifier names:
"KEEP_" Keeps the modifier on the object without applying it.
"TEMP_" Removes the modifier without applying it.
"SHAPE_" Applies the modifier as a shapekey.
A modifier with any other name will just be applied as usual.

i.e. A modifier called TEMP_Subdivision will be ignored and removed.
Your main armature modifiers should be using the KEEP_ prefix.

Your main mesh needs to be named "Body", and somewhere in the scene there needs to be an armature named "Armature" with a pose library for the pose conversion to work. Also, meshes that have their viewport visibility disabled will be excluded from the entire process.

In the pose library, pose names that start with the prefix "TEMP_" will NOT be converted to shapekeys.

Issues:
All objects and collections inside the "Export" collection need to be included in the "RenderLayer" view layer, otherwise it will throw an error.
'''

import bpy
from bpy import context

# Checks if the object is a mesh and applies all modifiers using the prefix rules.
def ApplyModifiers(o):
    if(o.type != "MESH"):
        return
    
    bpy.context.view_layer.objects.active = o
    
    for m in o.modifiers:
        
        # KEEP prefix leaves the modifier untouched.
        # i.e. KEEP_Example
        if m.name.startswith("KEEP"):
            continue
        
        # TEMP prefix removes the modifier without applying it.
        # i.e. TEMP_Example
        if m.name.startswith("TEMP_"):
            bpy.ops.object.modifier_remove(modifier=m.name)
            continue
        
        # SHAPE prefix applies the modifier as a shapekey.
        # i.e. SHAPE_Example
        if m.name.startswith("SHAPE_"):
            bpy.ops.object.modifier_apply_as_shapekey(modifier=m.name)
            continue
        
        # Otherwise apply the modifier as usual.
        bpy.ops.object.modifier_apply(modifier=m.name)

# Applies modifiers on each object in the selection and joins them to the active object.
def ApplyModifiersAndJoin(selection, objectToJoinTo):
    for i in selection:
        ApplyModifiers(i)
            
    bpy.context.view_layer.objects.active = objectToJoinTo 
    bpy.ops.object.join()
        
# Converts the poses found in the Pose Library to shapekeys on the selected object.
def ConvertPosesToShapeKeys(activeObject, morphArmature):
    obj = activeObject
    arm = morphArmature
    pl = arm.pose_library
    
    if pl == None:
        print("Pose library missing, skipping pose to shapekey conversion.")
        return
    
    poseList = pl.pose_markers
    
    def ApplyPose(i):
        bpy.context.view_layer.objects.active = arm
    
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        bpy.ops.pose.select_all(action='SELECT')
    
        bpy.ops.poselib.apply_pose(pose_index=i)

    def ConvertToShapeKey(p):
        bpy.context.view_layer.objects.active = obj
    
        if p.name.startswith("TEMP_") == False:
    
            mod = obj.modifiers.new(p.name, 'ARMATURE')
            mod.object = bpy.data.objects["Morph"]
    
            bpy.ops.object.modifier_apply_as_shapekey(modifier=p.name)
    
    def ResetPose():
        bpy.context.view_layer.objects.active = arm
    
        bpy.ops.object.mode_set(mode='POSE', toggle=False)
        bpy.ops.pose.select_all(action='SELECT')
    
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()
        bpy.ops.pose.loc_clear()
        
    #obj.shape_key_add(name="Basis")
    
    for i in range(len(poseList)):
        pose = poseList[i]
    
        ApplyPose(i);
        ConvertToShapeKey(pose)
    
    ResetPose()

def Main(exportCollectionName, bodyObjectName, morphArmatureName, convertPoses):
    
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')
    
    parentObjects = []
    singleObjects = []
    
    # Get all meshes in the collection that contain at least one child mesh.
    for obj in bpy.data.collections[exportCollectionName].all_objects:
        if obj.type == "MESH":
            if(len(obj.children)) > 0:
                for child in obj.children:
                    if(child.type == "MESH"):
                        #print(obj.name + " parent")
                        parentObjects.append(obj)
                        break
            else:
                #aprint(obj.name + " single")
                if(obj.parent != None):
                    if(obj.parent.type != "MESH"):
                        singleObjects.append(obj)
                else:
                    singleObjects.append(obj)
    
    # For each parent, select it and its children, apply their modifiers, and join them together.
    for parent in parentObjects:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = parent
        bpy.ops.object.select_grouped(type='CHILDREN')
        parent.select_set(True)
        
        selected = bpy.context.selected_objects
        ApplyModifiers(parent)
        ApplyModifiersAndJoin(selected, parent)
        
    # For each single object, just apply their modifiers.
    for single in singleObjects:
        print(single)
        ApplyModifiers(single)
    
    # Pose to shapekey conversion
    if convertPoses:
        ConvertPosesToShapeKeys(bpy.context.scene.objects[bodyObjectName], bpy.context.scene.objects[morphArmatureName])
    
    # Select all objects to be exported.
    bpy.ops.object.mode_set(mode='OBJECT')
    for obj in bpy.data.collections['Export'].all_objects:
        obj.select_set(True)
        
    print("Success. Selected objects are ready to be exported.")
    
Main(exportCollectionName="Export", bodyObjectName="Body", morphArmatureName="Morph", convertPoses=True)