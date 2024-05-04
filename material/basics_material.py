
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
# create cube and select object
# --------------------------------------------------------------------------------------------

# bpy.ops.mesh.primitive_cube_add(raius=1, location=(0, 0, 0))
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')


# select cube
cube_obj = bpy.data.objects['Cube']

cube_obj.select_set(True)



# --------------------------------------------------------------------------------------------
# create material
# --------------------------------------------------------------------------------------------

ma = bpy.data.materials.new('texture01')

print(f'material new: {ma}')



# --------------------------------------------------------------------------------------------
# material control
# --------------------------------------------------------------------------------------------


ma.use_nodes = True

bsdf = ma.node_tree.nodes["Principled BSDF"]



# --------------------------------------------------------------------------------------------
# assign rondom color to material
# --------------------------------------------------------------------------------------------

r = random.random()
g = random.random()
b = random.random()

color = (r,g,b,1)
print(f'color: {color}' )


# ----------
bsdf.inputs[0].default_value = color

# metallic
bsdf.inputs[4].default_value = 1

# roughness
bsdf.inputs[7].default_value = 0

# diffuse color
ma.diffuse_color = color



# --------------------------------------------------------------------------------------------
# add material to context
# --------------------------------------------------------------------------------------------

# IMPORTANT:  require to add material to context
bpy.context.object.data.materials.append(ma)


##############################################################################################
# --------------------------------------------------------------------------------------------
# count materials
# show material name
# --------------------------------------------------------------------------------------------

num_material = len(bpy.data.materials)

print('------------------------------------------------------\n')
print(f'Num Material: {str(num_material)}')


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



