f = open(filename, "r")
lines = f.read().split("\n")

verts = []

for line in lines:
    tokens = line.split(" ")
    if tokens[0] = "v": # is a vertex
        coords = [float(coord) for coord in tokens[2:]]
        verts.append(coords)

    if tokens[0] = "f": #definings a face
        verts_needed = []
        for token in tokens:
            face_infos = token.split("/")
            verts_neededa.ppend(face_infos[0])

        #nowdraw in the face:
        if verts_needed == 4:

        if verts_needed == 3:
