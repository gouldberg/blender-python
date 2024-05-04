

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
# simple cube
# --------------------------------------------------------------------------------------------

bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 0), scale=(1, 1.25, 1.75))



# --------------------------------------------------------------------------------------------
# assign material
# --------------------------------------------------------------------------------------------

mat = bpy.data.materials.new('mat')

mat.use_nodes = True


# ----------
bpy.ops.mesh.primitive_cube_add(
    location=(0, 0, 0), scale=(1, 1.25, 1.75))


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
# set camera to scene
# --------------------------------------------------------------------------------------------

camera_location = (12.0, -3.0, 2.0)
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
# render
# --------------------------------------------------------------------------------------------

render_path = '/home/kswada/blender/scripts/light/output/blender_render.png'
bpy.data.scenes['Scene'].render.filepath = render_path

bpy.data.scenes['Scene'].render.film_transparent=False

bpy.ops.render.render(use_viewport = True, write_still = True)




