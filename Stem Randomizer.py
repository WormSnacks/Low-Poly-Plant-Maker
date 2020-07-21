import bpy
import bmesh
import random
import mathutils


class StemRandomizer(bpy.types.Operator):
    """Wren's personalized stem randomizing tool, part of Plant Maker
    pass things here after they have been generated into a collection earlier
    """

    bl_idname = "mesh.stem_randomizer"
    bl_label = "Randomize Plant Maker Stem"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return (context.object.data.stem_properties.isStemObject)

    def execute(self, context):
        if context.object.data.type is not 'OBJECT':
            print("Invalid Stem!")
            return{'FINISHED'}

        stemProp = context.object.data.stem_properties
        stemObj = context.object
        # resize stem, set to one first in case this has been done before
        random.seed()
        stemSize = random.uniform(stemProp.stemScaleHeightMin,
                                  stemProp.stemScaleHeightMax)
        # stemObject = bpy.data.objects[self.stemName]

        # stemMesh = bmesh.new()
        # stemMesh = bmesh.from_mesh(stemObject)

        # Subdivide previous resolutions, keeping top and bottom rings
        # if context.object.mode is not 'EDIT':
        #     bpy.ops.object.mode_set(mode='EDIT')
# 
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.dissolve_limited()
        # bpy.ops.mesh.select_face_by_sides(number=6)

        bm = bmesh.new()
        bm.from_mesh(context.object.data)
        bm.faces.ensure_lookup_table()
        bmesh.ops.dissolve_limit(bm, angle_limit=0.0872663)
        topFace = bm.faces[0]
        bottomFace = bm.faces[0]
        for face in bm.faces:
            # print(face.calc_center_median())
            if face.calc_center_median()[2] > topFace.calc_center_median()[2]:
                topFace = face
            elif face.calc_center_median()[2] < bottomFace.calc_center_median()[2]:
                bottomFace = face

        currentRadius = (topFace.calc_center_median() -
                         topFace.verts[0].co).length
        newRadius = stemProp.stemScaleTop * 0.01
        sr = newRadius/currentRadius
        scaleVec = [sr, sr, sr]
        translateVec = [0, 0, (topFace.calc_center_median()[
                               2]-1)*-1 + (stemSize - 1)]
        bmesh.ops.translate(bm, verts=topFace.verts, vec=translateVec)
        bmesh.ops.scale(bm, verts=topFace.verts, vec=scaleVec)

        currentRadius = (bottomFace.calc_center_median() -
                         bottomFace.verts[0].co).length
        newRadius = stemProp.stemScaleBottom * 0.01
        sr = newRadius/currentRadius
        scaleVec = [sr, sr, sr]
        translateVec = [0, 0, (-bottomFace.calc_center_median()[2])]
        bmesh.ops.translate(bm, verts=bottomFace.verts, vec=translateVec)
        bmesh.ops.scale(bm, verts=bottomFace.verts, vec=scaleVec)

        bm.to_mesh(context.object.data)
        bm.free()
        # bm.faces.ensure_lookup_table()

# 
        # win = context.window
        # scr = win.screen
        # areas3d = [area for area in scr.areas if area.type == 'VIEW_3D']
        # region = [
        #     region for region in areas3d[0].regions if region.type == 'WINDOW']
# 
        # override = {'window': win,
        #             'screen': scr,
        #             'area': areas3d[0],
        #             'region': region[0],
        #             'scene': context.scene,
        #             }
        # 

        # bpy.ops.mesh.loopcut(override, MESH_OT_loopcut={"number_cuts":stemProp.stemResolution,
        if context.object.mode is not 'EDIT':
            bpy.ops.object.mode_set_with_submode(mode='EDIT', mesh_select_mode={'FACE'})

        bpy.ops.mesh.select_face_by_sides()
        bpy.ops.mesh.loopcut(override,
                             number_cuts=stemProp.stemResolution,
                             smoothness=0,
                             falloff='INVERSE_SQUARE',
                             object_index=0,
                             edge_index=12,
                             mesh_select_mode_init=(False, False, True))

        bpy.ops.object.mode_set(override, mode='OBJECT')

        # Now clean up Leaves
        if stemProp.leafMeshOne is not None:
            prepareLeaves(
                context, stemProp.leafMeshOne, stemProp.leafOneNum, stemProp.
                leafPosRangeMin, stemProp.leafPosRangeMax, stemSize, stemProp)

        if stemProp.leafMeshTwo is not None:
            prepareLeaves(
                context, stemProp.leafMeshTwo, stemProp.leafTwoNum, stemProp.
                leafPosRangeMin, stemProp.leafPosRangeMax, stemSize, stemProp)
        if stemProp.leafMeshThree is not None:
            prepareLeaves(
                context, stemProp.leafMeshThree, stemProp.leafThreeNum,
                stemProp.leafPosRangeMin, stemProp.leafPosRangeMax, stemSize,
                stemProp)

        # now the same with flowers!
        if stemProp.flowerHeadMeshOne is not None:
            prepareFlowers(context, stemProp.flowerHeadMeshOne,
                           stemProp.flowerOnePos, stemSize, stemProp)
        if stemProp.flowerHeadMeshTwo is not None:
            prepareFlowers(context, stemProp.flowerHeadMeshTwo,
                           stemProp.flowerTwoPos, stemSize, stemProp)

        return{'FINISHED'}


# def register():
    # print("Hello World")


# def unregister():
    # print("Goodbye World")


def floatLerp(a, b, c):
    return (c*a)+((1-c) * b)


def prepareLeaves(context, leafObj, num, min, max, stemSize, stemProp):
    # stemProp = context.object.data.stem_properties

    extantLeaves = []
    extantLeaves.append(context.object)  # placeholder
    leafname = ''
    if len(leafObj.name.split('.')) > 1:
        leafnamelist = leafObj.name.split('.')
        leafnamelist.pop()
        leafname = ''.join([str(elem) for elem in leafnamelist])
    else:
        leafname = leafObj.name
    for child in context.object.children:
        
        if leafname in child.name and child is not leafObj:
            extantLeaves.append(child)

    # below implies that this is a root stem, not a copy
    # this way when we duplicate to apply to curves
    # we can still keep references to base stem leaves
    if stemProp.baseStemObj is not None:
        if leafObj.parent is not context.object:
            leafObj.parent = context.object
    else:
        newLeaf = leafObj.copy()
        newLeaf.data = leafObj.data.copy()
        newLeaf.animation_data_clear()
        context.object.users_collection[0].objects.link(newLeaf)
        newLeaf.parent = context.object

    extantLeaves[0] = leafObj
    if len(extantLeaves) > num:
        diff = len(extantLeaves) - num
        for x in range(diff):
            extra = extantLeaves.pop()
            bpy.data.objects.remove(extra, do_unlink=True)

    elif len(extantLeaves) < num:
        # bpy.ops.object.select_all(action='DESELECT')
        diff = num - len(extantLeaves)
        # extantLeaves[0].select_set(True)
        for x in range(diff):
            newLeaf = leafObj.copy()
            newLeaf.data = leafObj.data.copy()
            newLeaf.animation_data_clear()
            context.object.users_collection[0].objects.link(newLeaf)
            newLeaf.parent = context.object
            extantLeaves.append(newLeaf)

    # put them all in position
    for leaf in extantLeaves:
        # bpy.ops.object.select_all(action='DESELECT')
        leafHeight = random.uniform(
            min, max)
        leaf.rotation_euler = [0, 0, random.uniform(0, 359)]
        leaf.location = [floatLerp(
            stemProp.stemScaleBottom*.01,
            stemProp.stemScaleTop*.01,
            leafHeight),
            0,
            leafHeight * stemSize]
        # random z rotation around stem

    return


def prepareFlowers(context, flowerObj, flowerPos, stemSize, stemProp):
    if flowerObj.parent is not context.object:
        flowerObj.parent = context.object
    flowerObj.location = [0, 0, floatLerp(stemSize, 0, flowerPos)]
    flowerObj.rotation_euler = [0, 0, random.uniform(0, 359)]
    return


def unused():
    bpy.ops.transform.rotate(
        value=random.uniform(0, 359), orient_axis='Z', orient_type='LOCAL',
        orient_matrix=leaf.matrix_local.to_3x3(),
        orient_matrix_type='LOCAL',
        constraint_axis=(False, False, True),
        mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH', proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False)
    # move up in the range, assuming leaf range is 0-1
    # across given length of stem
    bpy.ops.transform.translate(
        value=(
            floatLerp(
                stemProp.stemScaleBottom*.01,
                stemProp.stemScaleTop*.01,
                leafHeight),
            0,
            leafHeightAdjusted),
        orient_type='LOCAL',
        orient_matrix=leaf.matrix_local.to_3x3(),
        orient_matrix_type='LOCAL',
        constraint_axis=(False, False, True),
        mirror=True, use_proportional_edit=False,
        proportional_edit_falloff='SMOOTH',
        proportional_size=1,
        use_proportional_connected=False,
        use_proportional_projected=False)
