'''
Copyright (C) CURRENT_YEAR YOUR NAME
YOUR@MAIL.com

Created by YOUR NAME

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Plant Maker",
    "description": "A parametric low poly plant maker for Blender 2.83",
    "author": "Wren <w.masonblaug@gmail.com>",
    "version": (0, 0, 1),
    "blender": (2, 83, 0),
    "location": "View3D",
    "warning": "This addon is still in development.",
    #"wiki_url": "",
    "category": "Object" }


import bpy


# load and reload submodules
##################################

from . import auto_load

auto_load.init()

def register():
    auto_load.register()

def unregister():
    auto_load.unregister()