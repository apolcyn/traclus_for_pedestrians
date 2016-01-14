'''
Created on Jan 5, 2016

@author: Alex
'''

from generator_initializer import GeneratorInitializer
from representative_trajectory_average_inputs import get_representative_trajectory_average_inputs
from planar import Point

def get_representative_line_from_trajectory_line_segments(trajectory_line_segments, min_vertical_lines, min_prev_dist):
    inputs = get_representative_trajectory_average_inputs(trajectory_line_segments=trajectory_line_segments, \
                                                          min_prev_dist=min_prev_dist, min_lines=min_vertical_lines)
    out = []
    for line_seg_averaging_input in inputs:
        vert_val = get_mean_vertical_coordinate_in_line_segments(line_seg_averaging_input)
        out.append(Point(line_seg_averaging_input['horizontal_position'], vert_val))
    return out

def interpolate_within_line_segment(line_segment, horizontal_coordinate):
    min_x = min(line_segment.start.x, line_segment.end.x)
    max_x = max(line_segment.start.x, line_segment.end.x)
    
    if not (min_x <= horizontal_coordinate and max_x >= horizontal_coordinate):
        raise Exception("horizontal coordinate " + str(horizontal_coordinate) + \
                        " not within horizontal range of line segment" + \
                        " with bounds " + str(min_x) + " and " + str(max_x))
    elif line_segment.start.y - line_segment.end.y == 0.0:
        return line_segment.start.y
    elif line_segment.start.x - line_segment.end.x == 0.0:
        return (line_segment.end.y - line_segment.start.y) / 2.0 + line_segment.start.y
    else:
        return (horizontal_coordinate - line_segment.start.x) / (line_segment.end.x - line_segment.start.x) * \
            (line_segment.end.y - line_segment.start.y) + line_segment.start.y        
        
def line_segment_averaging_set_iterable(line_segments_to_average):
    def generator(line_segments_group=line_segments_to_average):
        horizontal_coord = line_segments_group['horizontal_position']
        for seg in line_segments_group['lines']:
            yield {'horizontal_pos': horizontal_coord, 'line_seg': seg.line_segment}
    
    return GeneratorInitializer(generator)

def number_average(iter_ob, func):
    total = 0.0
    count = 0
    for item in iter_ob:
        total += func(item)
        count += 1
        
    if count == 0:
        raise Exception("no input given to take average of")
    else:
        return total / count
        
def get_mean_vertical_coordinate_in_line_segments(line_segments_to_average):
    def apply_interpolation_to_line_segment(interpolation_info):
        if interpolation_info['line_seg'] == None or interpolation_info['horizontal_pos'] == None:
            raise Exception("nil key. " + str(interpolation_info) + " was passed to apply_interpolation_to_line_segment")
        return interpolate_within_line_segment(interpolation_info['line_seg'], interpolation_info['horizontal_pos'])
       
    return number_average(line_segment_averaging_set_iterable(line_segments_to_average), \
                          apply_interpolation_to_line_segment)