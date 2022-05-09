import bpy
from bpy import context

armature = bpy.context.view_layer.objects.active

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        for mod in obj.modifiers:
            if(mod.type == 'ARMATURE'):
                if(mod.object == None):
                    break
                if(mod.object.name == armature.name):
                    print(mod.object.name + ", " + armature.name)

                    d = obj.modifiers.new("CloneArmature", type='ARMATURE')
                    d.object = armature
                    
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.modifier_apply(modifier=d.name)

bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE', toggle=False)
bpy.ops.pose.select_all(action='SELECT')
bpy.ops.pose.armature_apply(selected=False)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='DESELECT')