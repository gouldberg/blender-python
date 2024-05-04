
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
# clear all meshes and materials if required
# --------------------------------------------------------------------------------------------

for item in bpy.data.meshes:
    bpy.data.meshes.remove(item)

for item in bpy.data.materials:
    bpy.data.materials.remove(item)



# --------------------------------------------------------------------------------------------
# simple glass ico sphere
# --------------------------------------------------------------------------------------------

material_glass = bpy.data.materials.new('Green')

material_glass.use_nodes = True


# ----------
bpy.ops.mesh.primitive_ico_sphere_add(
    subdivisions=1,
    enter_editmode=False,
    align='WORLD',
    location=(0, 0, 0), scale=(1, 1, 1))


# ----------
p_BSDF = material_glass.node_tree.nodes["Principled BSDF"]



# 0: base color (R, G, B, A)
p_BSDF.inputs[0].default_value = (0, 1, 0, 1)

# 7: roughness
p_BSDF.inputs[7].default_value = 0

# 15: transmission
p_BSDF.inputs[15].default_value = 1


# ----------
bpy.context.object.data.materials.append(material_glass)



# --------------------------------------------------------------------------------------------
# multiple ico shperes
# --------------------------------------------------------------------------------------------

for i in range(0,6):
    material_glass = bpy.data.materials.new('Blue')
    material_glass.use_nodes = True
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=i+1,
        location=(i, 0, 0),
        scale=(0.7, 0.7, 0.7)
        )
    p_BSDF = material_glass.node_tree.nodes["Principled BSDF"]
    p_BSDF.inputs[0].default_value = (0, 0, 1, 0.5)
    p_BSDF.inputs[4].default_value = 1
    p_BSDF.inputs[7].default_value = 0
    bpy.context.object.data.materials.append(material_glass)
    


# --------------------------------------------------------------------------------------------
# random torus
# --------------------------------------------------------------------------------------------

for i in range(0,10):
    num = random.random()

    material_glass = bpy.data.materials.new('Blue')
    material_glass.use_nodes = True
    bpy.ops.mesh.primitive_torus_add(
        rotation=(math.pi * num, math.pi * num, 0),
        major_segments=64,
        minor_segments=3,
        major_radius=10-i,
        minor_radius=0.1,
         )
    p_BSDF = material_glass.node_tree.nodes["Principled BSDF"]
    p_BSDF.inputs[4].default_value = 1
    p_BSDF.inputs[7].default_value = 0
    p_BSDF.inputs[0].default_value = (0, 0, 1 - i/10, 1)
    bpy.context.object.data.materials.append(material_glass)

