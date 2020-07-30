import bpy
import bmesh
import random
import mathutils
import math


def get_heirs(ob, levels=10):
    def recurse(ob, parent, depth, childlist):
        if depth > levels:
            return childlist
        # print("  " * depth, ob.name)

        for child in ob.children:
            childlist.append(child)
            recurse(child, ob,  depth + 1, childlist)
        return childlist
    childlist = []
    return recurse(ob, ob.parent, 0, childlist)


def floatLerp(a, b, c):
    return (c*a)+((1-c) * b)


def scaleRange(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]


def easeOutCubic(x):
    return (1 - pow(1 - x, 2))


def copyObj(obj, parent=None):
    nobj = obj.copy()
    if obj.type != 'EMPTY':
        nobj.data = obj.data.copy()
    nobj.animation_data_clear()
    # nobj.users_collection[0].objects.unlink(nobj)
    if parent is not None:
        nobj.parent = parent
        parent.users_collection[0].objects.link(nobj)
    
    return nobj


def measure(first, second):

    locx = second[0] - first[0]
    locy = second[1] - first[1]
    locz = second[2] - first[2]

    distance = math.sqrt((locx)**2 + (locy)**2 + (locz)**2)
    return distance
