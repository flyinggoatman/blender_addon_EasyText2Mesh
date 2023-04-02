# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.




bl_info = {
    "name": "EasyText2Mesh",
    "author": "flyinggoatman",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "3D View > Tool Shelf > EasyText2Mesh, Right-click Context Menu",
    "description": "Convert text objects to mesh and improve geometry",
    "category": "Object",
}

import bpy

def convert_text_to_mesh_and_improve_geometry(text_obj):
    if text_obj.type != 'FONT':
        print("Selected object is not a text object.")
        return

    # Make a copy of the text object and make it active
    bpy.ops.object.select_all(action='DESELECT')
    text_obj.select_set(True)
    bpy.ops.object.duplicate()
    duplicated_text_obj = bpy.context.active_object

    # Convert the duplicated text object to a mesh object
    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object

    # Switch to edit mode and perform limited dissolve to improve geometry
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665)  # 5-degree angle limit
    bpy.ops.object.mode_set(mode='OBJECT')

    # Remove the original text object
    bpy.data.objects.remove(text_obj)

class EASYText2MESH_OT_convert(bpy.types.Operator):
    bl_idname = "object.easyText2mesh_convert"
    bl_label = "Convert Text to Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'FONT':
            self.report({'ERROR'}, "Please select a text object")
            return {'CANCELLED'}

        convert_text_to_mesh_and_improve_geometry(obj)

        return {'FINISHED'}

class EASYTEXT2MESH_PT_panel(bpy.types.Panel):
    bl_idname = "EASYTEXT2MESH_PT_panel"
    bl_label = "EasyText2Mesh"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "EasyText2Mesh"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Convert text object to mesh:")
        layout.operator(EASYText2MESH_OT_convert.bl_idname)

def draw_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(EASYText2MESH_OT_convert.bl_idname)

def register():
    bpy.utils.register_class(EASYText2MESH_OT_convert)
    bpy.utils.register_class(EASYTEXT2MESH_PT_panel)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_func)

def unregister():
    bpy.utils.unregister_class(EASYText2MESH_OT_convert)
    bpy.utils.unregister_class(EASYTEXT2MESH_PT_panel)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_func)

if __name__ == "__main__":
    register()
