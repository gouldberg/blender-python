
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


# clear all meshes and materials
def delete_all():
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    for item in bpy.data.materials:
        bpy.data.materials.remove(item)


# --------------------------------------------------------------------------------------------
# create mutiple spheres with random color
# --------------------------------------------------------------------------------------------

def make_sphere(x,y,z):
    loc = (x,y,z)
    cube = bpy.ops.mesh.primitive_uv_sphere_add(location=loc)
    # 1 sphere 1 material slot
    bpy.ops.object.material_slot_add()
    r = random.random()
    g = random.random()
    b = random.random()
    ma = make_material("Color"+str(x)+str(y),(r,g,b,1))
    # assign material to material slot
    for m in bpy.context.active_object.material_slots:
        m.material = ma


def make_spheres(num_x,num_y):
    for x in range(num_x):
        for y in range(num_y):
            make_sphere(x*2-(num_x-1),y*2-(num_y-1),0)


def make_material(name,color):
    ma = bpy.data.materials.new(name)
    ma.diffuse_color = color
    bpy.context.object.data.materials.append(ma)
    return ma


# ----------
NUM_X = 7
NUM_Y = 7

delete_all()    

make_spheres(NUM_X, NUM_Y)



##############################################################################################
# --------------------------------------------------------------------------------------------
# count materials
# show material name
# --------------------------------------------------------------------------------------------

num_material = len(bpy.data.materials)

print('------------------------------------------------------\n')
print(f'Num Material Num : {str(num_material)}')


for i in range(num_material):
    m = bpy.data.materials[i]
    print(f'   Material: {m}   Material Name: {m.name}')


# --------------------------------------------------------------------------------------------
# material slot
# --------------------------------------------------------------------------------------------

print('------------------------------------------------------\n')

objs = [o for o in bpy.data.objects if o.type == 'MESH']
print(f'Num Mesh Object: {len(objs)}')


for o in objs:
    print(f'Mesh Object: {o}')
    print(f'   Num Material Slot: {len(o.material_slots)}')
    for m in o.material_slots:
        if not (m.material is None):
            print(f'      Material Name: {m.material.name}')



