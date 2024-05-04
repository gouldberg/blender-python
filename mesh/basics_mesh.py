
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
# create pyramid from vertices and faces
# --------------------------------------------------------------------------------------------

# only 1 polygon
#verts = [(0,0,10), (10,0,-10), (-10,0,-10)]
#faces = [(0,1,2)]
#name = "Polygon"


# pyramid with 5 polygons
verts = [(0,0,10), (10,10,-10), (-10,10,-10), (-10,-10,-10), (10,-10,-10)]
faces = [(0,1,2), (0,2,3), (0,3,4), (0,4,1), (4,3,2,1)]
name = "Polygons"


mesh = bpy.data.meshes.new(name)

object = bpy.data.objects.new(name, mesh)

bpy.context.collection.objects.link(object)


# ----------
# generate mesh by vertices, edges, and faces
# edge is automatically calculated (do not specify edge simultaneously with face !!)

mesh.from_pydata(verts, [], faces)

# default is calc_edges=True
mesh.update(calc_edges=True)



##############################################################################################
# --------------------------------------------------------------------------------------------
# count mesh objects and show object name
# --------------------------------------------------------------------------------------------

objs = [o for o in bpy.data.objects if o.type == 'MESH']

num_objs = len(objs)


print('------------------------------------------------------\n')
print(f'Num Mesh Objects : {num_objs}')


for i in range(num_objs):
    o = objs[i]
    print(f'   Mesh Object: {o}   Mesh Name: {o.name}')



# --------------------------------------------------------------------------------------------
# count vertices, edges, faces
# show vertices coordinate
# --------------------------------------------------------------------------------------------

print('------------------------------------------------------\n')

for i in range(len(objs)):
    mesh = bpy.data.meshes[objs[i].data.name]
    print(f'Mesh Object: {objs[i].data.name}')
    print(f'   Num Vertex: {len(mesh.vertices)}')
    for v in mesh.vertices:
        print(f'      {v.co.x} - {v.co.y} - {v.co.z}')
    print(f'   Num Edges: {len(mesh.edges)}')
    # NOTE:  no mesh.faces

    # ----------
    # from BMesh
    bpy.context.view_layer.objects.active = objs[i]
    bpy.ops.object.mode_set(mode = 'EDIT')
    me = objs[i].data
    # convert mesh data to BMesh data
    bm = bmesh.from_edit_mesh(me)
    print(f'   Num Vertex from BMesh: {len(bm.verts)}')
    print(f'   Num Edges from BMesh: {len(bm.edges)}')
    print(f'   Num Faces from BMesh: {len(bm.faces)}')
    


##############################################################################################
# --------------------------------------------------------------------------------------------
# copy object and move
# --------------------------------------------------------------------------------------------

# the new object is created with the old object's data, which makes it "linked"
# new_obj = bpy.data.objects.new('newobj', bpy.data.objects['Polygons'].data)
#new_obj.location = (20,20,0)
#bpy.context.collection.objects.link(new_obj)


# ----------
# copy object but not linked
bpy.ops.object.mode_set(mode = 'OBJECT')

bpy.data.objects["Polygons"].select_set(True)

bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')

bpy.data.objects["Polygons.001"].select_set(True)


bpy.ops.object.mode_set(mode = 'EDIT')

bpy.ops.transform.translate(value=(10, 10, 0), constraint_axis=(True, True, True))


# --------------------------------------------------------------------------------------------
# change selected vertex coordinate
# --------------------------------------------------------------------------------------------

# only mesh object of selected new object
obj = bpy.data.objects['Polygons.001']

bm = bmesh.from_edit_mesh(obj.data)


# requires ensure_lookup_table()
bm.verts.ensure_lookup_table()
vert_idx = 0
bm.verts[vert_idx].co.x = 20


# required to update
bpy.ops.object.mode_set(mode = 'OBJECT')



# --------------------------------------------------------------------------------------------
# change selected vertex coordinate
# --------------------------------------------------------------------------------------------

#bpy.ops.object.mode_set(mode = 'EDIT')

#object = bpy.context.active_object

#bm = bmesh.from_edit_mesh(object.data)

#for v in bm.verts:
#    if v.select:
#        v.co.x = -2


## required to update
#bpy.ops.object.mode_set(mode = 'OBJECT')



