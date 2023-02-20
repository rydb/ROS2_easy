"""
all of the 'common', packages/programs that any given launch configuration will likely use
E.G:
    Rviz, gazebo, robot state publisher, etc...

throw anything that is likely to get called regarldess of the project
"""

from .launch_configuration import launch_configuration
from .Cmd_Program import Cmd_Program
from .Package import Package
from .Config import Config

gazebo = Cmd_Program("gazebo.gz gazebo")
"""use:
    `sudo snap install --beta gazebo`
    to install gazebo"""

rqt_pkg = Package("rqt_gui", "rqt_gui")
"""package which displays gui which can be used to display all running nodes"""

robot_state_publisher_pkg = Package("robot_state_publisher", "robot_state_publisher", optional_launch_file_node_args= {"parameters": "[{'use_sim_time': True, 'robot_description': robot_desc}]"})
"""package which reads from urdf file and publishes relevant information about it. Usually read by Rviz or sometimes Gazebo"""