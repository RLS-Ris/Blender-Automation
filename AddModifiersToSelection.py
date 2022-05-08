import bpy

selected = bpy.context.selected_objects
active = bpy.context.active_object

#mod = obj.modifiers.new("VertexGroupTransfer", 'DATA_TRANSFER')

#for i in selected:
for i in selected:
    #if i == obj:
    #    continue
    mod = i.modifiers.get("VertexGroupTransfer")
    if mod is None:
        mod = i.modifiers.new("VertexGroupTransfer", 'DATA_TRANSFER')
    
        mod.use_vert_data = True
        mod.data_types_verts = {'VGROUP_WEIGHTS'}
        mod.vert_mapping = 'POLYINTERP_NEAREST'

        mod.object = bpy.data.objects["body_retop.007"]
        
    mod = i.modifiers.get("Armature")
    if mod is None:
        mod = i.modifiers.new("Armature", 'ARMATURE')
        #i.object = bpy.data.objects["Armature"]
        
        mod.object = bpy.data.objects["Armature"]

    
    
        
#bpy.context.view_layer.objects.active = active 
#bpy.ops.object.join()