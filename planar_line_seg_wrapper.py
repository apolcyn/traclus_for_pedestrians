'''
Created on Jan 21, 2016

@author: Alex
'''
from planar import LineSegment

class LineSegmentWrapper():
    def __init__(self, line_segment):
        self.wrapped_line_seg = line_segment
        self.wrapped_inf_line = line_segment.line
        self.wrapped_direction = self.wrapped_line.direction
        self.wrapped_end = line_segment.end
        self.wrapped_start = line_segment.start
        
        
        