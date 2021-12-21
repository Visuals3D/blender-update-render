# blender-update-render
A pythonscript for blender to allow manipulating a scene and start a render via the shell with some commands that can be added

This allows to reposition and rotate the camera to a new location, change textures and colors of specific shaders to allow minimal customisation without having to open the blender UI for it. 

## Execute

The script can be used as a parameter on a normal blender cli call in the shell like so:

```shell
blender --background ./file.blend -P ./update_and_render.py
```

This way a render process will start. To manipulate anything before starting the render some arguments have to be provided as described below. If possible the script will try to use a GPU for rendering. But it does not work as reliable as just setting the render mode to GPU in the blender file itself.

## Changing Camera

To change the position of the camera in the blender scene provide x, y and z coordinates as well as rotation quaternion values x,y,z and w.

```shell
blender --background ./file.blend -P ./update_and_render.py -- CAMERA_POSITION <X> <Y> <z> CAMERA_ROTATION <X> <Y> <Z> <W>
```

## Changing Image Size

Changing the size of the image that will be rendered provide a HEIGHT and WIDTH in pixel like so:

```shell
blender --background ./file.blend -P ./update_and_render.py -- IMAGE_SIZE <HEIGHT> <WIDTH>
```

## Changing Textures

A textur can be changed by providing the name of the texture file in the scene. This means the texture import Node in the shader has to have the same name as the file it imports and needs to be provided in TEXTURE_NAME.

To replace the texture just set a path to the new Texture file with TEXTURE_PATH

```shell
blender --background ./file.blend -P ./update_and_render.py -- TEXTURES <TEXTURE_NAME> <TEXTURE_PATH>
```

## Changing Colors

Changing colors is limited to RGB Nodes in shaders within the same material. If multiple materials have to change color the COLOR command hast to be repeated with all three arguments. 

MATERIAL_ID is the name of the shader. COLOR_NODE_ID is the name of the RGB node inside the shader that will change color and HEX_COLOR is the color itself provided in hex format.

```shell
blender --background ./file.blend -P ./update_and_render.py -- COLOR <MATERIAL_ID> <COLOR_NODE_ID> <HEX_COLOR>
```
