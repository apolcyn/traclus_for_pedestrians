'''
Created on Jan 7, 2016

@author: Alex
'''
from planar.line import LineSegment
from planar import Point
from generator_initializer import GeneratorInitializer
from distance_functions import get_total_distance_function,\
    perpendicular_distance, angular_distance, parrallel_distance
import math
from partitioning.mutable_float import MutableFloat

def call_partition_trajectory(trajectory_point_list):
    if len(trajectory_point_list) < 2:
        raise ValueError("didn't provide a trajectory with enough points")
    
    cum_dist_getter_func = \
    cummulative_distance_function_getter_adapter(individual_distance_func=lambda x, y: \
                                                                             perpendicular_distance(x, y) + \
                                                                             angular_distance(x, y), \
                                                                             accumulator_func_getter=get_number_list_reducer_that_returns_each_midway_val)

    partition_from_index_getter = get_partition_from_index_creator(get_line_segment_from_points)
    
    partition_cost_computer_func = part_cost_computer_adapter(part_cost_func=partition_cost_computer, \
                                                              line_segment_iterable_getter=get_trajectory_line_segment_iterator, \
                                                              partition_line_getter=partition_from_index_getter, \
                                                              distance_func_computer_getter=cum_dist_getter_func, \
                                                              line_segment_creator=get_line_segment_from_points)
    no_par_cost_computer_func = no_part_cost_computer_adapter(no_part_cost_func=no_partition_cost_computer, \
                                                              line_segment_iterable_getter=get_trajectory_line_segment_iterator, \
                                                              line_segment_creator=get_line_segment_from_points)
    
    return partition_trajectory(trajectory_point_list=trajectory_point_list, \
                                partition_cost_func=partition_cost_computer_func, \
                                no_partition_cost_func=no_par_cost_computer_func, \
                                get_model_cost_computer_func=get_model_cost_computer, \
                                individual_line_seg_model_cost_computer=individual_line_seg_model_cost_computer)
    
def get_model_cost_computer(individual_line_segment_cost_computer):
    return get_number_list_reducer_that_returns_each_midway_val(func=individual_line_segment_cost_computer)

def cummulative_distance_function_getter_adapter(individual_distance_func, accumulator_func_getter):
    def _func():
        return cummulative_distance_function_getter(individual_distance_func=individual_distance_func, \
                                                    accumulator_func_getter=accumulator_func_getter)
    return _func
        
def cummulative_distance_function_getter(individual_distance_func, accumulator_func_getter):
    accumulator_func = accumulator_func_getter(lambda x: x)
    def _distance_func(line_a, line_b):
        return accumulator_func(individual_distance_func(line_a, line_b))
    return _distance_func
        
def get_number_list_reducer_that_returns_each_midway_val(func):
    total = MutableFloat(0.0)  
    def _func(num):
        total.increment(func(num))
        return total.get_val()
    return _func
    
def individual_line_seg_model_cost_computer(line_seg):
    if line_seg.length < 1.0:
        raise ValueError
    return math.ceil(math.log(line_seg.length, 2))

def get_partition_from_index_creator(line_segment_from_point_getter):
    def _func(list, low, high):
        if high >= len(list) or low >= high:
            raise Exception
        return line_segment_from_point_getter(list[low], list[high])
    return _func

def check_low_high_list_indices(trajectory_point_list, low_index, high_index):
    if high_index >= len(trajectory_point_list) or low_index >= high_index:
        raise IndexError

def part_cost_computer_adapter(part_cost_func, line_segment_iterable_getter, partition_line_getter, \
                               distance_func_computer_getter, line_segment_creator):
    def _func(trajectory_point_list, low_index, high_index, model_cost_computer):
        check_low_high_list_indices(trajectory_point_list=trajectory_point_list,\
                                     low_index=low_index, high_index=high_index)
        return part_cost_func(trajectory_point_list, low_index, high_index, \
                              line_segment_iterable_getter=line_segment_iterable_getter, \
                              partition_line_getter=partition_line_getter, \
                              model_cost_computer=model_cost_computer, \
                              distance_func_computer=distance_func_computer_getter(), \
                              line_segment_creator=line_segment_creator)
    return _func

def no_part_cost_computer_adapter(no_part_cost_func, line_segment_iterable_getter, line_segment_creator):
    def _func(trajectory_point_list, low_index, high_index, model_cost_computer):
        check_low_high_list_indices(trajectory_point_list=trajectory_point_list,\
                                     low_index=low_index, high_index=high_index)
        return no_part_cost_func(trajectory_point_list=trajectory_point_list, low_index=low_index, \
                                 high_index=high_index, line_segment_iterable_getter=line_segment_iterable_getter, \
                                 model_cost_computer=model_cost_computer, \
                                 line_segment_creator=line_segment_creator)
    return _func
    
def partition_trajectory(trajectory_point_list, partition_cost_func, no_partition_cost_func, \
                         get_model_cost_computer_func, individual_line_seg_model_cost_computer):
    low = 0
    high = 2
    partition_indices = []
    partition_indices.append(0)
    
    while high < len(trajectory_point_list):
        cost_par = partition_cost_func(trajectory_point_list, low, high, \
                                       get_model_cost_computer_func(individual_line_seg_model_cost_computer))
        cost_no_par = no_partition_cost_func(trajectory_point_list, low, \
                                             high, get_model_cost_computer_func(individual_line_seg_model_cost_computer))
        
        if cost_par > cost_no_par:
            partition_indices.append(high - 1)
            low = high - 1
        
        high += 1
    
    if partition_indices[-1] != len(trajectory_point_list) - 1:
        partition_indices.append(len(trajectory_point_list) - 1)
            
    return partition_indices

def partition_cost_computer(trajectory_point_list, low_index, high_index, line_segment_iterable_getter, \
                            partition_line_getter, model_cost_computer, distance_func_computer, \
                            line_segment_creator):
    if low_index >= high_index:
        raise IndexError("illegal indices to partition func")
    
    partition_line = partition_line_getter(trajectory_point_list, low_index, high_index)
    model_cost = model_cost_computer(partition_line)
    
    encoding_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, \
                                                     line_segment_creator):
        encoding_cost = distance_func_computer(line_segment, partition_line)
        
    if encoding_cost == None:
        raise Exception("undefined encoding cost, there were no line segments")
        
    return model_cost + encoding_cost

def no_partition_cost_computer(trajectory_point_list, low_index, high_index, \
                               line_segment_iterable_getter, model_cost_computer, \
                               line_segment_creator):
    if low_index >= high_index:
        raise IndexError("illegal indices to no partition func")
    
    total_cost = None
    for line_segment in line_segment_iterable_getter(trajectory_point_list, low_index, high_index, \
                                                     line_segment_creator):
        total_cost = model_cost_computer(line_segment)
        
    if total_cost == None:
        raise Exception("undefined total cost, there were no line segments")
    
    return total_cost

def get_line_segment_from_points(point_a, point_b):
    return LineSegment.from_points([point_a, point_b])

def get_trajectory_line_segment_iterator_adapter(iterator_getter, get_line_segment_from_points_func):
    def _func(list, low, high, get_line_segment_from_points_func=get_line_segment_from_points_func):
        iterator_getter(list, low, high, get_line_segment_from_points_func)
    return _func
        

def get_trajectory_line_segment_iterator(list, low, high, get_line_segment_from_points_func):
    if high <= low:
        raise Exception("high must be greater than low index")
            
    def line_segment_generator(func=get_line_segment_from_points_func):
        cur_pos = low
        
        while cur_pos < high:
            yield func(list[cur_pos], list[cur_pos + 1])
            cur_pos += 1
            
    return GeneratorInitializer(line_segment_generator)