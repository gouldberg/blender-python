
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
# create torus with random color by segment
# --------------------------------------------------------------------------------------------

class Torus():
    def __init__(self):
        for item in bpy.data.meshes:
            bpy.data.meshes.remove(item)
        for item in bpy.data.materials:
            bpy.data.materials.remove(item)

    def make(self):
        bpy.ops.mesh.primitive_torus_add(
            major_segments=24, minor_segments=8, major_radius=5, minor_radius=2)
        o = bpy.context.active_object
        bpy.ops.object.mode_set(mode = 'EDIT')
        mesh = bmesh.from_edit_mesh(o.data)
        mesh.select_mode = {'FACE'}
        mesh.faces.ensure_lookup_table()
        
        for f in range(len(mesh.faces)):
            face = mesh.faces[f]
            self.set_material(o,f)
            face.material_index = f
            o.data.update()

    def make_material(self,name,color):
        ma = bpy.data.materials.new(name)
        ma.use_nodes = True
        bsdf = ma.node_tree.nodes["Principled BSDF"]
        bsdf.inputs[0].default_value = color
        bsdf.inputs[4].default_value = 0.5
        bsdf.inputs[7].default_value = 0
        bpy.context.object.data.materials.append(ma)
        ma.diffuse_color = color
        return ma

    def set_material(self,o,index):
        r = random.random()
        g = random.random()
        b = random.random()
        ma = self.make_material("Color"+str(index),(r,g,b,1))
        m = o.material_slots[index]
        m.material = ma


# ----------
torus = Torus()

torus.make()

bpy.ops.object.mode_set(mode = 'OBJECT')



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



