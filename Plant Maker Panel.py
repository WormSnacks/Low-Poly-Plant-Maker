import bpy


class PlantMakerPanel(bpy.types.Panel):
    bl_idname = "_PT_PlantPanel"
    bl_label = "Plant Maker Panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        if context.object.type == 'MESH':
            return (context.object.data.stem_properties.isStemObject)
        else:
            return False

    def draw_header(self, context):
        layout = self.layout
        layout.label(text="")

    def draw(self, context):
        layout = self.layout
    
        stemProp = context.object.data.stem_properties

        col = layout.column()
        col.label(text="Object Data")
        col.prop(stemProp,
                    "flowerHeadMeshOne", text="Flower One")
        col.prop(stemProp,
                    "flowerHeadMeshTwo", text="Flower Two")
        col.prop(stemProp,
                    "leafMeshOne", text="Leaf One")
        col.prop(stemProp,
                    "leafMeshTwo", text="Leaf Two")
        col.prop(stemProp,
                    "leafMeshThree", text="Leaf Three")
        col.prop(stemProp,
                    "hairParticleObj", text="Hair Particle Object")

        col = layout.column()
        col.label(text="Stem Data")
        col.prop(stemProp,
                    "stemScaleHeightMax", text="Maximum Stem Height")
        col.prop(stemProp,
                    "stemScaleHeightMin", text="Minumum Stem Height")
        col.prop(stemProp,
                    "stemScaleBottom", text="Bottom of Stem Width")
        col.prop(stemProp,
                    "stemScaleTop", text="Top of Stem Width")
        col.prop(stemProp,
                    "stemResolution", text="Vertical Resolution")

        col = layout.column()
        col.label(text="Flower Data")
        if stemProp.flowerHeadMeshOne is not None:
            col.prop(stemProp,
                        "flowerOnePos", text="Flower One Pos 0-1")
        if stemProp.flowerHeadMeshTwo is not None:
            col.prop(stemProp,
                        "flowerTwoPos", text="Flower Two Pos 0-1")

        col = layout.column()
        col.label(text="Leaf Data")
        col.prop(stemProp,
                    "leafPosRangeMin", text="Leaf Distribution Bottom")
        col.prop(stemProp,
                    "leafPosRangeMax", text="Leaf Distribution Top")
        if stemProp.leafMeshOne is not None:
            col.prop(stemProp,
                        "leafOneNum", text="Number of Leaf Ones")
        if stemProp.leafMeshTwo is not None:
            col.prop(stemProp,
                        "leafTwoNum", text="Number of Leaf Twos")
        if stemProp.leafMeshThree is not None:
            col.prop(stemProp,
                        "leafThreeNum", text="Number of Leaf Threes")

        col = layout.column()
        col.label(text="Particle System Data")
        if stemProp.hairParticleObj is not None and stemProp.baseStemObj is None:
            col.prop(stemProp, "heightFalloffFromCenter",
                        text="Relative height falloff from center")
            col.operator("mesh.stem_apply")
        elif stemProp.baseStemObj is not None:
            col.prop(stemProp, "baseStemObj", text="Duplicate of")


        col = layout.column()
        col.operator("mesh.stem_randomizer")

# bpy.utils.register_class(PlantMakerPanel)
