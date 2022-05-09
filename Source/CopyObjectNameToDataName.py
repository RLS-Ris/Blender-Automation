import bpy

objects = bpy.context.scene.objects

for obj in objects:
    if obj.type == "MESH":
        obj.data.name = obj.name
    
#obj.select_set(obj.type == "MESH")