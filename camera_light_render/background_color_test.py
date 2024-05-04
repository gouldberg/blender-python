

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
# generate stack of color cubes
# --------------------------------------------------------------------------------------------

for i in range(5):
    for j in range(5):
        for k in range(5):
            bpy.ops.mesh.primitive_cube_add(size=0.5, enter_editmode=False, align='WORLD', location=(i, j, k), scale=(1, 1, 1))
            obj = bpy.context.view_layer.objects.active
            mat = bpy.data.materials.new('Cube')
            # random brown color
            r1=0.1 + 0.15 * i
            g1=0.1 + 0.15 * j
            b1=0.1 + 0.15 * k
            mat.diffuse_color = (r1, g1, b1, 0)
            obj.data.materials.append(mat)


# --------------------------------------------------------------------------------------------
# new camera align with view
# --------------------------------------------------------------------------------------------

bpy.ops.object.camera_add(
    enter_editmode=False,
    align='VIEW', location=(6, -6, 11), rotation=(45/180*3.14, -15/180*3.14, 45/180*3.14))


# ----------
# get active object
camera_obj = bpy.context.object
camera_obj.name = 'Camera_1'

scene = bpy.context.scene
scene.camera = camera_obj


# --------------------------------------------------------------------------------------------
# 3 spot lights
# --------------------------------------------------------------------------------------------

def set_spot_lights(energy_scale=1.0):
    
    for item in bpy.data.lights:
        bpy.data.lights.remove(item)

    # spot light 1
    light_data = bpy.data.lights.new(name="light_spot1", type='SPOT')
    light_data.energy = 3000 * energy_scale
    light_object = bpy.data.objects.new(name="light_spot1", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.context.view_layer.objects.active = light_object
    light_object.location = (5, -5, 8)
    light_object.delta_rotation_euler = (1.3, 0, 0.3)
    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()


    # spot light 2
    light_data = bpy.data.lights.new(name="light_spot2", type='SPOT')
    light_data.energy = 2000 * energy_scale
    light_object = bpy.data.objects.new(name="light_spot2", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.context.view_layer.objects.active = light_object
    light_object.location = (2, -4, 8)
    light_object.delta_rotation_euler = (1.5, 0, 0)
    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()



    # spot light 3
    light_data = bpy.data.lights.new(name="light_spot3", type='SPOT')
    light_data.energy = 2000 * energy_scale
    light_object = bpy.data.objects.new(name="light_spot3", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    bpy.context.view_layer.objects.active = light_object
    light_object.location = (2, -2, 3)
    light_object.delta_rotation_euler = (1.6, 0, 0)
    dg = bpy.context.evaluated_depsgraph_get() 
    dg.update()



# --------------------------------------------------------------------------------------------
# render image with changing backgound and spot ligths energy scale
# --------------------------------------------------------------------------------------------

def hex_to_rgb( hex_value ):
    b = (hex_value & 0xFF) / 255.0
    g = ((hex_value >> 8) & 0xFF) / 255.0
    r = ((hex_value >> 16) & 0xFF) / 255.0
    return r, g, b

color_value_list = [0x7FFFD4, 0xFFEFD5, 0xb0e0e6, 0xBDB76B]
color_name = ['aquamarine', 'powerwhip', 'powerblue', 'darkkhaki']

# aquamarine #7fffd4,   papayawhip #ffefd5,    powderblue #b0e0e6,    darkkhaki #bdb76b
# aquamarine 0x7FFFD4,  papayawhip 0xFFEFD5,   powderblue 0xb0e0e6,   darkkhaki 0xBDB76B



# ----------
energy_scale_list = [0.1, 0.5, 0.9]

for idx in range(len(color_value_list)):
    for i in range(len(energy_scale_list)):

        #bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (R, G, B, 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (*hex_to_rgb(color_value_list[idx]), 1)
        bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.5

        energy_scale = energy_scale_list[i]
        set_spot_lights(energy_scale=energy_scale)

        render_path = f'/home/kswada/blender/scripts/camera_light_render/output/background_color_test_{color_name[idx]}_energy{energy_scale}.png'
        bpy.data.scenes['Scene'].render.filepath = render_path

        bpy.context.scene.render.resolution_x = 640
        bpy.context.scene.render.resolution_y = 480
        bpy.context.scene.render.resolution_percentage = 100

        bpy.ops.render.render(use_viewport = True, write_still = True)



