import os
import bpy
import bmesh

from math import pi, tan
from mathutils import Vector

import getopt
from bpy_extras.object_utils import world_to_camera_view

import json



#################################################################################
# -------------------------------------------------------------------------------
# scene bounding box
# -------------------------------------------------------------------------------

def coords(objName, space = 'GLOBAL'):
    
    # Store reference to the bpy.data.objects datablock
    obj = bpy.data.objects[objName]
    
    # Store reference to bpy.data.objects[].meshes datablock
    if obj.mode == 'EDIT':
        v = bmesh.from_edit_mesh(obj.data).verts
    elif obj.mode == 'OBJECT':
        v = obj.data.vertices
    
    if space == 'GLOBAL':
        # Return T * L as list of tuples
        # return [(obj.matrix_world * v.co).to_tuple() for v in v]
        return [(obj.matrix_world @ v.co).to_tuple() for v in v]
    elif space == 'LOCAL':
        # Return L as list of tuples
        return [v.co.to_tuple() for v in v]


# ----------
# Return the aggregate bounding box of all meshes in a scene
def scene_bounding_box():

    # Get names of all meshes
    mesh_names = [v.name for v in bpy.context.scene.objects if v.type == 'MESH']

    # Save an initial value
    # Save as list for single-entry modification
    co = coords(mesh_names[0])[0]
    bb_max = [co[0], co[1], co[2]]
    bb_min = [co[0], co[1], co[2]]

    # Test and store maxima and mimima
    for i in range(0, len(mesh_names)):
        co = coords(mesh_names[i])
        for j in range(0, len(co)):
            for k in range(0, 3):
                if co[j][k] > bb_max[k]:
                    bb_max[k] = co[j][k]
                if co[j][k] < bb_min[k]:
                    bb_min[k] = co[j][k]

    # Convert to tuples
    bb_max = (bb_max[0], bb_max[1], bb_max[2])
    bb_min = (bb_min[0], bb_min[1], bb_min[2])

    return [bb_min, bb_max]


# ----------
# Point a light or camera at a location specified by 'target'
# ----------
# to_track_quat:  Return a quaternion rotation from the vector and the track and up axis.
#    track (string) – Track axis in [‘X’, ‘Y’, ‘Z’, ‘-X’, ‘-Y’, ‘-Z’].
#    up (string) – Up axis in [‘X’, ‘Y’, ‘Z’].
# ----------
# to_euler:  Return an Euler representation of the rotation matrix (3x3 or 4x4 matrix only)
def point_at(ob, target):
    ob_loc = ob.location
    dir_vec = target - ob.location
    ob.rotation_euler  = dir_vec.to_track_quat('-Z', 'Y').to_euler()
#    ob.rotation_euler  = dir_vec.to_track_quat('-Z', 'X').to_euler()



# -------------------------------------------------------------------------------
# function: rotate --> render and get camera view 2d coordinate
# -------------------------------------------------------------------------------

def rotate_and_render(
    obj,
    output_dir,
    rotation_auler_axis,
    output_file_pattern_string = 'render%d.png',
    rotation_steps = 32,
    rotation_angle = 360.0):

    # ----------
    original_rotation = obj.rotation_euler
    # background is black (default is False)
    # scene.render.film_transparent=True

    coords2d_dict = {}
    for step in range(0, rotation_steps):
        obj.rotation_euler[rotation_auler_axis] = step * (rotation_angle / rotation_steps) * pi / 180
        idx = output_file_pattern_string % step
        scene.render.filepath = os.path.join(output_dir, (idx))
        # ----------
        # rendering
        bpy.ops.render.render(write_still = True)
        # ----------
        # get 2d coordinate
        coords2d_list0 = []
        for vert in obj.data.vertices:
            coords2d = world_to_camera_view(scene, scene.camera, obj.matrix_world @ vert.co)
            # ----------
            # X and Y map to the view plane and Z is the depth on the view axis
            # print("coords2d: {},{}".format(coords2d.x, coords2d.y))
            coords2d_list0.append((coords2d.x, coords2d.y, coords2d.z))
            # ----------
        coords2d_dict[idx] = coords2d_list0
    # ----------
    obj.rotation_euler = original_rotation
    return coords2d_dict



#################################################################################
# -------------------------------------------------------------------------------
# select cube object
# -------------------------------------------------------------------------------

# please note that this script is executed AFTER relevant blend file is loaded
# also in outliner, point 'Cube'


bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


# ----------
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')

cube_obj = bpy.data.objects['Cube']

cube_obj.select_set(True)



# -------------------------------------------------------------
# set camera
# -------------------------------------------------------------

# height and width
# Now height and width should be same value ...
resolution = (int(640*0.75), 640)


bbox = scene_bounding_box()

# Calculate median of bounding box
bbox_med = ( (bbox[0][0] + bbox[1][0])/2,
             (bbox[0][1] + bbox[1][1])/2,
             (bbox[0][2] + bbox[1][2])/2 )
             
# Calculate size of bounding box
bbox_size = ( (bbox[1][0] - bbox[0][0]),
              (bbox[1][1] - bbox[0][1]),
              (bbox[1][2] - bbox[0][2]) )
              

# add camera to scene
bpy.ops.object.camera_add(location=(0, 0, 0), rotation=(0, 0, 0))
camera_obj = bpy.context.object
camera_obj.name  = 'Camera_1'

# Required for us to manipulate FoV as angles
camera_obj.data.lens_unit = 'FOV'


# Set image resolution in pixels
scene = bpy.context.scene
scene.render.resolution_x = resolution[1]
scene.render.resolution_y = resolution[0]


# Compute FoV angles
aspect_ratio = scene.render.resolution_x / scene.render.resolution_y

if aspect_ratio > 1:
    camera_angle_x = camera_obj.data.angle
    camera_angle_y = camera_angle_x / aspect_ratio
else:
    camera_angle_y = camera_obj.data.angle
    camera_angle_x = camera_angle_y * aspect_ratio


# Set the scene's camera to the our new camera
scene.camera = camera_obj

# Determine the distance to move the camera away from the scene
camera_dist_x = (bbox_size[1]/2) * (tan(camera_angle_x / 2) ** -1)
camera_dist_y = (bbox_size[2]/2) * (tan(camera_angle_y / 2) ** -1)
camera_dist = max(camera_dist_x, camera_dist_y)


# Multiply the distance by an arbitrary buffer
camera_buffer = 1.5
camera_dist *= camera_buffer

# Position the camera to point up the x-axis
camera_loc = (bbox[0][1] - camera_dist, bbox_med[1], bbox_med[2])
# Position the camera to point up the y-axis
# camera_loc = (bbox_med[0], bbox[1][1] - camera_dist, bbox_med[2])

# Set new location and point camera at median of scene
camera_obj.location = camera_loc

point_at(camera_obj, Vector(bbox_med))



# -------------------------------------------------------------
# set background
# -------------------------------------------------------------

bpy.data.worlds["World"].node_tree.nodes["Background"].inputs['Color'].default_value = (1,1,1,1)
# bpy.data.worlds["World"].node_tree.nodes["Background"].inputs['Strength'].default_value = 0.5


# -------------------------------------------------------------
# rotation + rendering and get NDC coordinate
# -------------------------------------------------------------

save_dir = '/home/kswada/blender/scripts/box_rotation_and_render/output'


rotate_value = 10
orient_axis = 'Z'


# 0: x  1: y  2: z
rotation_auler_axis = 2
rotation_steps = 35
rotation_angle = 360.0

coords2d_list = rotate_and_render(
    obj=cube_obj,
    output_dir = save_dir,
    rotation_auler_axis = rotation_auler_axis,
    rotation_steps = rotation_steps,
    rotation_angle = rotation_angle)


# print(coords2d_list)


# NOTE:  bpy_extras.object_utils.world_to_camera_view
# Returns the camera space coords for a 3d point. (also known as: normalized device coordinates - NDC).
# Where (0, 0) is the bottom left and (1, 1) is the top right of the camera frame.
# values outside 0-1 are also supported. A negative ‘z’ value means the point is behind the camera.
# Takes shift-x/y, lens angle and sensor size into account as well as perspective/ortho projections.


# ----------
with open(os.path.join(save_dir, 'coords2d_dict.json'), 'w') as f:
    json.dump(coords2d_list, f, indent=2) 



###############################################################
# -------------------------------------------------------------
# set camera and render from camera view
# -------------------------------------------------------------

#save_dir = '/home/kswada/blender/data/uv_sample/rendered_output'
#resolution = (480, 640)

## Get scene's bounding box (meshes only)
#bbox = scene_bounding_box()

## Calculate median of bounding box
#bbox_med = ( (bbox[0][0] + bbox[1][0])/2,
#             (bbox[0][1] + bbox[1][1])/2,
#             (bbox[0][2] + bbox[1][2])/2 )
#             
## Calculate size of bounding box
#bbox_size = ( (bbox[1][0] - bbox[0][0]),
#              (bbox[1][1] - bbox[0][1]),
#              (bbox[1][2] - bbox[0][2]) )
#              

## ----------
## Add camera to scene
#bpy.ops.object.camera_add(location=(0, 0, 0), rotation=(0, 0, 0))
#camera_obj = bpy.context.object
#camera_obj.name  = 'Camera_1'


## Required for us to manipulate FoV as angles
#camera_obj.data.lens_unit = 'FOV'


## Set image resolution in pixels
## Output will be half the pixelage set here
#scn = bpy.context.scene
#scn.render.resolution_x = resolution[0]
#scn.render.resolution_y = resolution[1]


## ----------
## Compute FoV angles
#aspect_ratio = scn.render.resolution_x / scn.render.resolution_y

#if aspect_ratio > 1:
#    camera_angle_x = camera_obj.data.angle
#    camera_angle_y = camera_angle_x / aspect_ratio
#else:
#    camera_angle_y = camera_obj.data.angle
#    camera_angle_x = camera_angle_y * aspect_ratio


## ----------
## Set the scene's camera to the our new camera
#scn.camera = camera_obj


## ----------
## Determine the distance to move the camera away from the scene
#camera_dist_x = (bbox_size[1]/2) * (tan(camera_angle_x / 2) ** -1)
#camera_dist_y = (bbox_size[2]/2) * (tan(camera_angle_y / 2) ** -1)
#camera_dist = max(camera_dist_x, camera_dist_y)


## Multiply the distance by an arbitrary buffer
#camera_buffer = 1.10
#camera_dist *= camera_buffer

## Position the camera to point up the x-axis
#camera_loc = (bbox[0][1] - camera_dist, bbox_med[1], bbox_med[2])

## Set new location and point camera at median of scene
#camera_obj.location = camera_loc


## ----------
#point_at(camera_obj, Vector(bbox_med))


## ----------
#render_path = os.path.join(save_dir, 'blender_render_sample.png')
#bpy.data.scenes['Scene'].render.filepath = render_path

## Render using Blender Render
#bpy.ops.render.render( write_still = True )




