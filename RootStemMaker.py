import bpy
import bmesh


class OBJECT_OT_StemMaker(bpy.types.Operator):
    """applies meshes to curves"""
    bl_idname = "mesh.makestem"
    bl_label = "Make Stem"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return True
        return False

    def execute(self, context):
        stem = bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.01, depth=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.5))
        context.active_object.name = "Stem"
        curserPrevLoc = context.scene.cursor.location
        context.scene.cursor.location = [0, 0, 0]
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        context.scene.cursor.location = curserPrevLoc

        # Need enter edit Mode?
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.cylinder_project(
            direction='ALIGN_TO_OBJECT', clip_to_bounds=False, scale_to_bounds=True)
        bpy.ops.object.editmode_toggle()

        # Finally add custom properties
        # context.active_object = stem
        # context.active_object.stem_properties = bpy.props.CollectionProperty(type=StemProperties)
        context.object.data.stem_properties.isStemObject = True
        # # print(context.active_object.data.stem_properties.stemScaleBottom)

        return{'FINISHED'}

    def register():
        # bpy.utils.register_class(OBJECT_OT_add_object)
        # bpy.utils.register_manual_map(add_object_manual_map)
        bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)

    def unregister():
        # bpy.utils.unregister_class(OBJECT_OT_add_object)
        # bpy.utils.unregister_manual_map(add_object_manual_map)
        bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

    if __name__ == "__main__":
        register()


def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_StemMaker.bl_idname,
        text="Plant Maker Stem",
        icon='PLUGIN')


class StemProperties(bpy.types.PropertyGroup):
    # Editing Info
    stemScaleHeightMax: bpy.props.FloatProperty(min=0, soft_max=5, default=0.8)
    stemScaleHeightMin: bpy.props.FloatProperty(min=0, soft_max=5, default=0.8)
    stemScaleBottom: bpy.props.FloatProperty(min=0.1, soft_max=2, default=1)
    stemScaleTop: bpy.props.FloatProperty(min=0.1, soft_max=2, default=1)
    stemScaleOriginalRadius: bpy.props.FloatProperty(
        min=0.01, max=0.011, default=0.01)
    stemResolution: bpy.props.IntProperty(min=0, soft_max=25, default=10)
    # range of 0 to 1 based on height of stem
    leafPosRangeMin: bpy.props.FloatProperty(min=0, max=1, default=0.0)
    leafPosRangeMax: bpy.props.FloatProperty(min=0, max=1, default=0.5)
    flowerOnePos: bpy.props.FloatProperty(min=0, max=1, default=0.95)
    flowerTwoPos: bpy.props.FloatProperty(min=0, max=1, default=0.95)
    leafScaleVariance: bpy.props.FloatProperty(min=0, soft_max=1, default=0.1)
    scaleLeafZOnly: bpy.props.BoolProperty(default=True)
    # number of Leaves
    leafOneNum: bpy.props.IntProperty(min=0, soft_max=25, default=10)
    leafTwoNum: bpy.props.IntProperty(min=0, soft_max=25, default=10)
    leafThreeNum: bpy.props.IntProperty(min=0, soft_max=25, default=10)

    # Mesh Names
    # flowerHeadMeshOneName: bpy.props.StringProperty()
    # flowerHeadMeshTwoName: bpy.props.StringProperty()
    # leafMeshOneHolderName: bpy.props.StringProperty()
    # leafMeshTwoHolderName: bpy.props.StringProperty()
    # leafMeshThreeName: bpy.props.StringProperty()

    # Mesh Pointer Properties
    flowerHeadMeshOne: bpy.props.PointerProperty(
        name="Flower Head Type 1", type=bpy.types.Object)
    flowerHeadMeshTwo: bpy.props.PointerProperty(
        name="Flower Head Type 2", type=bpy.types.Object)
    leafMeshOne: bpy.props.PointerProperty(
        name="Leaf Type 1", type=bpy.types.Object)
    leafMeshTwo: bpy.props.PointerProperty(
        name="Leaf Type 2", type=bpy.types.Object)
    leafMeshThree: bpy.props.PointerProperty(
        name="Leaf Type 3", type=bpy.types.Object)

    isStemObject: bpy.props.BoolProperty()

    # All information for copying across particle system
    baseStemObj: bpy.props.PointerProperty(
        name="Base Stem", type=bpy.types.Object)
    hairParticleObj: bpy.props.PointerProperty(
        name="Hair Particle Obj", type=bpy.types.Object)
    # 0-1 range exponential fall off relative to total height
    heightFalloffFromCenter: bpy.props.FloatProperty(min=0, max=1, default=0.1)

    def register():
        # bpy.utils.register_class(StemProperties)
        bpy.types.Mesh.stem_properties = bpy.props.PointerProperty(
            type=StemProperties)

    # def unregister():
        # bpy.utils.unregister_class(StemProperties)
