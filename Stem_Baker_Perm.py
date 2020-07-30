import bpy
import bmesh
import random
import mathutils
from .common_funcs import (
    floatLerp,
    get_heirs,
    copyObj
)


class StemApplierPerm(bpy.types.Operator):
    """Wren's personalized stem randomizing tool, part of Plant Maker
    pass things here after they have been generated into a collection earlier
    """

    bl_idname = "mesh.stems_bake_perm"
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
                                # print(obj.name)
                                topObjs.append(obj)
                for obj in topObjs:
                    cObjs = get_heirs(obj, 5)
                    cObjs.insert(0, obj)
                    bpy.ops.object.select_all(action='DESELECT')
                    context.view_layer.objects.active = obj
                    for n in cObjs:
                        n.select_set(True)
                    bpy.ops.object.apply_all_modifiers()
                    bpy.ops.object.join()

                bpy.ops.object.select_all(action='DESELECT')

                for n in topObjs:
                    n.select_set(True)
                print(topObjs[0].name)
                context.view_layer.objects.active = topObjs[0]
                bpy.ops.object.join()
            else:
                print("Error! Stem has not been duplicated.")
        else:
            print("Error! Not a mesh")
        return{'FINISHED'}
