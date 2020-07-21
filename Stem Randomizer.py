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
        return (context.view_layer.objects.active.data.stem_properties.isStemObject)

    def execute(self, context):

        stemObj = context.view_layer.objects.active
        stemProp = stemObj.data.stem_properties
        # resize stem, set to one first in case this has been done before
        random.seed()
        stemSize = random.uniform(stemProp.stemScaleHeightMin,
                                  stemProp.stemScaleHeightMax)
        # stemObject = bpy.data.objects[self.stemName]

        # stemMesh = bmesh.new()
        # stemMesh = bmesh.from_mesh(stemObject)

        # Subdivide previous resolutions, keeping top and bottom rings
        # if stemObj.mode is not 'EDIT':
        #     bpy.ops.object.mode_set(mode='EDIT')
#
        # bpy.ops.mesh.select_all(action='SELECT')
        # bpy.ops.mesh.dissolve_limited()
        # bpy.ops.mesh.select_face_by_sides(number=6)

        bm = bmesh.new()
        bm.from_mesh(stemObj.data)

        bm.faces.ensure_lookup_table()
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

        bm.edges.ensure_lookup_table()
        subDivEdges = []
        for edge in bm.edges:
            if edge not in topFace.edges and edge not in bottomFace.edges:
                subDivEdges.append(edge)

        topEdges = [ele for ele in topFace.edges
                    if isinstance(ele, bmesh.types.BMEdge)]
        bottomEdges = [ele for ele in bottomFace.edges
                       if isinstance(ele, bmesh.types.BMEdge)]

        bmesh.ops.delete(bm, geom=subDivEdges, context='EDGES')
        subDivEdges = bmesh.ops.bridge_loops(bm, edges=topEdges+bottomEdges)
        # bmesh.ops.dissolve_edges(bm, edges=subDivEdges)

        bmesh.ops.subdivide_edges(
            bm, edges=subDivEdges['edges'], cuts=stemProp.stemResolution, use_grid_fill=True,
            use_only_quads=True)

        bm.to_mesh(stemObj.data)
        bm.free()
        
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
    # stemProp = stemObj.data.stem_properties
    stemObj = context.view_layer.objects.active
    extantLeaves = []
    extantLeaves.append(stemObj)  # placeholder
    # print(context.view_layer.objects.active.name)
    leafname = ''
    if len(leafObj.name.split('.')) > 1:
        leafnamelist = leafObj.name.split('.')
        leafnamelist.pop()
        leafname = ''.join([str(elem) for elem in leafnamelist])
    else:
        leafname = leafObj.name
    for child in stemObj.children:

        if leafname in child.name and child is not leafObj:
            extantLeaves.append(child)

    # below implies that this is a root stem, not a copy
    # this way when we duplicate to apply to curves
    # we can still keep references to base stem leaves
    if stemProp.baseStemObj is None:
        if leafObj.parent is not stemObj:
            leafObj.parent = stemObj
    elif stemProp.baseStemObj is not None:
        
        newLeaf = leafObj.copy()
        newLeaf.data = leafObj.data.copy()
        newLeaf.animation_data_clear()
        stemObj.users_collection[0].objects.link(newLeaf)
        newLeaf.parent = stemObj

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
            stemObj.users_collection[0].objects.link(newLeaf)
            newLeaf.parent = stemObj
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
    stemObj = context.view_layer.objects.active
    if flowerObj.parent is not stemObj:
        flowerObj.parent = stemObj
    flowerObj.location = [0, 0, stemSize-flowerPos]
    flowerObj.rotation_euler = [0, 0, random.uniform(0, 359)]
    return

