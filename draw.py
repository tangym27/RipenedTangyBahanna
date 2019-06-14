from display import *
from matrix import *
from gmath import *

def add_mesh(polygons, filename):
                # notes on parsing obj files
                # "Faces are defined using lists of vertex, texture and normal indices which start at 1"
    f = open(filename, "r")
    lines = f.read().split("\n")

    verts = ["placeholder"]


    for line in lines:
        tokens = line.split(" ")
        if tokens[0] == "v": # is a vertex
            coords = [5 * float(coord) for coord in tokens[2:]]
            verts.append(coords)

        if tokens[0] == "f": #definings a face
            verts_needed = []
            for token in tokens[1:-1]:
                face_infos = token.split("/")
                verts_needed.append(int(face_infos[0]))

            #AS OF THIS POINT: index n of vertex contains the nth verticies, which is [x,y,z], where x y z are floats
            #verts_needed is a list of either 3 or 4 verticies (by number), and they are all integers

            #nowdraw in the face:

            a = verts[verts_needed[0]]
            b = verts[verts_needed[1]]
            c = verts[verts_needed[2]]
            if len(verts_needed) == 4:
                d = verts[verts_needed[3]]
                add_polygon(polygons, a[0], a[1], a[2], b[0], b[1], b[2], c[0], c[1], c[2])
                add_polygon(polygons, a[0], a[1], a[2], c[0], c[1], c[2], d[0], d[1], d[2])
            if len(verts_needed) == 3:
                add_polygon(polygons, a[0], a[1], a[2], b[0], b[1], b[2], c[0], c[1], c[2])

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color, vertices, view, ambient, light, symbols, reflect, shading):
    # print vertices
    # exit()
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz
        # SWITCH EVERYTHING >:(  or else you get these funky trinagles which makes sense but whatever.)
        if shading == 'gouraud' or shading == 'phong':
            vertices = [vertices[1], vertices[0]]

    x = x0
    z = z0
    if shading != 'flat':
        r = vertices[0][0]
        g = vertices[0][1]
        b = vertices[0][2]
        #changes in the vertices
        dxr = (vertices[1][0] - vertices[0][0]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        dyg = (vertices[1][1] - vertices[0][1]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
        dzb = (vertices[1][2] - vertices[0][2]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        if shading == 'gouraud':
            gcolor = [ int(r), int(g), int(b)]
            plot(screen, zbuffer, gcolor, x, y, z)
        elif shading == 'phong':
            ppcolor = [0,0,0]
            for lit in light:
                pcolor = get_lighting([r,g,b] , view, ambient, lit, symbols, reflect )
                ppcolor[0] += pcolor[0]
                ppcolor[1] += pcolor[1]
                ppcolor[2] += pcolor[2]
            plot(screen, zbuffer, ppcolor, x, y, z)
        else:
            # flat
            # print color
            plot(screen, zbuffer, color, x, y, z)

        x+= 1
        z+= (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

        # update values based on those slopes
        if shading == 'gouraud' or shading == 'phong':
            r += dxr
            g += dyg
            b += dzb

def scanline_convert(polygons, point, screen, zbuffer, end_vert, view, ambient, light, symbols, reflect, shading):
    # print point
    flip = False
    BOT = 0
    TOP = 2
    MID = 1
    END = 3

    points = [ (polygons[point][0], polygons[point][1], polygons[point][2], end_vert[0] ),
               (polygons[point+1][0], polygons[point+1][1], polygons[point+1][2], end_vert[1]),
               (polygons[point+2][0], polygons[point+2][1], polygons[point+2][2], end_vert[2]) ]

    points.sort(key = lambda y: y[1])
    x0 = x1 = points[BOT][0]
    z0 = z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1

    dx0 = (points[TOP][0] - x0) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - z0) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - x1) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - z1) / distance1 if distance1 != 0 else 0

    if shading != 'flat':
        xr0 = xr1 = points[BOT][END][0]
        yg0 = yg1 = points[BOT][END][1]
        zb0 = zb1 = points[BOT][END][2]

        dxr0 = (points[TOP][3][0] - xr0) / distance0 if distance0 != 0 else 0
        dyg0 = (points[TOP][3][1] - yg0) / distance0 if distance0 != 0 else 0
        dzb0 = (points[TOP][3][2] - zb0) / distance0 if distance0 != 0 else 0
        dxr1 = (points[MID][3][0] - xr0) / distance1 if distance1 != 0 else 0
        dyg1 = (points[MID][3][1] - yg0) / distance1 if distance1 != 0 else 0
        dzb1 = (points[MID][3][2] - zb0) / distance1 if distance1 != 0 else 0

    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = not flip

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            xr1 = points[MID][3][0]
            yg1 = points[MID][3][1]
            zb1 = points[MID][3][2]


            if shading != 'flat':
                dxr1 = (points[TOP][3][0] - xr1) / distance2 if distance2 != 0 else 0
                dyg1 = (points[TOP][3][1] - yg1) / distance2 if distance2 != 0 else 0
                dzb1 = (points[TOP][3][2] - zb1) / distance2 if distance2 != 0 else 0

                xr1 = points[MID][3][0]
                yg1 = points[MID][3][1]
                zb1 = points[MID][3][2]



        color = end_vert if shading == 'flat' else None
        vertices = [[xr0, yg0, zb0], [xr1, yg1, zb1]] if shading != 'flat' else []
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color, vertices, view, ambient, light, symbols, reflect, shading)

        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1

        if shading != 'flat':
            xr0 += dxr0
            yg0 += dyg0
            zb0 += dzb0
            xr1 += dxr1
            yg1 += dyg1
            zb1 += dzb1
        y+= 1




def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def draw_polygons( polygons, screen, zbuffer, shading, view, ambient, lights, symbols, reflect):
    if len(polygons) < 2:
        print ('Need at least 3 points to draw')
        return

    if shading != 'flat':
        norms = {}
        pts = 0
        for pts in polygons:
            norms[tuple(pts)] = [0,0,0]
        #  reset
        pts = 0
        while pts < len(polygons) - 2:
            k = 0
            normal = calculate_normal(polygons, pts)
            normalize(normal)
            while (k < 3):
                # print k
                # print"done"
                norms[tuple(polygons[pts])][k] += normal[k]
                norms[tuple(polygons[pts+1])][k] += normal[k]
                norms[tuple(polygons[pts+2])][k] += normal[k]
                k += 1
            pts += 3

        for key in norms.keys():
            normalize(norms[key])
        # print norms

    pts = 0
    while pts < len(polygons) - 2:

        normal = calculate_normal(polygons, pts)[:]

        #print normal
        if normal[2] > 0:
            if shading == 'flat':
                colors = [0,0,0]
                for light in lights:
                    c =  get_lighting(normal, view, ambient, light, symbols, reflect )
                    colors[0] += c[0]
                    colors[1] += c[1]
                    colors[2] += c[2]
                scanline_convert(polygons, pts, screen, zbuffer, colors,
                        view, ambient, light, symbols, reflect, shading )

            else:
                norm0 = norms[tuple(polygons[pts])]
                norm1 = norms[tuple(polygons[pts+1])]
                norm2 = norms[tuple(polygons[pts+2])]

                if shading == 'gouraud':
                    colors = [[0,0,0],[0,0,0],[0,0,0]]
                    for light in lights:
                        v0_color = get_lighting(norm0, view, ambient, light, symbols, reflect )
                        v1_color = get_lighting(norm1, view, ambient, light, symbols, reflect )
                        v2_color = get_lighting(norm2, view, ambient, light, symbols, reflect )
                        colors[0][0] += v0_color[0]
                        colors[0][1] += v0_color[1]
                        colors[0][2] += v0_color[2]
                        colors[1][0] += v1_color[0]
                        colors[1][1] += v1_color[1]
                        colors[1][2] += v1_color[2]
                        colors[2][0] += v2_color[0]
                        colors[2][1] += v2_color[1]
                        colors[2][2] += v2_color[2]

                    scanline_convert(polygons, pts, screen, zbuffer, colors, view, ambient, light, symbols, reflect, shading)

                if shading == 'phong':

                    normals = [norm0, norm1, norm2]
                    scanline_convert(polygons, pts, screen, zbuffer, normals, view, ambient, lights, symbols, reflect, shading)

        pts+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print ('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance= abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z+= dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z )
