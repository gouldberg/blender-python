

import os
import random

import bpy
import bmesh


# --------------------------------------------------------------------------------------------
# clear scene if required 
# --------------------------------------------------------------------------------------------

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()



# --------------------------------------------------------------------------------------------
# clear all meshes and materials if required
# --------------------------------------------------------------------------------------------

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)

for item in bpy.data.materials:
    bpy.data.materials.remove(item)



# --------------------------------------------------------------------------------------------
# add text
# --------------------------------------------------------------------------------------------

# add text and edit mode = True
bpy.ops.object.text_add(enter_editmode = True, location = (0,0,0))


# delete initial text
bpy.ops.font.delete(type = 'PREVIOUS_WORD')


# insert text
bpy.ops.font.text_insert(text = 'Blender')


# end edit mode
bpy.ops.object.editmode_toggle()



# --------------------------------------------------------------------------------------------
# add text with assigning material  (same as object)
# --------------------------------------------------------------------------------------------

bpy.ops.object.text_add(enter_editmode = True, location = (1, 1, 3))

bpy.ops.font.delete(type = 'PREVIOUS_WORD')

bpy.ops.font.text_insert(text = 'Blender')

bpy.ops.object.editmode_toggle()


# ----------
material_glass = bpy.data.materials.new('Blue')

material_glass.use_nodes = True

bsdf = material_glass.node_tree.nodes["Principled BSDF"]


# base color (R, G, B, A)
color = (0, 0, 1, 1)
bsdf.inputs[0].default_value = color

# 4: metallic
bsdf.inputs[4].default_value = 1

# 7: roughness
bsdf.inputs[7].default_value = 0

bpy.context.object.data.materials.append(material_glass)


