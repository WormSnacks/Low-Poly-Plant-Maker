import bpy
import bmesh
import random
import mathutils
from .common_funcs import (
    floatLerp,
    get_heirs,
    copyObj
)


class StemApplier(bpy.types.Operator):
    """Wren's personalized stem randomizing tool, part of Plant Maker
    pass things here after they have been generated into a collection earlier
    """

    bl_idname = "mesh.stems_bake"
    bl_label = "Combine Stems to single Object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        stemProp = context.object.data.stem_properties
        stemObj = context.view_layer.objects.active
        hairObj = stemProp.hairParticleObj
        if stemObj.type == 'MESH':
            if stemProp.duplicateContainer is not None:
                col = stemObj.users_collection[0]
                topObjs = []
                nTopObjs = []
                for co in stemProp.duplicateContainer.children:
                    if stemObj.name + " Meshes" in co.name:
                        for obj in co.objects:
                            if obj.parent is hairObj:
                                topObjs.append(obj)

                for obj in topObjs:
                    # obj.select_set = True
                    nParent = copyObj(obj)
                    nParent.parent = None
                    nTopObjs.append(nParent)
                    col.objects.link(nParent)
                    # if nParent.type == 'MESH':
                    #     # dgraph = obj.eva
                    #     # nParent.data = obj.to_mesh()
                    #     nParent.data = obj.data

                    cObjs = get_heirs(obj, 5)
                    ncObjs = []
                    ncObjs.append(nParent)
                    # print(nParent.parent.name)
                    for c in cObjs:
                        nc = copyObj(c, nParent)
                        # if c.type == 'MESH':
                        #     nc.data = c.data
                        ncObjs.append(nc)
                    for n in ncObjs:
                        n.select_set(True)
                    context.view_layer.objects.active = ncObjs[0]
                    # print(override.active_object.name)
                    bpy.ops.object.join()
                    bpy.ops.object.select_all(action='DESELECT')
                    # print(None.name)

                bpy.ops.object.select_all(action='DESELECT')
                for n in nTopObjs:
                    n.select_set(True)
                context.view_layer.objects.active = nTopObjs[0]
                bpy.ops.object.join()
            else:
                print("Error! Stem has not been duplicated.")
        else:
            print("Error! Not a mesh")
        return{'FINISHED'}
