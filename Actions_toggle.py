bl_info = {
    "name": "Anim Flag",
    "author": "Your Name Here",
    "version": (0, 0, 1),
    "blender": (2, 91, 2),
    "location": "View3D > UI > bool vec",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "category": "Development",
    "support": "TESTING"
}

import bpy


def flag_all(self, context):
    actions = bpy.data.actions
    scn_pg = context.scene.MyPropertyGroup
    for k in actions.keys():
        actions[k].MyPropertyGroup.flag_anim_bool = scn_pg.flag_all_bool
    return None


class ANIM_FLAG_PG(bpy.types.PropertyGroup):
    flag_all_bool: bpy.props.BoolProperty(
        name="flag_all_bool",
        description="",
        default=False,
        update=flag_all,
        )


class IND_ANIM_FLAG_PG(bpy.types.PropertyGroup):
    flag_anim_bool: bpy.props.BoolProperty(
        name="flag_anim_bool",
        description="",
        default=False,
        )


class EXPORT_ACTIONS_OT_from_selected(bpy.types.Operator):
    bl_idname = 'export_actions.from_selected'
    bl_label = "Export"

    def execute(self, context):
        print(f"{self.bl_idname} pressed")
        actions = [
            k for k in bpy.data.actions.keys()
            if bpy.data.actions[k].MyPropertyGroup.flag_anim_bool
            ]
        if not actions:
            print("No Actions selected")
        for action in actions:
            print(action)
        return {'FINISHED'}


class Anim_Export_Panel(bpy.types.Panel):
    """Creates a Panel in the VIEW_3D UI window"""
    bl_label = "Action Key Panel"
    bl_idname = "ACTION_PT_helper"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Example"

    def draw(self, context):
        scene = context.scene
        props = scene.MyPropertyGroup
        layout = self.layout
        col = layout.column()
        col.prop(props, "flag_all_bool", text="SELECT ALL")
        box = layout.box()
        col = box.column(align=True)
        col.label(text="Existing action keys")
        for k in bpy.data.actions.keys():
            col.prop(
                bpy.data.actions[k].MyPropertyGroup, "flag_anim_bool", text=k
                )
        col = layout.column()
        col.operator('export_actions.from_selected', text="Do Something")


classes = [
    Anim_Export_Panel,
    ANIM_FLAG_PG,
    IND_ANIM_FLAG_PG,
    EXPORT_ACTIONS_OT_from_selected,
    ]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.MyPropertyGroup = bpy.props.PointerProperty(
            type=ANIM_FLAG_PG)
    bpy.types.Action.MyPropertyGroup = bpy.props.PointerProperty(
            type=IND_ANIM_FLAG_PG)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.MyPropertyGroup
    del bpy.types.Action.MyPropertyGroup


if __name__ == "__main__":
    register()
