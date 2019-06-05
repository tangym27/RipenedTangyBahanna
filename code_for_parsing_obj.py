# notes on parsing obj files 
# "Faces are defined using lists of vertex, texture and normal indices which start at 1"

f = open(filename, "r")
lines = f.read().split("\n")

verts = ["placeholder"]

for line in lines:
    tokens = line.split(" ")
    if tokens[0] = "v": # is a vertex
        coords = [float(coord) for coord in tokens[2:]]
        verts.append(coords)

    if tokens[0] = "f": #definings a face
        verts_needed = []
        for token in tokens:
            face_infos = token.split("/")
            verts_needed.append(int(face_infos[0]))

        #AS OF THIS POINT: index n of vertex contains the nth verticies, which is [x,y,z], where x y z are floats
        #verts_needed is a list of either 3 or 4 verticies (by number), and they are all integers

        #nowdraw in the face:

        if verts_needed == 4:
            add_polygon(polygons, verts_needed[0], verts_needed[1], verts_needed[2])
        if verts_needed == 3:
            add_polygon(polygons, verts_needed[0], verts_needed[1], verts_needed[2])

