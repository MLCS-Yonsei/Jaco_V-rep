from __future__ import absolute_import, print_function, division
import os,sys,time

from sim.jaco import Jaco_arm


def main(max_episode, max_step):
    
    sim=Jaco_arm('/opt/vrep') # Your V-rep path here

    sim.launch()

    for episode in range(max_episode):
        sim.reset()
        print('Episode:',episode+1)
        sim.start()
        for step in range(max_step):
            joint_target = [0.0]*6 # joint target angle here (radian)
            joint_angle=sim.step(joint_target)

    sim.close()

if __name__=='__main__':
    main(10, 10)