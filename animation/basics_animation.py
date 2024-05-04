
#  1.  save this scripy as .py file
#  2.  Alt + P to run
#  3.  go to 'Animation' tab and run


import os
import random

import bpy
import bmesh

import numpy as np


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
# simple uv sphere
# simple cube
# --------------------------------------------------------------------------------------------

bpy.ops.mesh.primitive_uv_sphere_add(
    segments=32, ring_count=16, radius=1.0, 
    calc_uvs=True, enter_editmode=False, 
    align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))



bpy.ops.object.modifier_add(type='SUBSURF')
bpy.ops.object.shade_smooth()



# ----------
bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), scale=(1.0, 1.25, 1.75))
bpy.context.object.name = 'cube1'



# --------------------------------------------------------------------------------------------
# assign material
# --------------------------------------------------------------------------------------------

mat = bpy.data.materials.new('mat')

mat.use_nodes = True


# ----------
bsdf = mat.node_tree.nodes["Principled BSDF"]


# 0: base color (R, G, B, A)
color = (0, 1, 0, 1)
bsdf.inputs[0].default_value = color

# 4: metallic
# bsdf.inputs[4].default_value = 1.0

# 7: roughness
# bsdf.inputs[7].default_value = 0.0

# 15: transmission
 #bsdf.inputs[15].default_value = 1.0


# ----------
# diffuse color
# mat.diffuse_color = color


# --------------------------------------------------------------------------------------------
# add material to context
# --------------------------------------------------------------------------------------------

# IMPORTANT:  require to add material to context
bpy.context.object.data.materials.append(mat)



##############################################################################################
# --------------------------------------------------------------------------------------------
# animation setting
# --------------------------------------------------------------------------------------------

# set longer frames
scn = bpy.context.scene 

scn.frame_end = 600


# --------------------------------------------------------------------------------------------
# animation - 1
# --------------------------------------------------------------------------------------------

# set longer frames
scn = bpy.context.scene 

scn.frame_end = 600


scales = (1,3,2), (4,1,6), (3,5,1), (3,10,1), (1,8,1)

start_pos = (10, 10, -3)

ob = bpy.data.objects['Sphere']

frame_num = 0

for s in scales:
    bpy.context.scene.frame_set(frame_num)
    ob.scale = s
    ob.keyframe_insert(data_path = "scale", index = -1)
    frame_num += 20



# --------------------------------------------------------------------------------------------
# animation - 2  (after animation 1)
# --------------------------------------------------------------------------------------------

cube1 = bpy.data.objects['cube1']

start_pos = (100, -10, 3)

frame_num = 0

bpy.context.scene.frame_set(frame_num)


# ----------
cube1.keyframe_insert(data_path="rotation_euler", frame=50)

cube1.rotation_euler.z += np.radians(180)

cube1.keyframe_insert(data_path="rotation_euler", frame=150)


# ----------
cube1.keyframe_insert(data_path="rotation_euler", frame=160)

cube1.rotation_euler.x += np.radians(180)

cube1.keyframe_insert(data_path="rotation_euler", frame=260)


# ----------
cube1.keyframe_insert(data_path="rotation_euler", frame=270)

cube1.rotation_euler.y += np.radians(180)

cube1.keyframe_insert(data_path="rotation_euler", frame=370)


# ----------
cube1.keyframe_insert(data_path="rotation_euler", frame=380)

cube1.rotation_euler.x += np.radians(180)
cube1.rotation_euler.y += np.radians(180)
cube1.rotation_euler.z += np.radians(180)

cube1.keyframe_insert(data_path="rotation_euler", frame=480)



# --------------------------------------------------------------------------------------------
# set camera to scene
# --------------------------------------------------------------------------------------------

camera_location = (40.0, -10, 2.0)
camera_rotation_euler = (1.4, 0.0, 1.2)

bpy.ops.object.camera_add(
    location=camera_location,
    rotation=camera_rotation_euler
    )

# ----------
camera_obj = bpy.context.object
camera_obj.name = 'Camera_1'

scene = bpy.context.scene
scene.camera = camera_obj



# --------------------------------------------------------------------------------------------
# set spot light
# --------------------------------------------------------------------------------------------

light_data = bpy.data.lights.new(name="light_spot1", type='SPOT')

light_data.energy = 300


# ----------
light_object = bpy.data.objects.new(name="light_spot1", object_data=light_data)

bpy.context.collection.objects.link(light_object)

bpy.context.view_layer.objects.active = light_object

light_object.location = (-5, -5, 5)


# default is (0, 0, 0) : downside
light_object.delta_rotation_euler = (0.8, -0.2, -0.3)

dg = bpy.context.evaluated_depsgraph_get() 

dg.update()



# --------------------------------------------------------------------------------------------
# rendered to avi format video
# --------------------------------------------------------------------------------------------

render_path = '/home/kswada/blender/scripts/animation/output/blender_render.avi'

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = "AVI_RAW"

bpy.data.scenes['Scene'].render.filepath = render_path
bpy.data.scenes['Scene'].render.film_transparent=False

bpy.ops.render.render(use_viewport = True, animation = True)


