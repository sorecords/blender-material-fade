# Blender Material Fade
The scripts creates in Blender 2.8. Shader Editor 2 node-groups:

### "Camera Range" node group

1. "Camera Range" node-group (can be used as a mix factor for transparency, or for creating real time fog, or any other way you like). Controls are:
Cut In - close cut (everything closer to camera than this point is colored in black)
Fade In - close end of fade in (everything between Fade In and Fade Out is white)
Fade Out - far start of fade out (from that point far fading starts)
Cut Out - far cut (everything farther than this point is black)
Exponent In - how sharp is closer fade
Exponent Out - how sharp is farther fade
All values represent the same Blender measure units, as the project.

For Input Value node inside the group the script adds driver which links its output value to the Active Camera "clip end" parameter, so if camera range is changed, node group still works correctly. 

### "Map Range"

2. "Map Range" - it is needed for the work of the main group, but can be also used separately. It just converts one range into another - pretty much like "Map Range" node from Animation Nodes but only within materials.
