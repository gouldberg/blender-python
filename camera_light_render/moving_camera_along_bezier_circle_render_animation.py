

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
# Add a plane for ground
# --------------------------------------------------------------------------------------------

bpy.ops.mesh.primitive_plane_add(size=200.0, align='WORLD', location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0) )

matp = bpy.data.materials.new('Plane')

matp.diffuse_color = (0.4, 0.2, 0.01, 0) 

obj.data.materials.append(matp)



# --------------------------------------------------------------------------------------------
# background
# --------------------------------------------------------------------------------------------

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[0].default_value = (0.01, 0.15, 0.25, 1)
bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.7            



# --------------------------------------------------------------------------------------------
# new camera (aligned with view)
# --------------------------------------------------------------------------------------------

# camera aligned with view
bpy.ops.object.camera_add(
    enter_editmode=False,
    align='VIEW', 
    location=(0,0,0), rotation=(0, 0, 0))


# ----------
# get active object
camera_obj = bpy.context.object
camera_obj.name = 'Camera_1'

scene = bpy.context.scene
scene.camera = camera_obj



# --------------------------------------------------------------------------------------------
# sun light
# --------------------------------------------------------------------------------------------

#light_data = bpy.data.lights.new(name="light_spot1", type='SPOT')
light_data = bpy.data.lights.new(name="light_spot1", type='SUN')

light_data.energy = 5


light_object1 = bpy.data.objects.new(name="light_spot1", object_data=light_data)

bpy.context.collection.objects.link(light_object1)

bpy.context.view_layer.objects.active = light_object1

light_object1.location = (-3, -10, 50)

light_object1.delta_rotation_euler = (1.3, 0, -0.3)

dg = bpy.context.evaluated_depsgraph_get() 

dg.update()



# --------------------------------------------------------------------------------------------
# camera movement
# --------------------------------------------------------------------------------------------

# Bezier cicle movement
bpy.ops.curve.primitive_bezier_circle_add(enter_editmode=False, align='WORLD', location=(20, 20, 30))

bpy.context.object.scale[0] = 50

bpy.context.object.scale[1] = 50

bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0,0,0))


# ----------
bpy.data.objects['Empty'].select_set(True)
bpy.data.objects['Camera_1'].select_set(True)

bpy.context.view_layer.objects.active = bpy.data.objects['Empty']
bpy.ops.object.parent_set(type='OBJECT')


# ----------
# select empty
bpy.data.objects['Camera_1'].select_set(False)
bpy.data.objects['Empty'].select_set(True)

# set follow path
bpy.ops.object.constraint_add(type='FOLLOW_PATH')
bpy.context.object.constraints["Follow Path"].target = bpy.data.objects["BezierCircle"]
bpy.context.object.constraints["Follow Path"].use_curve_follow = True
bpy.context.object.constraints["Follow Path"].use_fixed_location = True


# ----------
# select camera
bpy.data.objects['Empty'].select_set(False)
bpy.data.objects['Camera_1'].select_set(True)

# set track
bpy.ops.object.constraint_add(type='TRACK_TO')
bpy.context.object.constraints["Track To"].target = bpy.data.objects["Cube.016"]
bpy.context.object.constraints["Track To"].up_axis = 'UP_Y'
bpy.context.object.constraints["Track To"].track_axis = 'TRACK_NEGATIVE_Z'


# ----------
# Insert keyframe to object's Offset Factor
bpy.data.objects['Camera_1'].select_set(False)

bpy.data.objects['Empty'].select_set(True)

bpy.context.scene.frame_current = 1

bpy.context.object.constraints["Follow Path"].offset_factor = 0

ob = bpy.context.object


# ----------
# ob.constraints['Follow Path']
# bpy.data.objects['Empty'].constraints["Follow Path"]
# [bpy.data.objects['Empty'].constraints["Follow Path"]]
con = ob.constraints.get("Follow Path")
con.offset_factor = 0.0

con.keyframe_insert("offset_factor", frame=1)
con.offset_factor = 0.25

con.keyframe_insert("offset_factor", frame=8*10)
con.offset_factor = 0.50

con.keyframe_insert("offset_factor", frame=16*10)
con.offset_factor = 0.75

con.keyframe_insert("offset_factor", frame=23*10)
con.offset_factor = 0.99

con.keyframe_insert("offset_factor", frame=30*10)


# --------------------------------------------------------------------------------------------
# render animation
# --------------------------------------------------------------------------------------------

# set longer frames
scene = bpy.context.scene 
scene.frame_end = 350


render_path = '/home/kswada/blender/scripts/camera_light_render/output/moving_camera_bezier_circle.avi'

bpy.context.scene.render.resolution_x = 640
bpy.context.scene.render.resolution_y = 480
bpy.context.scene.render.resolution_percentage = 100
bpy.context.scene.render.image_settings.file_format = "AVI_RAW"

bpy.data.scenes['Scene'].render.filepath = render_path
# bpy.data.scenes['Scene'].render.film_transparent=False

bpy.ops.render.render(use_viewport = True, animation = True)



