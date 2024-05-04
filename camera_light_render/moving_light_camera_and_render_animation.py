

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

START = 0
END   = 100
N     = 3

for x in range(0, N):
    for y in range(0, N):
        for z in range(0, N):
            bpy.ops.mesh.primitive_cube_add( location=(x*3, y*3, z*3) )
            bpy.ops.transform.resize(value=(0.8, 0.1, 2.0))
            bpy.ops.transform.rotate(value= -3.1415/6, orient_axis='X')
            #obj = bpy.context.scene.objects.active #(old blender2.7script)
            obj = bpy.context.view_layer.objects.active
            #mat.diffuse_color = (x/N, y/N, z/N)#(old blender2.7script)
            mat = bpy.data.materials.new('Cube')
            r1=0.15 + 0.8 * random.random()
            g1=0.07 + 0.3 * random.random()
            b1=0.01 + 0.05 * random.random()
            mat.diffuse_color = (r1, g1, b1, 0)
            #mat.use_transparency = True #(この行は2.8で試していない)
            #mat.alpha = 0.6 #(この行は2.8で試していない)
            obj.data.materials.append(mat)



# --------------------------------------------------------------------------------------------
# background
# --------------------------------------------------------------------------------------------

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.15, 0.25, 1)
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.7            


# --------------------------------------------------------------------------------------------
# new camera
# --------------------------------------------------------------------------------------------

bpy.ops.object.add(
    radius=1.0,
    type='CAMERA',
    enter_editmode=False,
    align='WORLD',
    location=(20.0, -6.0, 8.0), rotation=(1.4, 0.0, 1.2))


# ----------
# get active object
camera_obj = bpy.context.object
camera_obj.name = 'Camera_1'

scene = bpy.context.scene
scene.camera = camera_obj


# --------------------------------------------------------------------------------------------
# point light (ligth_2.80)
# --------------------------------------------------------------------------------------------

light_data = bpy.data.lights.new(name="light_2.80", type='POINT')
light_data.energy = 1000


# ----------
light_object = bpy.data.objects.new(name="light_2.80", object_data=light_data)


# link light object
bpy.context.collection.objects.link(light_object)


# make it active 
bpy.context.view_layer.objects.active = light_object


# change location
light_object.location = (5, -4, 10)


# update scene, if needed
dg = bpy.context.evaluated_depsgraph_get() 

dg.update()



# --------------------------------------------------------------------------------------------
# spot light
# --------------------------------------------------------------------------------------------

light_data = bpy.data.lights.new(name="light_spot1", type='SPOT')
light_data.energy = 3000


# ----------
light_object1 = bpy.data.objects.new(name="light_spot1", object_data=light_data)

bpy.context.collection.objects.link(light_object1)

bpy.context.view_layer.objects.active = light_object1

light_object1.location = (5, -5, 10)

# (0, 0, 0) is downside
light_object1.delta_rotation_euler = (1.2, 0, -0.3)

dg = bpy.context.evaluated_depsgraph_get() 

dg.update()



# --------------------------------------------------------------------------------------------
# move light in animation: point light
# --------------------------------------------------------------------------------------------

# make POINT light ACTIVE 
# deselect and select
bpy.context.scene.objects["light_spot1"].select_set(False)
bpy.context.scene.objects["light_2.80"].select_set(True)



# ----------
# get active object
# cdnow  = bpy.context.object
cdnow  = bpy.context.scene.objects["light_2.80"]

frame_num = 0
bpy.context.scene.frame_set(frame_num)

cdnow.keyframe_insert(data_path="location", frame=50)
cdnow.location = (1,-10,1)

cdnow.keyframe_insert(data_path="location", frame=100)
cdnow.location = (1,-10,8)

cdnow.keyframe_insert(data_path="location", frame=150)
cdnow.location = (8,-5,8)

cdnow.keyframe_insert(data_path="location", frame=200)
cdnow.location = (1,-10,1)

cdnow.keyframe_insert(data_path="location", frame=250)



# --------------------------------------------------------------------------------------------
# move light in animation: spot light
# --------------------------------------------------------------------------------------------

# deselect and select
bpy.context.scene.objects["light_2.80"].select_set(False)
bpy.context.scene.objects["light_spot1"].select_set(True)


# ----------
# get active object
cdnow  = bpy.context.object

cdnow.location = (5, -5, 8)

cdnow.keyframe_insert(data_path="location", frame=300)
cdnow.location = (5, -5, 13)

cdnow.keyframe_insert(data_path="location", frame=350)
cdnow.location = (2, -5, 13)

cdnow.keyframe_insert(data_path="location", frame=400)
cdnow.location = (5, -5, 8)

cdnow.keyframe_insert(data_path="location", frame=450)



# --------------------------------------------------------------------------------------------
# move camera
# --------------------------------------------------------------------------------------------

bpy.data.objects['Camera_1'].select_set(True)

cdnow  = bpy.context.scene.objects["Camera_1"]


bpy.ops.anim.keyframe_insert_menu(type='Location')

cdnow.keyframe_insert(data_path="location", frame=500)
cdnow.location = (20.0, -4.0, 9.0)

cdnow.keyframe_insert(data_path="location", frame=550)
cdnow.location =  (22.0, -4.0, 10.0)

cdnow.keyframe_insert(data_path="location", frame=600)
cdnow.location = (20.0, -6.0, 8.0)

cdnow.keyframe_insert(data_path="location", frame=650)

bpy.data.objects['Camera_1'].select_set(False)



# --------------------------------------------------------------------------------------------
# render animation
# --------------------------------------------------------------------------------------------

# set longer frames
scene = bpy.context.scene 
scene.frame_end = 650


render_path = '/home/kswada/blender/scripts/camera_light_render/output/moving_light_camera.avi'

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = "AVI_RAW"

bpy.data.scenes['Scene'].render.filepath = render_path
# bpy.data.scenes['Scene'].render.film_transparent=False

bpy.ops.render.render(use_viewport = True, animation = True)



