import bpy
import json
from bpy_extras.io_utils import ExportHelper, ImportHelper
from .utilfuncs import *

def draw_panel(layout):
    row = layout.row()
    row.operator('retarget.load', icon='FILEBROWSER')
    row.operator('retarget.save', icon='FILE_TICK')
    row.operator('retarget.automap', icon='AUTO')

class LoadOperator(bpy.types.Operator, ImportHelper):
    bl_idname = 'retarget.load'
    bl_label = 'Load Config'
    bl_description = 'Load a previously saved configuration'

    filter_glob: bpy.props.StringProperty(
        default='*.rtconf',
        options={'HIDDEN'},
        maxlen=255
    )

    def execute(self, context):
        with open(self.filepath, 'r') as f:
            state().from_serialized(json.load(f))
        return {'FINISHED'}

class SaveOperator(bpy.types.Operator, ExportHelper):
    bl_idname = 'retarget.save'
    bl_label = 'Save Config'
    bl_description = 'Save a configuration'
    filename_ext = '.rtconf'

    filter_glob: bpy.props.StringProperty(
        default='*.rtconf',
        options={'HIDDEN'},
        maxlen=255
    )

    def execute(self, context):
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(state().serialize()))

        return {'FINISHED'}

class AutomateMappingOperator(bpy.types.Operator):
    bl_idname = 'retarget.automap'
    bl_label = 'Automate Mapping'
    bl_description = 'Automatic mapping for bones with same names'
    
    def execute(self, context):
        s = state()
        for name, bone in s.source.pose.bones.items():
            if s.target.pose.bones.get(name):
                mapping = s.mappings.add()
                mapping.source = name
                mapping.target = name
                
        return {'FINISHED'}

classes = (
    LoadOperator,
    SaveOperator,
    AutomateMappingOperator
)