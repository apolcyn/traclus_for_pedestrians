'''
Created on Jan 10, 2016

@author: Alex
'''
from generator_initializer import GeneratorInitializer

def filter_by_indices(good_indices, vals):
    return GeneratorInitializer(_filter_by_indices, good_indices, vals)

def _filter_by_indices(good_indices, vals):
    vals_iter = iter(vals)
    good_indices_iter = iter(good_indices)
    
    num_vals = 0
    for i in good_indices_iter:
        if i != 0:
            raise IndexError("the first index should be 0, but it was " + str(i))
        else:
            for item in vals_iter:
                yield item
                break
            num_vals = 1
            break
    if num_vals == 0:
        raise IndexError("can't pass in empty lists")
            
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
                
    if max_good_index != num_vals - 1:
        raise IndexError("last index is " + str(max_good_index) + \
                         " but there were " + str(num_vals) + " vals")

