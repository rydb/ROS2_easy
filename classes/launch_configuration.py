
import typing
import yaml
from dataclasses import dataclass
from typing import Optional
import os


from .Package import Package
from .Cmd_Program import Cmd_Program
from .Config import Config
from .logger import *


MODEL_FORMAT = ".FCStd"
URDF_FILE_EXTENSION = ".xml"
"""urdf file extensions have been finicky when testing, so setting expected urdf extension to .xml since thats what has worked for me"""

@dataclass
class launch_configuration():
    """
    object that holds all of the parameters for a specific type of a ros2 enviorment. E.G: configuration for running a simulation enviorment/real enviorment.
    """
    config_store_pkg: Package
    """
    package which stores all configs.
    
    This includes things like launch files, rviz configs, etc..

    for sanity sake the only option will be to store all configs in 1 package.
    """
    launch_file: str
    """The full name of the launch file for this launch configuration. Include the .py extension. E.G:
        
        `launch.py`
    """
    urdf_file_name: str
    """urdf file without the extension at the end"""

    packages_to_run: typing.List[Package]
    """All packages to be ran by this launch configuration"""
    extra_pkgs_to_build: Optional[typing.List[Package]] = None
    """The packages to be built by colcon in addition to config storing pkg"""
    external_programs_to_run: Optional[typing.List["function"]] = None
    """
    External programs to run that aren't ROS2 packages. E.G: Gazebo/Ignition
    
    in order to add a program to this, define a function which uses launch configuration, and pass that function object to to this as part of a list.
    E.G:

    def gazebo(launch_conf):
        ..... launch gazebo.....

    external_programs_to_run = [gazebo]
    """
    gazebo_world_name: Optional[str] = None
    """optional name of gazebo world in /worlds folder for config package. If this is not set, this will defualt to the urdf name."""



    def save_self_as_yaml(self, dir_path=""):
        """save relevant information about this launch configuration into a yaml file"""
        with open(dir_path + "launch_conf_info.yaml", "w") as file:
            
            #dump relevant information thats package specific
            yaml.dump(self.config_store_pkg.path_dict, file)

            #dump relevant information thats relevant to this specific launch configuration
            relevant_info_on_self = {
                "URDF_NAME": self.urdf_file_name,
                "PROJECT_DIR": os.getcwd() + "/",
                "LOGS_DIR": log_path_folder,

            }
            yaml.dump(relevant_info_on_self, file)
        #yaml.dump(self.__dict__, default_flow_style=False))
        #pass
        
    @property
    def model_file_path(self):
        """returns path to model file used by this launch configuration. `!!!Assuming there is one, and the file is named after the urdf as it should be if made by the urdf converter!!!`"""

        return self.config_store_pkg.path_dict["MODELS"] + self.urdf_file_name + MODEL_FORMAT
    
    @property
    def urdf_path(self):
        """return absolute path to urdf file loaded by this launch configuration"""
        return self.config_store_pkg.path_dict["URDFS"] + self.urdf_file_name + URDF_FILE_EXTENSION
    
    @property
    def gazebo_world_path(self):
        """return the absolute path to the world file for this launch_configuration"""
        if(self.gazebo_world_name == None):
            return self.config_store_pkg.path_dict["WORLDS"] + self.urdf_file_name + ".sdf"
        else:
            return self.config_store_pkg.path_dict["WORLDS"] + self.gazebo_world_name + ".sdf"