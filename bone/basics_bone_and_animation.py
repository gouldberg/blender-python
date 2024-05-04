
import os
import random
import math

import bpy
import bmesh


# --------------------------------------------------------------------------------------------
# clear scene if required 
# --------------------------------------------------------------------------------------------

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()



# --------------------------------------------------------------------------------------------
# clear meshes and armatures if required 
# --------------------------------------------------------------------------------------------

for a in bpy.data.armatures:
    bpy.data.armatures.remove(a)


for m in bpy.data.meshes:
    bpy.data.meshes.remove(m)



# --------------------------------------------------------------------------------------------
# make objects
# --------------------------------------------------------------------------------------------
  
bpy.ops.object.add(type='ARMATURE')

amt = bpy.data.objects["Armature"]


# ----------
bpy.ops.mesh.primitive_cylinder_add()

obj = bpy.data.objects["Cylinder"]


# ----------
bpy.context.view_layer.objects.active = amt



# --------------------------------------------------------------------------------------------
# make bones
# --------------------------------------------------------------------------------------------

bpy.ops.object.mode_set(mode='EDIT')


# new bone
b = amt.data.edit_bones.new('Bone')
b2 = amt.data.edit_bones.new('Bone2')

b.head = (0,0,-1)
b.tail = (0,0,0)

b2.head = b.tail
b2.tail = (0,0,1)
b2.parent = b


# ----------
bpy.ops.object.mode_set(mode='OBJECT')

bpy.context.view_layer.objects.active = obj
bpy.context.view_layer.objects.active = amt

bpy.ops.object.parent_set(type='ARMATURE_AUTO')


# --------------------------------------------------------------------------------------------
# make animation
# --------------------------------------------------------------------------------------------

bone2 = amt.pose.bones['Bone2']

bone2.rotation_mode = "XYZ"

rotations = (0,0,0),(90,0,0),(-90,0,0),(0,90,0),(0,-90,0),(0,0,90),(0,0,-90),(0,0,0)


# ----------
frame = 0

bpy.context.scene.frame_set(frame)

for r in rotations:
    bone2.rotation_euler.x = math.radians(r[0])
    bone2.rotation_euler.y = math.radians(r[1])
    bone2.rotation_euler.z = math.radians(r[2])
    bone2.keyframe_insert("rotation_euler",frame=frame)
    frame += 35


bpy.context.scene.frame_set(0)

