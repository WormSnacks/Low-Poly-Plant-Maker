import bpy
import bmesh
import random
import mathutils


class StemApplier(bpy.types.Operator):
    """Wren's personalized stem randomizing tool, part of Plant Maker
    pass things here after they have been generated into a collection earlier
    """

    bl_idname = "mesh.stem_apply"
    bl_label = "Apply Plant Maker Stem to Particle System Hair"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        stemProp = context.object.data.stem_properties
        stemObj = context.object
        hairObj = stemProp.hairParticleObj
        stemProp.baseStemObj = None
        bpy.ops.mesh.stem_randomizer()
        # We're going to want to keep this organized
        # collectionMade = False
        fullCollection = None
        meshCollection = None
        curveCollection = None

        for child in stemObj.users_collection[0].children:
            if stemObj.name+" Duplicates" in child.name:
                fullCollection = child
                for chil in fullCollection.children:
                    if stemObj.name+" Meshes" in chil.name:
                        meshCollection = chil
                    if stemObj.name+" Curves" in chil.name:
                        curveCollection = chil

        if fullCollection is None:
            fullCollection = bpy.data.collections.new(
                stemObj.name + " Duplicates")
            # parentColl(fullCollection, stemObj.users_collection[0], context)
            stemObj.users_collection[0].children.link(fullCollection)

            meshCollection = bpy.data.collections.new(stemObj.name+" Meshes")
            # bpy.data.collections[fullCollection].children.link(meshCollection)
            fullCollection.children.link(meshCollection)
            curveCollection = bpy.data.collections.new(stemObj.name+" Curves")
            fullCollection.children.link(curveCollection)
        if meshCollection is None:
            meshCollection = bpy.data.collections.new(stemObj.name+" Meshes")
            fullCollection.children.link(meshCollection)
        if curveCollection is None:
            curveCollection = bpy.data.collections.new(stemObj.name+" Curves")
            fullCollection.children.link(curveCollection)

        # Collections now set up, now delete all objects
        for obj in meshCollection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        for obj in curveCollection.objects:
            bpy.data.objects.remove(obj, do_unlink=True)
        for obj in fullCollection.objects:
            if obj is not stemProp.hairParticleObj:
                bpy.data.objects.remove(obj, do_unlink=True)

        if stemProp.hairParticleObj.users_collection[0] is not fullCollection:
            fullCollection.objects.link(stemProp.hairParticleObj)
            stemProp.hairParticleObj.users_collection[0].objects.unlink(
                stemProp.hairParticleObj)

        for mod in stemProp.hairParticleObj.modifiers:

            if mod.type == 'PARTICLE_SYSTEM':
                # set active collection to mesh collection so that the
                # converted particle will automatically go there
                layer_collection = context.view_layer.layer_collection
                layerColl = recurLayerCollection(
                    layer_collection, curveCollection.name)
                context.view_layer.active_layer_collection = layerColl

                override = context.copy()
                override['object'] = stemProp.hairParticleObj
                # print(context.object.name)
                bpy.ops.object.modifier_convert(override,
                                                modifier=mod.name)

        for obj in curveCollection.objects:
            if "Mesh" in obj.name:

                override = context.copy()
                override['active_object'] = obj
                bpy.ops.mesh.separate(override, type='LOOSE')

        curveObjs = []
        for obj in curveCollection.objects:
            curveObjs.append(obj)
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            bm.verts.ensure_lookup_table()
            origin = mathutils.Vector(
                (bm.verts[0].co[0],
                 bm.verts[0].co[1],
                 bm.verts[0].co[2]))
            # print(bm.verts[0].co)
            bmesh.ops.translate(bm,
                                verts=bm.verts,
                                vec=-origin,
                                )
            bm.to_mesh(obj.data)
            obj.data.update()
            # print(origin)
            obj.location = origin

        override = context.copy()
        override['selected_objects'] = curveObjs
        bpy.ops.object.convert(target='CURVE', keep_original=False)
        for obj in curveObjs:
            for spline in obj.data.splines:
                spline.type = 'BEZIER'
                for point in spline.bezier_points:
                    point.handle_left_type = 'AUTO'
                    point.handle_right_type = 'AUTO'

        # CURVES NOW PREPARED!!
        # now get to adding curve modifier to stemObj and duplicating it!
        # Find radius of curve collection for falloff

        CurveCheck(stemObj)
        stemObjs = []

        # stemObjs.append(stemObj)
        for obj in stemObj.children:
            CurveCheck(obj)
            stemObjs.append(obj)

        for x in range(len(curveCollection.objects)):
            newStem = stemObj.copy()
            newStem.data = stemObj.data.copy()
            newStem.animation_data_clear()
            meshCollection.objects.link(newStem)
            newStem.data.stem_properties.baseStemObj = stemObj

            bpy.ops.object.select_all(action='DESELECT')
            context.view_layer.objects.active = newStem
            bpy.ops.mesh.stem_randomizer()
            target_curve = curveCollection.objects[x]
            newStem.location = target_curve.location
            ApplyCurveMod(newStem, target_curve)
            for child in newStem.children:
                ApplyCurveMod(child, target_curve)
        context.view_layer.objects.active = stemObj
        return{'FINISHED'}


def ApplyCurveMod(obj, curve):
    for mod in obj.modifiers:
            # print(mod.name)
        if "Stem Curve" in mod.name and mod.type == 'CURVE':
            mod.object = curve
            mod.deform_axis = 'POS_Z'

def CurveCheck(obj):
    hasCurve = False
    for mod in obj.modifiers:
        if mod.type == 'CURVE':
            hasCurve = True
    if hasCurve is False:
        obj.modifiers.new(name="Stem Curve", type='CURVE')


# Recursivly transverse layer_collection for a particular name
def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found
