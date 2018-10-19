from __future__ import print_function, absolute_import, division
import subprocess
import time

from sim.sim_modules import vrep

class Core(object):

    def __init__(self, vrep_path, scene, visualization=True, autolaunch=True, api_port = 19998, dt = 50):
        self.vrep_path=vrep_path
        self.visualization=visualization
        self.autolaunch=autolaunch
        self.port=api_port
        self.clientID=None
        self.scene=scene
        self.dt=dt

    def vrep_launch(self):
        if self.autolaunch:
            if self.visualization:
                vrep_exec=self.vrep_path+'/vrep.sh '
                t_val = 5.0
            else:
                vrep_exec=self.vrep_path+'/vrep.sh -h '
                t_val = 1.0
            synch_mode_cmd= \
                '-gREMOTEAPISERVERSERVICE_'+str(self.port)+'_FALSE_TRUE '
            subprocess.call( \
                vrep_exec+synch_mode_cmd+self.scene+' &',shell=True)
            time.sleep(t_val)      
        self.clientID=vrep.simxStart(
            '127.0.0.1',self.port,True,True,5000,5)
    
    def vrep_start(self):
        vrep.simxStartSimulation(
            self.clientID,vrep.simx_opmode_blocking)
        vrep.simxSynchronous(self.clientID, True)
    
    def vrep_reset(self):
        vrep.simxStopSimulation(
            self.clientID,vrep.simx_opmode_blocking)
        time.sleep(0.1)
    
    def pause(self):
        vrep.simxPauseSimulation(
            self.clientID,vrep.simx_opmode_blocking)
    
    def close(self):
        self.vrep_reset()
        while vrep.simxGetConnectionId(self.clientID) != -1:
            vrep.simxSynchronousTrigger(self.clientID)
        vrep.simxFinish(self.clientID)

if __name__ == '__main__':
    env = Core(None, None)