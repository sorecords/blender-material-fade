# Blender Material Fade

### "Camera Range" node group

1. "Camera Range" node-group (can be used as a mix factor for transparency, or for creating real time fog, or any other way you like). Controls are:
Cut In - close cut (everything closer to camera than this point is colored in black)
Fade In - close end of fade in (everything between Fade In and Fade Out is white)
Fade Out - far start of fade out (from that point far fading starts)
Cut Out - far cut (everything farther than this point is black)
Exponent In - how sharp is closer fade
Exponent Out - how sharp is farther fade
All values represent the same Blender measure units, as your project.

### "Map Range"

2. "Map Range" - it is needed for the work of the main group, but can be also used separately. It just converts one range into another - pretty much like "Map Range" node from Animation Nodes but only within materials.
About the video. This is is an example of using "Camera Range" node for creating fog (I mean far-distanced atmospheric fog, not those rising smokes). It is rendered in Eevee. I've just inverted "Camera Range" node group output and plugged it into Emission socket of Principled BSDF node. That way of creating far-distance fog is much faster than using Volumetrics and feels much more comfortable than using Mist pass on Compositor because you can see the result realtime, immediately. The landscape in the video was made from subdivided plane using displace modifier and heightmap from terrain.party, material is procedural. Rising smokes are the particle system with planes always oriented towards camera, with procedural noises as a material.
