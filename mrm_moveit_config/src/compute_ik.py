#!/usr/bin/env python 

from math import *
import cmath
from geometry_msgs.msg import Pose, Quaternion

class ComputeIk(): 

    def __init__(self): 

        # DH parameters
        self.a_2 = 0.246
        self.d_4 = -0.242

    def Compute_ik(self, p): 

        # Initizaliztion 
        p_x = p.position.x
        p_y = p.position.y
        p_z = p.position.z
        a_2 = self.a_2
        d_4 = self.d_4

        # theta1 
        theta1 = atan2 (p_x, p_y)

        # theta3
        K = (p_x**2 + p_y**2 + p_z**2 - a_2**2 - d_4**2) / 2*a_2
        theta3 = -atan2(K, sqrt(d_4**2 - K**2))

        # theta2
        c1 = cos(theta1)
        c3 = cos(theta3)
        s1 = sin(theta1)
        s3 = sin(theta3)

        theta23 = atan2((-a_2*c3*p_z - (c1*p_x + s1*p_y)*(d_4 - a_2*s3)), (a_2*s3 - d_4)*p_z - a_2*c3*(c1*p_x + s1*p_y))
        theta2 = theta23 - theta3

        # theta4
        r13 = 0
        r23 = 0
        r33 = -1

        c23 = ((a_2*s3 - d_4)*p_z - a_2*c3*(c1*p_x + s1*p_y)) / (p_z**2 + (c1*p_x + s1*p_y)**2)
        s23 = (-a_2*c3*p_z + (c1*p_x + s1*p_y) * (a_2*s3 - d_4)) / (p_z**2 + (c1*p_x + s1*p_y)**2)

        theta4 = atan2(-r13*s1 + r23*c1, -r13*c1*c23 - r23*s1*c23 + r33*s23)
        
        # theta5 
        c4 = cos(theta4)
        s4 = sin(theta4)

        s5 = r13*(c1*c23*c4 + s1*s4) + r23*(s1*c23*c4 - c1*s4) - r33*s23*c4
        c5 = -r13*c1*s23 - r23*s1*s23 - r33*c23

        theta5 = atan2(-s5, c5)

        # theta6 
        c5 = cos(theta5)
        s5 = sin(theta5)
        r11 = 1
        r21 = 0 
        r31 = 0

        s6 = -r11*(c1*c23*s4 - s1*c4) - r21*(s1*c23*s4 + c1*c4) + r31*s23*s4
        c6 = r11*((c1*c23*c4 + s1*s4)*c5 - c1*s23*s5) + r21*((s1*c23*c4 - c1*s4)*c5 - s1*s23*s5) - r31*(s23*s4)

        theta6 = atan2(s6, c6) 


        return [theta1, theta2, theta3, theta4, theta5, theta6]

if __name__ == '__main__': 

    ik = ComputeIk()
    pose = Pose()
    pose.position.x = 0
    pose.position.y = 0
    pose.position.z = 0.611
    thetas = ik.Compute_ik(pose)

    for i in range(6): 
        print (thetas[i])



