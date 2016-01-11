'''
Created on Jan 10, 2016

@author: Alex
'''
from generator_initializer import GeneratorInitializer

def get_trajectory_line_segments_from_points_iterable(point_iterable, trajectory_line_segment_factory, trajectory_id, \
                                                      trajectory_partitioning_func, line_seg_from_points_func):
    good_point_iterable = filter_by_indices(good_indices=trajectory_partitioning_func(trajectory_point_list=point_iterable), \
                             vals=point_iterable)
    line_segs = consecutive_item_func_iterator_getter(consecutive_item_func=line_seg_from_points_func, \
                                                      item_iterable=good_point_iterable)
    def _create_traj_line_seg(line_seg):
        return trajectory_line_segment_factory.new_trajectory_line_seg(line_seg, trajectory_id=trajectory_id)
    
    return map(_create_traj_line_seg, line_segs)

def filter_by_indices(good_indices, vals):
    return GeneratorInitializer(_filter_by_indices, good_indices, vals)

def _filter_by_indices(good_indices, vals):
    vals_iter = iter(vals)
    good_indices_iter = iter(good_indices)
    
    num_vals = 0
    for i in good_indices_iter:
        if i != 0:
            raise ValueError("the first index should be 0, but it was " + str(i))
        else:
            for item in vals_iter:
                yield item
                break
            num_vals = 1
            break
            
    max_good_index = 0
    vals_cur_index = 1
    for i in good_indices_iter:
        max_good_index = i
        for item in vals_iter:
            num_vals += 1
            if vals_cur_index == i:
                vals_cur_index += 1
                yield item
                break
            else:
                vals_cur_index += 1
                
    for i in vals_iter:
        num_vals += 1
                
    if num_vals < 2:
        raise ValueError("list passed in is too short")
    if max_good_index != num_vals - 1:
        raise ValueError("last index is " + str(max_good_index) + \
                         " but there were " + str(num_vals) + " vals")
        
def consecutive_item_func_iterator_getter(consecutive_item_func, item_iterable):
    def _func():
        iterator = iter(item_iterable)
        last_item = None
        num_items = 0
        for item in iterator:
            num_items = 1
            last_item = item
            break
        if num_items == 0:
            raise ValueError("iterator doesn't have any values")
        
        for item in iterator:
            num_items += 1
            yield consecutive_item_func(last_item, item)
            last_item = item
            
        if num_items < 2:
            raise ValueError("iterator didn't have at least two items")
        
    return GeneratorInitializer(_func)
            