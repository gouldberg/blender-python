
import os
import random

import bpy
import bmesh

from mathutils import Color


# --------------------------------------------------------------------------------------------
# clear scene if required 
# --------------------------------------------------------------------------------------------

# bpy.ops.object.mode_set(mode='OBJECT')
# bpy.ops.object.select_all(action='SELECT')
# bpy.ops.object.delete()



# --------------------------------------------------------------------------------------------
# clear all meshes, materials and textures if required
# --------------------------------------------------------------------------------------------

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)


for item in bpy.data.materials:
    bpy.data.materials.remove(item)


for item in bpy.data.textures:
    bpy.data.materials.remove(item)



# --------------------------------------------------------------------------------------------
# create cube
# --------------------------------------------------------------------------------------------

bpy.ops.mesh.primitive_cube_add(size = 1, location = (0, 0, 0))



# --------------------------------------------------------------------------------------------
# create material to hold texture
# --------------------------------------------------------------------------------------------

ma1 = bpy.data.materials.new('number_1_material')

ma1.use_nodes = True
bsdf1 = ma1.node_tree.nodes["Principled BSDF"]


# base color
color = (1, 0, 0, 1)
bsdf1.inputs[0].default_value = color



# --------------------------------------------------------------------------------------------
# link image texture to base color
# --------------------------------------------------------------------------------------------

imgpath1 = '/home/kswada/blender/sample_images/number_1.png'

imgpath2 = '/home/kswada/blender/sample_images/number_2.png'


img1 = ma1.node_tree.nodes.new('ShaderNodeTexImage')

img1.image = bpy.data.images.load(imgpath1)


# image_obj2 = bpy.data.images.load(imgpath2)



# ----------
# link image texture to base color
ma1.node_tree.links.new(bsdf1.inputs['Base Color'], img1.outputs['Color'])


# ----------
ma1.diffuse_color = color

# Tone down color map, turn on and tone up normal mapping
#ma1.diffuse_color_factor = 0.2
#ma1.use_map_normal = True
#ma1.normal_factor = 2.0


# --------------------------------------------------------------------------------------------
# material to context
# --------------------------------------------------------------------------------------------

bpy.context.object.data.materials.append(ma1)



# --------------------------------------------------------------------------------------------
# configuring UV coordinates 
# --------------------------------------------------------------------------------------------

bm = bmesh.from_edit_mesh(bpy.context.edit_object.data)

bm.faces.ensure_lookup_table()


# ----------
# Index of face to texture
face_ind = 0
bpy.ops.mesh.select_all(action='DESELECT')
bm.faces[face_ind].select = True


# ----------
# Unwrap to instantiate uv layer
bpy.ops.uv.unwrap()


# Grab uv layer
uv_layer = bm.loops.layers.uv.active


# --------------------------------------------------------------------------------------------
# mapping
# --------------------------------------------------------------------------------------------

# Begin mapping...
loop_data = bm.faces[face_ind].loops


# bottom right
uv_data = loop_data[0][uv_layer].uv
uv.data.x = 1.0
uv_data.y = 0.0


# top right
uv_data = loop_data[1][uv_layer].uv
uv.data.x = 1.0
uv_data.y = 1.0


# top left
uv_data = loop_data[2][uv_layer].uv
uv.data.x = 0.0
uv_data.y = 1.0


# bottom left
uv_data = loop_data[3][uv_layer].uv
uv.data.x = 0.0
uv_data.y = 0.0



# --------------------------------------------------------------------------------------------
# change background color
# --------------------------------------------------------------------------------------------

# change background color to white to match our example
bpy.data.worlds['World'].horizon_color = Color((1.0, 1.0, 1.0))



# --------------------------------------------------------------------------------------------
# add lights
# --------------------------------------------------------------------------------------------

# Switch to object mode to add lights
bpy.ops.object.mode_set(mode='OBJECT')


# Liberally add lights
dist = 5
for side in [-1, 1]:
    for coord in [0, 1, 2]:
        loc = [0, 0, 0]
        loc[coord] = side * dist
        bpy.ops.object.lamp_add(type='POINT', location=loc)




