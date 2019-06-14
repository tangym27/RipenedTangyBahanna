# Hanna Yang && Michelle Tang: Team RipenedTangyBahanna

** note that also in our mesh parsing we multiply the verticies by 6 to scale our included .obj file to the right size, and we only deal with .obj files that handle faces that are specified in / / / form.

### Changes in scripting language
light takes in either 10 or 14 arguments:
* light (name of light) (posiiotion args) (intensity args) (knob for position) (knob for color)
* light (name of light) (position args) (intensity args) (knob for x position) (knob for y position) (knob for z position) (knob for red) (knob for green ) (knob for blue)
** note that varying (knob for position) actually doesn't do anything to the light, since values are normalized.

Naming conventions that must be followed:
* knob for position of light must have first 8 characters "location" 
* knob for hue of color must have first 5 characters "color"
* knob for x position of light must have first 4 characters "xcor", and same for y and z
* knob for red light must have first 3 characters "red" (for example, "red333" is a valid name, but "3red" is not.)
* to be safe, make sure you don't name any other knobs with these names (location, color, red, green, blue, xcor, ycor, zcor)

### List of features we implemented
* Mesh
* Phong and Gouraud Shading
* Using vary to move the light position / color
* Specifying light sources and having multiple of them
