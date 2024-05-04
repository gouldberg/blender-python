import os
import bpy
import bmesh

from mathutils import Vector

from bpy_extras.object_utils import world_to_camera_view


# reference:
# https://github.com/dfelinto/blender/blob/master/release/scripts/modules/bpy_extras/object_utils.py



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
    location=(1, 2, -0.5), scale=(1, 1.25, 1.75))




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
cam = bpy.context.object
cam.name = 'Camera_1'


scene = bpy.context.scene
scene.camera = cam


print('--------------------------------------------------')
print(f'Camera View Frame: {cam.data.view_frame(scene=scene)}')

frame = [v for v in cam.data.view_frame(scene=scene)[:3]]
print(f'Frame: {frame}')



# --------------------------------------------------------------------------------------------
# object and camera world matrix 
# --------------------------------------------------------------------------------------------

obj = bpy.data.objects['Cube']


# 4 * 4 matrix:  following column, orient of (X-axis, Y-axis, Z-axis) and location
# get by column (require to transpose to get by column) also convert to 3x3

print('--------------------------------------------------')
print(f'Object Matrix World: {obj.matrix_world}')
print(f'Object Matrix World normalized: {obj.matrix_world.normalized()}')
print(f'Object Matrix World normalized inverted: {obj.matrix_world.normalized().inverted()}')
print(obj.matrix_world.transposed().to_3x3()[0])
print(obj.matrix_world.transposed().to_3x3()[1])
print(obj.matrix_world.transposed().to_3x3()[2])

obj.matrix_world.normalized().inverted()

print('--------------------------------------------------')
print(f'Camera Matrix World: {cam.matrix_world}')
print(f'Camera Matrix World normalized: {cam.matrix_world.normalized()}')
print(f'Camera Matrix World normalized inverted: {cam.matrix_world.normalized().inverted()}')
print(cam.matrix_world.transposed().to_3x3()[0])
print(cam.matrix_world.transposed().to_3x3()[1])
print(cam.matrix_world.transposed().to_3x3()[2])



# --------------------------------------------------------------------------------------------
# get vertices coordinates of object by matrix_word @ vert.co
# convert to coord into camera view  (NDC:  normalized device coordinate)
# --------------------------------------------------------------------------------------------

verts = [vert for vert in obj.data.vertices]

print('--------------------------------------------------')

for i in range(len(verts)):

    # ----------
    # 1. coordinate of the vertex
    coord_vert = obj.matrix_world @ verts[i].co

    # ----------
    # 2-1. coordinate of the vertex in camera view
    
    # this is local coord = verts[i].co
    co_local = obj.matrix_world.normalized().inverted() @ coord_vert
#    z = -co_local.z

#    camera_tmp = scene.camera.data
#    frame = [v for v in camera_tmp.view_frame(scene=scene)[:3]]

#    if cam.type != 'ORTHO':
#        if z == 0.0:
#            coord_camview = Vector((0.5, 0.5, 0.0))
#        else:
#            frame2 = [-(v / (v.z / z)) for v in frame]
#            min_x, max_x = frame[2].x, frame[1].x
#            min_y, max_y = frame[1].y, frame[0].y
#            x = (co_local.x - min_x) / (max_x - min_x)
#            y = (co_local.y - min_y) / (max_y - min_y)
#            coord_camview = Vector((x, y, z))

    # ----------
    # 2-2. coordinate of the vertex in camera view (NDC)
    # Where (0, 0) is the bottom left and (1, 1) is the top right of the camera frame.
    # values outside 0-1 are also supported. A negative ‘z’ value means the point is behind the camera.

    coord_camview2 = world_to_camera_view(scene, scene.camera, coord_vert)

    print(f'vers {i}')
    print(f'     local coord    : {verts[i].co}')
    print(f'     world coord    : {coord_vert}')
    print(f'     co_local coord : {co_local}')
#    print(f'     camview coord  : {coord_camview}')
    print(f'     camview coord2 : {coord_camview2}')




