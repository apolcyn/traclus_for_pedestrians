'''
Created on Jan 7, 2016

@author: Alex
'''
from planar.line import LineSegment
from planar import Point
from string import lower
from generator_initializer import GeneratorInitializer
from distance_functions import get_total_distance_function,\
    perpendicular_distance, angular_distance, parrallel_distance
import math
from partitioning.mutable_float import MutableFloat

def get_par_cost_computer():
    return partition_cost_computer

def get_no_par_cost_computer():
    return no_partition_cost_computer

def call_partition_trajectory(trajectory_point_list, partition_trajectory_func, par_cost_func=get_par_cost_computer(), \
                              no_par_cost_func=get_no_par_cost_computer()):
    line_seg_iterable_getter = get_trajectory_line_segment_iterator(0, len(trajectory_point_list), \
                                                                    get_line_segment_from_points)
    
    model_cost_computer = get_number_list_reducer_that_returns_each_midway_val(individial_line_seg_model_cost_computer)
    distance_function = get_total_distance_function(perpendicular_distance, angular_distance, parrallel_distance)
    partition_from_index_getter = get_partition_from_index_creator(get_line_segment_from_points)
    
    partition_cost_computer_func = part_cost_computer_adapter(part_cost_func=partition_cost_computer, \
                                                              trajectory_point_list=trajectory_point_list, \
                                                              line_segment_iterable_getter=line_seg_iterable_getter, \
                                                              partition_line_getter=partition_from_index_getter, \
                                                              model_cost_computer=model_cost_computer, \
                                                              distance_func_computer=distance_function)
    no_par_cost_computer_func = no_part_cost_computer_adapter(no_part_cost_func=no_partition_cost_computer, \
                                                              trajectory_point_list=trajectory_point_list, \
                                                              line_segment_iterable_getter=line_seg_iterable_getter, \
                                                              model_cost_computer=model_cost_computer)
    
    return partition_trajectory_func(trajectory_point_list, partition_cost_computer_func, no_par_cost_computer_func)
    
def get_number_list_reducer_that_returns_each_midway_val(func):
    total = MutableFloat(0.0)  
    def __func(num):
        total.increment(func(num))
        return total.get_val()
    
def individial_line_seg_model_cost_computer(line_seg):
    return math.ceil(math.log(line_seg.distance(), 2))

def get_partition_from_index_creator(line_segment_from_point_getter):
    def __func(list, low, high):
        return line_segment_from_point_getter(list[low], list[high])
    return __func

def part_cost_computer_adapter(part_cost_func, trajectory_point_list, \
                               line_segment_iterable_getter, partition_line_getter, \
                               model_cost_computer, distance_func_computer):
    def __func(trajectory_point_list, low, high, line_segment_iterable_getter=line_segment_iterable_getter, \
               partition_line_getter=partition_line_getter, model_cost_computer=model_cost_computer, \
               distance_func_computer=distance_func_computer):
        return partition_cost_computer(trajectory_point_list, low)
    return __func

def no_part_cost_computer_adapter(no_part_cost_func, trajectory_point_list, \
                               line_segment_iterable_getter, model_cost_computer):
    def __func(trajectory_point_list, low_index, high_index, \
               line_segment_iterable_getter=line_segment_iterable_getter, model_cost_computer=model_cost_computer):
        return no_part_cost_func(trajectory_point_list=trajectory_point_list, low_index=low_index, \
                                 high_index=high_index, line_segment_iterable_getter=line_segment_iterable_getter, \
                                 high_index=high_index)
    return __func
    
def partition_trajectory(trajectory_point_list, partition_cost_func, no_partition_cost_func):
    low = 0
    high = 2
    partition_indices = []
    partition_indices.append(0)
    
    while high < len(trajectory_point_list):
        cost_par = partition_cost_func(trajectory_point_list, low, high)
        cost_no_par = no_partition_cost_func(trajectory_point_list, low, high)
        
        if cost_par > cost_no_par:
            partition_indices.append(high - 1)
            low = high - 1
        
        high += 1
    
    if partition_indices[-1] != len(trajectory_point_list) - 1:
        partition_indices.append(len(trajectory_point_list) - 1)
            
    return partition_indices

def partition_cost_computer(trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_func_computer):
    if low_index >= high_index:
        raise IndexError("illegal indices to partition func")
    
    partition_line = partition_line_getter(trajectory_point_list, low_index, high_index)
    model_cost = model_cost_computer(partition_line)
    
    encoding_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        encoding_cost = distance_func_computer(line_segment, partition_line)
        
    if encoding_cost == None:
        raise Exception("undefined encoding cost, there were no line segments")
        
    return model_cost + encoding_cost

def no_partition_cost_computer(trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer):
    if low_index >= high_index:
        raise IndexError("illegal indices to no partition func")
    
    total_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, None):
        total_cost = model_cost_computer(line_segment)
        
    if total_cost == None:
        raise Exception("undefined total cost, there were no line segments")
    
    return total_cost

def get_line_segment_from_points(point_a, point_b):
    return LineSegment.from_points([point_a, point_b])

def get_trajectory_line_segment_iterator(list, low, high, get_line_segment_from_points_func):
    if high <= low:
        raise Exception("high must be greater than low index")
            
    def line_segment_generator(func=get_line_segment_from_points_func):
        cur_pos = low
        
        while cur_pos < high:
            yield func(list[cur_pos], list[cur_pos + 1])
            cur_pos += 1
            
    return GeneratorInitializer(line_segment_generator)