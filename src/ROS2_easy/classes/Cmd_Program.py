from dataclasses import dataclass
from typing import Optional


@dataclass
class Cmd_Program():
    """A program to be launched with ROS2 that isn't a package via cmd(E.G: Gazebo, or non-ros package, things)"""

    command: str
    """
    command to execute for cmd like utility
    
    split parameters with spaces. E.G:

    `gazebo --verbose -s example_world.so`
    """

    output: Optional[str] = "screen"
    """output for command line utility"""
    def as_process_conf_dict(self):

        """launch files represent ros2 packages as dicitionaries. return this package as a dict for that"""
        result =  {
            "command": "%s" % self.command.split(" "),
            "output": "'%s'" % self.output,

        }
        return result
        