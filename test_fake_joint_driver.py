#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import actionlib # imported actionlib
from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal)
from trajectory_msgs.msg import (
    JointTrajectory,
    JointTrajectoryPoint)
import rospy # imported rospy
import rostest # imoprted rostest
from sensor_msgs.msg import JointState # imported Jointstate
from trajectory_msgs.msg import JointTrajectory # imported JoinTrajectory
import unittest# imported unittest

# class TestFakeJoinDriver
class TestFakeJointDriver(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        rospy.init_node('test_fake_joint_driver_node')

    def setUp(self):
        rospy.Subscriber('joint_states',
                         JointState, self.cb_joint_states, queue_size=10)
        self.joint_states = rospy.wait_for_message(
            'joint_states', JointState, timeout=10.0)
        
        self.pub = rospy.Publisher(
            'joint_trajectory_controller/command',
            JointTrajectory,
            queue_size=10)
        
        self.client = actionlib.SimpleActionClient(
            'joint_trajectory_controller/follow_joint_trajectory',
            FollowJointTrajectoryAction)

        self.client.wait_for_server(timeout=rospy.Duration(10.0))

# created funciton for join states

    def cb_joint_states(self, msg):
        self.joint_states = msg

# created funciton for joint trajectory command        
    def test_joint_trajectory_command(self):
        traj = JointTrajectory()
        traj.header.stamp = rospy.Time(0)
        traj.joint_names = ['JOINT1', 'JOINT2', 'JOINT3']
        for i in range(11):
            point = JointTrajectoryPoint()
            point.positions = [0.1*i, 0.2*i, 0.3*i]
            point.time_from_start = rospy.Duration(i*0.1)
            traj.points.append(point)

        self.pub.publish(traj)
        rospy.sleep(1.1)
        self.assertAlmostEqual(self.joint_states.position[0], 1.0)
        self.assertAlmostEqual(self.joint_states.position[1], 2.0)
        self.assertAlmostEqual(self.joint_states.position[2], 3.0)

# created funciton for joint trajectory action
    def test_joint_trajectory_action(self):
        goal = FollowJointTrajectoryGoal()
        traj = goal.trajectory
        traj.header.stamp = rospy.Time(0)
        traj.joint_names = ['JOINT1', 'JOINT2', 'JOINT3']
        for i in range(11):
            point = JointTrajectoryPoint()
            point.positions = [0.1*i, 0.2*i, 0.3*i]
            point.time_from_start = rospy.Duration(i*0.1)
            traj.points.append(point)

        self.client.send_goal_and_wait(goal)
        rospy.sleep(0.1)

        self.assertAlmostEqual(self.joint_states.position[0], 1.0)
        self.assertAlmostEqual(self.joint_states.position[1], 2.0)
        self.assertAlmostEqual(self.joint_states.position[2], 3.0)
        
# calling the main function       
if __name__ == '__main__':
    rostest.rosrun('fake_joint_driver',
                   'test_fake_joint_driver',
                   TestFakeJointDriver)
