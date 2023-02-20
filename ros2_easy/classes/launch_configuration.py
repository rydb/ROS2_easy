
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
    external_programs_to_run: Optional[typing.List[Cmd_Program]] = None
    """External programs to run that aren't ROS2 packages. E.G: Gazebo/Ignition"""

    def save_self_as_yaml(self):
        """save relevant information about this launch configuration into a yaml file"""
        with open("launch_conf_info.yaml", "w") as file:
            
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