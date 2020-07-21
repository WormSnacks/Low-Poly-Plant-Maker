import bpy


class CurveApplicator(bpy.types.Operator):
    """applies meshes to curves"""
    bl_idname = "plant.curve_applicator"
    bl_label = "Applies Plant Maker meshes to a collection of curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        n = -1
        meshObjs = []
        curveObjs = []

        # Iterate through all selected objects, select mesh objects, add to meshObjs,
        # bezier curves are added to curveObjs, children of meshObjs to be added later
        for obj in self.meshCollection:
            if obj.type == "MESH" and obj.parent is None:
                meshObjs.append(obj)
            # elif obj.type == "CURVE" and obj.parent is not None:
                # meshObjs.append(obj)
        for curve in self.curveCollection:
            if obj.type == "CURVE" and obj.parent is None:
                curveObjs.append(obj)

        for obj in meshObjs:
            n = n+1
            operatingObjs = []
            operatingObjs.append(meshObjs[n])
            # print(meshObjs[n-1].name)
            for ob in obj.children:
                operatingObjs.append(ob)
                for o in ob.children:
                    operatingObjs.append(o)
                    for b in o.children:
                        operatingObjs.append(b)

            targetCurve = curveObjs[n]

            obj.location = targetCurve.location
            obj.rotation_euler[0] = 0
            obj.rotation_euler[1] = 0

            for ob in operatingObjs:
                for mod in ob.modifiers:
                    if mod.type == "CURVE":
                        mod.object = targetCurve

        return{'FINISHED'}

    def register():
        print("curve applicator registered")

    def unregister():
        print("curve applicator unregistered")
