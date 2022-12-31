#!/usr/bin/env python3
import sys
from utils import *

def help_msg():
    return """
    Rule 110 Phase Space Mapper
    Use this application to view different graphs of Rule 110

    ./script <outfile=path> <config=path> <bin=False> <state=False> <phase=False>

    outfile (required): path for output package
    config (required): path to configuration for Mapper
    bin: png of binary graph
    state: png of states graph
    phase*: png of phase space graph   

    * output only if at least bin or state is set
    """

def get_arg(arg):
    out = [x.split("=")[1] for x in sys.argv if arg in x]
    if len(out) < 1:
        return ""

    return out[0]


#Config Format: each line -> <initial condition> <# gens> 
#returns a list of integer lists 
def parse_config(cf_path):
    out = []
    with open(cf_path) as cf:
        lines = cf.readlines()
        for l in lines:
            parts = l.split(",")
            lstore = "" 
            gstore = 0
            if len(parts) > 1:
                lstore = parts[0]
                gstore = int(parts[1])
            pair = (lstore, gstore)
            
            if len(pair) > 1:
                out.append(pair)
    
    return out

#check for minimum arg length
if len(sys.argv) < 3:
    print(help_msg())
    exit()

outfile = get_arg("outfile=")
config = get_arg("config=")

#parse these to boolean
bin = get_arg("bin=")
state = get_arg("state=")
phase = get_arg("phase=")

#check for required vars
if outfile == "" or config == "":
    print(help_msg())
    exit()

#run rules and parse output options
fcnt = 0
for ic, gens in parse_config(config):
    bin_lat = gen_lattice(ic, gens)
    stat_lat = lattice_states(bin_lat)
    if bin == "True":
        save_lattice(bin_lat, outfile + "_bin_" + str(fcnt) + ".png", binary=True) 
    if state == "True":
        save_lattice(stat_lat, outfile + "_state_" + str(fcnt) + ".png", binary=False) 
    if phase == "True":
        verts = []
        edges = []
        
        if bin == "True":
            verts, edges = parse_verts_edges(bin_lat)
            draw_graph(verts, edges, outfile+"_binphase_" + str(fcnt) + ".png")
        if state == "True":
            verts, edges = parse_verts_edges(stat_lat)
            draw_graph(verts, edges, outfile+"_statephase_" + str(fcnt) + ".png")
    fcnt += 1

#TODO I want to be able to look at the graphs without needing all the other output