'''
Created on Jan 20, 2016

@author: Alex
'''

from coordination import the_whole_enchilada
from deer_file_reader import read_test_file
import os

if __name__ == '__main__':
    print "hello"
    file = os.path.dirname(__file__) + "\\deer_1995test.tra"
    points = read_test_file(file)
    traj_res = the_whole_enchilada(point_iterable_list=points, epsilon=0, min_neighbors=0, \
                                   min_num_trajectories_in_cluster=1, min_vertical_lines=1, min_prev_dist=0.0)
    print "heres the output: " + str(traj_res)
    print "about to print out the lines"
    for traj in traj_res:
        print "A new average trajectory:"
        for point in traj:
            print "    x: " + str(point.x) + ", y: " + str(point.y)
    print "done"
                