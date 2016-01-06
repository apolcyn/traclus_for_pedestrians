'''
Created on Jan 5, 2016

@author: Alex
'''

def interpolate_within_line_segment(line_segment, horizontal_coordinate):
    min_x = min(line_segment.start.x, line_segment.end.x)
    max_x = max(line_segment.start.x, line_segment.end.x)
    
    if not (min_x <= horizontal_coordinate and max_x >= horizontal_coordinate):
        raise Exception("horizontal coordinate not within horizontal range of line segment")
    
    return horizontal_coordinate / (line_segment.end.x - line_segment.start.x) * \
        (line_segment.end.y - line_segment.start.y) + line_segment.start.y
        
def apply_interpolation_to_line_segment(interpolation_info):
    interpolate_within_line_segment(interpolation_info['line_seg'], interpolation_info['horizontal_pos'])
        
def line_segment_averaging_set_generator(line_segments_to_average):
    horizontal_coord = line_segments_to_average['horizontal_position']
    
    for seg in line_segments_to_average:
        yield {'horizontal_pos': horizontal_coord, 'line_seg': seg}

def number_average(iter, func):
    total = 0.0
    count = 0
    for item in iter:
        total += func(item)
        count += 1
        
    if count == 0:
        raise Exception("no input given to take average of")
    else:
        return total / count

def get_mean_vertical_coordinate_in_line_segments(line_segments, horizontal_coordinate):
    if line_segments == None or len(line_segments) == 0:
        raise Exception("tried to get the mean value of a non-existanct group of line segments")
    
    y_values = 0.0
    
    for seg in line_segments:
        yield None