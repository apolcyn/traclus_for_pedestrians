'''
Created on Dec 29, 2015

@author: Alex
'''
from planar import Line
from planar import Vec2
import math

def get_longer_line(line_a, line_b):
    if line_a.length >= line_b.length:
        return line_a
    else:
        return line_b
    
def get_shorter_line(line_a, line_b):
    if line_a.length < line_b.length:
        return line_a
    else:
        return line_b
    
def get_total_distance_function(perp_dist_func, angle_dist_func, parrallel_dist_func):
    def __dist_func(line_a, line_b, perp_func=perp_dist_func, angle_func=angle_dist_func, \
                    parr_func=parrallel_dist_func):
        return perp_func(line_a, line_b) + angle_func(line_a, line_b) + \
            parr_func(line_a, line_b)
    return __dist_func

def _perp_dist_longer_line_known(longer_line, shorter_line):
    dist_a = longer_line.wrapped_inf_line.project(shorter_line.wrapped_start).distance_to(shorter_line.wrapped_start)
    dist_b = shorter_line.wrapped_inf_line.project(shorter_line.wrapped_end).distance_to(shorter_line.wrapped_end)
    
    if dist_a == 0.0 and dist_b == 0.0:
        return 0.0
    else:
        return (math.pow(dist_a, 2) + math.pow(dist_b, 2)) / (dist_a + dist_b)
    
def dist_func_longer_finder(dist_func, line_a, line_b):
    if line_a.line_seg == get_longer_line(line_a, line_b):
        return dist_func(longer_line=line_a, shorter_line=line_b)
    else:
        return dist_func(longer_line=line_b, shorter_line=line_a)
    
def perpendicular_distance(line_a, line_b):
    return dist_func_longer_finder(_perp_dist_longer_line_known, line_a, line_b)

def _angular_dist_longer_known(longer_line, shorter_line):
    angle_in_radians = math.radians(longer_line.direction.angle_to(shorter_line.direction))
    sine_coefficient = math.sin(angle_in_radians) 
    
    return abs(sine_coefficient * shorter_line.length)

def angular_distance(line_a, line_b):
    return dist_func_longer_finder(_angular_dist_longer_known(line_a, line_b))

def _parr_dist_longer_known(longer_line, shorter_line):
    dist_a = dist_to_projection_point(longer_line, longer_line.line.project(shorter_line.start))
    dist_b = dist_to_projection_point(longer_line, longer_line.line.project(shorter_line.end))
    
def parrallel_distance(line_a, line_b):
    return dist_func_longer_finder(_parr_dist_longer_known, line_a, line_b) 
    
def dist_to_projection_point(line, proj):
    return min(proj.distance_to(line.start), proj.distance_to(line.end))