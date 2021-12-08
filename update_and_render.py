import bpy
import sys
import mathutils
import _cycles
from os import sep
from bpy_extras.io_utils import axis_conversion
argv = sys.argv
argv = argv[argv.index("--") + 1:]
path = '//render'

# --- Args ---
camera_position = {}
camera_rotation = {}
textures = []
colors = []
image_size = {"height": None, "width":None}


scene = bpy.data.scenes["Scene"]
scene.render.use_border = True
rot_axis_conv_matrix = axis_conversion(from_forward='Z',
        from_up='Y',
        to_forward='-Y',
        to_up='Z').to_4x4()


scene = bpy.context.scene
scene.cycles.device = 'GPU'
GPU_RENDERING = False

cycles_preferences = bpy.context.preferences.addons['cycles'].preferences
cuda_devices, opencl_devices = cycles_preferences.get_devices()
for device in cuda_devices:
    if device.use == True:
        GPU_RENDERING = True

if GPU_RENDERING:
    scene.render.tile_x = 512
    scene.render.tile_y = 512
else: 
    scene.render.tile_x = 64
    scene.render.tile_y = 64
        



def render_scene():
    print('start render')
    #scene.render.filepath = path + './test.png'
    bpy.ops.render.render(write_still=True)


def set_camera_position(x, y, z, up):
    if up == '+y':
        scene.camera.location.x = x
        scene.camera.location.y = -z
        scene.camera.location.z = y

def set_camera_rotation(x, y, z, w, up):
    if up == '+y':
        quat = mathutils.Quaternion([w, x, y, z])
        #print(quat.to_matrix())
        #print(rot_axis_conv_matrix)
        rot_matrix = rot_axis_conv_matrix @ quat.to_matrix().to_4x4()
        scene.camera.matrix_world =  rot_matrix

def change_textures():
    for tex in textures:
        print('tex', tex)
        for image in bpy.data.images:
            if image.filepath.split(sep)[-1] == tex['org_tex_name']:
                image.filepath = tex['new_tex_path']
                image.reload()

def change_image_size():
    scene.render.resolution_x = int(image_size['width'])
    scene.render.resolution_y = int(image_size['height'])
    scene.render.resolution_percentage = 100

def change_colors():
    for color in colors:
        color_list = list(int(color["color"].split('#')[1][i:i+2], 16) / 255 for i in (0, 2, 4))
        color_list.append(1)
        print('NODES: ', bpy.data.materials[color["material_name"]].node_tree.nodes)
        for node in bpy.data.materials[color["material_name"]].node_tree.nodes:
            if node.label == color["color_name"]:
                node.outputs[0].default_value = tuple(color_list)

def process_args():
    index = 0
    while index < len(argv):
        if argv[index] == 'CAMERA_POSITION':
            global camera_position
            camera_position = {
                'x': float(argv[index + 1]),
                'y': float(argv[index + 2]),
                'z': float(argv[index + 3]),
                'up': '+y'
            }
            index += 3
        elif argv[index] == 'CAMERA_ROTATION':
            global camera_rotation
            camera_rotation = {
                'x': float(argv[index + 1]),
                'y': float(argv[index + 2]),
                'z': float(argv[index + 3]),
                'w': float(argv[index + 4]),
                'up': '+y'
            }
            index += 4
        elif argv[index] == 'IMAGE_SIZE':
            global image_size
            image_size['height'] = argv[index + 1]
            image_size['width'] = argv[index + 2]
            print(argv[index + 1])
            index += 2
        elif argv[index] == 'TEXTURE':
            global textures
            textures.append({
                'org_tex_name': argv[index + 1],
                'new_tex_path': argv[index + 2]
            })
            index += 2
        elif argv[index] == 'COLOR':
            global colors
            colors.append({
                'material_name': argv[index +1],
                'color_name':  argv[index +2],
                'color': argv[index +3]
            })
        index += 1

def main():
    process_args()
    set_camera_rotation(camera_rotation['x'], camera_rotation['y'], camera_rotation['z'], camera_rotation['w'], '+y')
    set_camera_position(camera_position['x'], camera_position['y'], camera_position['z'], '+y')
    change_textures()
    change_colors()
    if image_size['height'] != None and image_size['width'] != None:
        change_image_size()
    print(textures)
    render_scene()
    print('RENDERING FINISHED')


if __name__ == "__main__":
    main()
