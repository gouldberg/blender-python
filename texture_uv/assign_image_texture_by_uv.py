
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
# new object and link to collection
# --------------------------------------------------------------------------------------------

name = 'Triangle'

mesh = bpy.data.meshes.new(name)


object = bpy.data.objects.new(name, mesh)


# link object to collection
bpy.context.collection.objects.link(object)



# --------------------------------------------------------------------------------------------
# generate meshes
# --------------------------------------------------------------------------------------------

verts = [(-10, 0, 10), (10, 0, 10), (10, 0, -10), (-10, 0, -10)]

faces = [(0, 1, 2, 3)]

# generate meshes
mesh.from_pydata(verts, [], faces)


# --------------------------------------------------------------------------------------------
# generate meshes
# --------------------------------------------------------------------------------------------

me = object.data

# generate uv coordinate
me.uv_layers.new(name=name)


# ----------
uvs = [(0,1),(1,1),(1,0),(0,0)]

for i in range(len(uvs)):
    me.uv_layers[0].data[i].uv = uvs[i]

mesh.update()


# --------------------------------------------------------------------------------------------
# active and edit mode
# --------------------------------------------------------------------------------------------

bpy.context.view_layer.objects.active = object

bpy.ops.object.mode_set(mode = 'EDIT')



# --------------------------------------------------------------------------------------------
# convert objet data to bmesh
# --------------------------------------------------------------------------------------------

# convert object data to bmesh
mesh = bmesh.from_edit_mesh(object.data)


# ----------
mesh.select_mode = {'FACE'}

# requires !!
mesh.faces.ensure_lookup_table()

mesh.faces[0].material_index = 0



# --------------------------------------------------------------------------------------------
# link image texture to base color
# --------------------------------------------------------------------------------------------

name2 = 'Color'

ma = bpy.data.materials.new(name2)

ma.use_nodes = True
bsdf = ma.node_tree.nodes["Principled BSDF"]

color = (1, 0, 0, 1)
bsdf.inputs[0].default_value = color


# ----------
# image texture

img = ma.node_tree.nodes.new('ShaderNodeTexImage')

imgpath = '/home/kswada/blender/sample_images/LadyEye.png'

img.image = bpy.data.images.load(imgpath)


# ----------
# link image texture to base color
ma.node_tree.links.new(bsdf.inputs['Base Color'], img.outputs['Color'])



# --------------------------------------------------------------------------------------------
# material to context
# --------------------------------------------------------------------------------------------

bpy.context.object.data.materials.append(ma)

ma.diffuse_color = color



# --------------------------------------------------------------------------------------------
# post process
# --------------------------------------------------------------------------------------------

# back to object mode 
bpy.ops.object.mode_set(mode = 'OBJECT')



##############################################################################################
# --------------------------------------------------------------------------------------------
# get mesh object --> show uv info and material name
# --------------------------------------------------------------------------------------------

print('------------------------------------------------------\n')

objs = [o for o in bpy.data.objects if o.type == 'MESH']
print(f'Num Mesh Object: {len(objs)}')

for o in objs:
    mesh = bpy.data.meshes[o.data.name]

    print(f'Mesh Object: {o}   Name: {o.data.name}')

    print(f'   Num Material Slot: {len(o.material_slots)}')
    for m in o.material_slots:
        if not (m.material is None):
            print(f'      Material Name: {m.material.name}')


    for layer in mesh.uv_layers:
        for idx, dat in enumerate(mesh.uv_layers[layer.name].data):
            s = ",".join([str(uv) for uv in dat.uv])
            print(f'   UV Index: {idx}  UV: {s}')


num_material = len(bpy.data.materials)

print('------------------------------------------------------\n')
print(f'Num Material Num : {str(num_material)}')


for i in range(num_material):
    m = bpy.data.materials[i]
    print(f'   Material: {m}   Name: {m.name}')


# --------------------------------------------------------------------------------------------
# get texture info
# --------------------------------------------------------------------------------------------

for o in bpy.data.objects:
    for m in o.material_slots:
        if m.material.node_tree is not None:
            nodes = m.material.node_tree.nodes
            for n in nodes:
                if n.type == 'TEX_IMAGE':
                    print(n.image.filepath)


