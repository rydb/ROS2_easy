from dataclasses import dataclass
import typing
from typing import Optional
import os
import numpy as np
import yaml

#!!!RELATIVE IMPORTS MUST HAVE A DOT OR THEY THROW AN ERROR WHEN THE FILE IMPORTING THE IMPORTING FILE TRYS THE IMPORT THE IMPORTING FILE!!!
from .Config import Config
PROJECT_PATH = os.getcwd() + "/"


class Package():
    """A ros2 package and its relevant information."""
    global local_directory_for
    local_directory_for = {
        "URDFS": "urdf/", 
        "MODELS": "models/",
        "RVIZ": "rviz/",
        "PACKAGES": "src/",
    }
    """people store files like models, urdfs, etc.. in different ways, refer to this schema for file paths on where to find file types"""
    
    def __init__(self, name:str, executable_name:str, config:str = None, urdf_name:str = None, output:str= "screen", build:bool= False, optional_launch_file_node_args = None, entry_point:str = None):
        #self.parent_pkg: "Package" = parent_pkg
        #"""ROS2 package that is parent of this package."""
        self.name: str = name
        """name of this package"""
        self.executable_name: str = executable_name
        """
        name of executable used by package. In a ros2 package, this is generally the name of the file executing code,
            E.G:
            in model_pkg:
                `model_pkg -> src -> model_pkg -> model.py`
                is package executable, so

                `model` is executable_name
        """
        self.config: Optional[Config] = config
        """config info about this package if relevant"""

        #self.urdf_path: str = self.urdf_folder + self.urdf_name

        self.output: Optional[str] = output
        """output for package, used in launch file"""

        self.build: Optional[bool] = build
        """weather colcon builds this package. is set to no by default"""
        self.entry_point: Optional[str] = entry_point
        """entry point for this package(assuming this package is executable), used for initializing setup.py"""

        self.optional_launch_file_node_args: Optional[typing.Dict[str, str]] = optional_launch_file_node_args


    """optional arguements to be a part of the launch file node list. Set this for packages with custom node arguements like rviz2."""
    def as_node_conf_dict(self):

        """launch files represent ros2 packages as dicitionaries. return this package as a dict for that"""
        result =  {
            "package": "'%s'" % self.name,
            "executable": "'%s'" % self.executable_name,
            "output": "'%s'" % self.output,
            "parameters": "[]"

        }
        if(self.optional_launch_file_node_args != None):
            result.update(self.optional_launch_file_node_args)
        return 

    def __repr__(self):
        return str(self.__dict__)

    """optional arguements to be a part of the launch file node list. Set this for packages with custom node arguements like rviz2."""
    def as_node_conf_dict(self):

        """launch files represent ros2 packages as dicitionaries. return this package as a dict for that"""
        result =  {
            "package": "'%s'" % self.name,
            "executable": "'%s'" % self.executable_name,
            "output": "'%s'" % self.output,
            "parameters": "[]"

        }
        if(self.optional_launch_file_node_args != None):
            result.update(self.optional_launch_file_node_args)
        return result

    @property
    def path(self):
        """returns path to this package... assuming this is a package that is built"""
        if(self.build == True):
            return PROJECT_PATH + local_directory_for["PACKAGES"] + self.name + "/"
        else:
            raise "this property is intended for built packages, mabye different behaviour can be added here for things like Rviz2, for example."
    
    @property
    def path_dict(self):
        return {
        "URDFS": self.path + local_directory_for["URDFS"], 
        "MODELS": self.path + local_directory_for["MODELS"],
        "RVIZ": self.path + local_directory_for["RVIZ"],
    }
    """paths to various config files (urdfs, models, etc..)"""
    
        #print(yaml.dump(self.__dict__, default_flow_style=False))

#model_pkg = Package(None, "model_pkg", "model", build=True, urdf_name="diff_bot.urdf.xml")

