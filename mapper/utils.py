import igraph
from subprocess import call
from PIL import Image, ImageDraw

def rule110(current_gen, next_gen):
    # Iterate over each cell in the current generation
    for i in range(len(current_gen)):
        # Determine the state of the current cell and its neighbors
        left_neighbor = current_gen[i - 1] if i > 0 else current_gen[-1]
        right_neighbor = current_gen[i + 1] if i < len(current_gen) - 1 else current_gen[0]
        current_cell = current_gen[i]

        # Apply Rule 110 to determine the state of the cell in the next generation
        cells = str(left_neighbor) + str(current_cell) + str(right_neighbor)
        
        if cells == "000":
            next_gen[i] = 0
        elif cells == "001":
            next_gen[i] = 1
        elif cells == "010":
            next_gen[i] = 1
        elif cells == "011":
            next_gen[i] = 1
        elif cells == "100":
            next_gen[i] = 0
        elif cells == "101":
            next_gen[i] = 1
        elif cells == "110":
            next_gen[i] = 1
        elif cells == "111":
            next_gen[i] = 0

#iterate rule110 for gens # of times starting with initial condition
def gen_lattice(ic, gens):
    lattice = []
    current_gen = [int(x) for x in str(ic)]
    next_gen = [0] * len(current_gen)
    for i in range(gens):
        rule110(current_gen, next_gen)
        lattice.append(current_gen)
        current_gen = next_gen
        next_gen = [0] * len(current_gen)
    return lattice

def lattice_states(lattice):
    states = []
    #save initial conditions
    states.append(lattice[0]) 
    # Iterate over each cell in the current generation
    for i in range(len(lattice)):
        i += 1
        state = []
        for c in range(len(lattice[i-1])):

            # Determine the state of the current cell and its neighbors
            left_neighbor = lattice[i-1][c - 1] if c > 0 else lattice[i-1][-1]
            right_neighbor = lattice[i-1][c + 1] if c < len(lattice[i-1]) - 1 else lattice[i-1][0]
            current_cell = lattice[i-1][c]
        
            cells = str(left_neighbor) + str(current_cell) + str(right_neighbor)
            state.append(int(cells,2))
        
        states.append(state)
    return states

def save_lattice(lattice, name, binary=True, x_size=1, y_size=8):
    # Determine the size of the image based on the size of the lattice and the cell size
    width = len(lattice[0]) * x_size
    height = len(lattice)
    
    # Create a new image and a drawing context
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    # Iterate over each cell in the lattice and draw a black or white rectangle
    for l in range(len(lattice)):
        for i, cell in enumerate(lattice[l]):
            x = i * x_size
            y = l

            if binary:
                color = (0, 0, 0) if cell == 0 else (255, 255, 255)
            else:
                if cell == 0:
                    color = (0,0,0)
                if cell == 1:
                    color = (255,0,0)
                if cell == 2:
                    color = (255,255,51)
                if cell == 3:
                    color = (51, 255, 51)
                if cell == 4:
                    color = (51,255,255)
                if cell == 5:
                    color = (51,51,255)
                if cell == 6:
                    color = (255, 51, 255)
                if cell == 7:
                    color = (255, 255, 255)
            draw.rectangle((x, y, x + (x_size), y + (y_size)), fill=color)

    image.save(name)

def draw_graph(vertices, edges, name):
    # Create a Graph object
    g = igraph.Graph(directed=True)

    # Add vertices to the graph
    g.add_vertices(vertices)
    # Add edges to the grapA
    g.add_edges(edges)
    
    # Clean up unconnected vertices
    g.vs["name"] = vertices
    layout = g.layout_kamada_kawai()
    
    # Plot the graph
    plot = igraph.plot(g, target=name, vertex_label=g.vs["name"])
    plot.save(name)
    
def parse_verts_edges(lattice):
    #each cell in each generation in a vertex, map it to the next gen via an edge
    #collect a list of list of verts (verts for each gen)
    v_list = []
    for l in lattice:
        verts = []
        for i in range(len(l)):
            v = ""
            v += str(l[i-1]) if i > 0 else str(l[-1])
            v += str(l[i])
            v += str(l[i+1]) if i < len(l)-1 else str(l[0])
            verts.append(v)
        v_list.append(verts)

    edges = []
    #for each index in verts and vert list build an edge between the two
    for i in range(1, len(v_list)):
        for j in range(len(v_list[i])):
            edges.append((v_list[i-1][j], v_list[i][j]))

    out_verts = [v for verts in v_list for v in verts]
    out_verts = list(set(out_verts))
    out_edges = edges
    return (out_verts, out_edges)
"""
def parse_verts_edges(lattice):
    verts = [str(l) for l in lattice]

    edges = []
    for i in range(len(lattice)-1):
        edges.append((str(lattice[i]),str(lattice[i+1])))

    return (verts, edges)
"""