from __future__ import print_function, absolute_import, division
import os, sys, time
from sim.sim_modules import vrep
from sim.sim_modules.core import Core


scene_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'scenes')


class Jaco_arm(Core):

    def __init__(self, vrep_path):
        Core.__init__(
            self,
            vrep_path,
            os.path.join(scene_dir,'jaco.ttt'))
        self.std = ' step:%04d | joint_angle:' + ' % 2.1f' * 6 + '\n'
    
    def launch(self):
        self.vrep_launch()
        vrep.simxSynchronousTrigger(self.clientID)
        self.joint_handles=[ \
            vrep.simxGetObjectHandle( \
                self.clientID,'Jaco_joint'+str(idx),vrep.simx_opmode_blocking)[1] \
                for idx in range(1,7)]
        self.count=0
    
    def reset(self):
        self.vrep_reset()
        self.count=0
        time.sleep(0.2)
    
    def start(self):
        self.vrep_start()
        self.controller([0.0]*6)
        vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxGetPingTime(self.clientID)
    
    def step(self, joint_target):
        self.count += 1
        self.controller(joint_target)
        vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxGetPingTime(self.clientID)
        joint_angle=[ \
            vrep.simxGetJointPosition( \
                self.clientID,self.joint_handles[idx],vrep.simx_opmode_blocking)[1] \
                for idx in range(6)]
        sys.stderr.write(self.std%tuple([self.count]+joint_angle))
        return joint_angle
    
    def controller(self, joint_target):
        for idx,target in enumerate(joint_target):
            vrep.simxSetJointTargetPosition(
                self.clientID,self.joint_handles[idx],target,vrep.simx_opmode_streaming)