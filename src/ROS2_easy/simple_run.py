"""
A collection of functions which makes running ROS2 tasks easier:

See the example folder(FOLDER PENDING) to see how to use this.
"""

import os
import subprocess
import glob
import json
from dataclasses import dataclass
from typing import Optional
from inspect import getsourcefile
from os.path import abspath

from .classes.logger import return_logger
from .classes.launch_configuration import launch_configuration


split_str = "/"
log_path =  "simple_run_logs/simple_run.log"
"""path of log file for simple_run"""
log_path_folder = "".join([x + split_str for x in log_path.split(split_str)[0:-1]]) # get folder path from file path

current_py_file:str = abspath(getsourcefile(lambda:0))
"""returns path of this python file, no clue what lambda:0 is though"""
current_py_folder = "".join([x + split_str for x in current_py_file.split(split_str)[0:-1]]) # get folder path from file path

urdf_converter_macro_path = "export_model_to_urdf.py"

logger = return_logger(log_path, logger_write_mode="w")
"""logger for simple_run"""

urdf_file_extension = ".xml"
"""file extension to represent urdf files. """

def replace_setup_py(launch_conf: launch_configuration,
 install_requires="setuptools",
 zip_safe="True",
 maintainer="placeholder",
 maintainer_email="placeholder@gmail.com",
 description="TODO: Package description",
 license="TODO: License declaration",
 tests_require="pytest",


   ):
    """
    adds EVERY folder in each package_to_build to their /share directorys for each setup.py

    ROS2 requires everything it uses to be in the /share directory, so for the sake of saving headaches, pre-emptively add EVERYTHING to it. 

    BUG: multi-nested folders do not currently work, I will want to fix that
    """
    logger.debug("replacing setup.py with auto-generated one based on existing files in launch_conf config package")
    tab = "    "

    directory_of_file = "src/%s/" % launch_conf.config_store_pkg.name
    file_to_edit = "setup.py"
    print(".%s*/" % directory_of_file)
    setup_py = directory_of_file + file_to_edit
    print("re-writting ||%s|| to include all folders inside them inside their /install/<pkg_name>/share directory" % launch_conf.config_store_pkg.name)

    f = open(setup_py, "w")
    sample_f_list = []

    sample_f_list.append(['WRITE', 0, "from setuptools import setup"])
    sample_f_list.append(['WRITE', 0, "import os"])
    sample_f_list.append(['WRITE', 0, "import glob"])
    sample_f_list.append(['WRITE', 0, " "])
    sample_f_list.append(['WRITE', 0, "#NOTE: MAKE SURE YOUR LAUNCH FILE IS INSIDE <pkg_name>/launch"])
    sample_f_list.append(['WRITE', 0, " "])
    sample_f_list.append(['WRITE', 0, "#GLOB STARTS FROM THE PACKAGE DIRECTORY WHEN USING setup.py"])
    sample_f_list.append(['WRITE', 0, " "])
    sample_f_list.append(['WRITE', 0, "package_name = '%s'" % launch_conf.config_store_pkg.name])
    sample_f_list.append(['WRITE', 0, " "])
    sample_f_list.append(['WRITE', 0, "setup("])
    \
        sample_f_list.append(['WRITE', 1, "name=package_name,"])
    \
        sample_f_list.append(['WRITE', 1, "version='0.0.0',"])
    \
        sample_f_list.append(['WRITE', 1, "packages=[package_name],"])
    \
        sample_f_list.append(['WRITE', 1, "data_files=["])
    \
            sample_f_list.append(['WRITE', 2, "('share/ament_index/resource_index/packages',"])
    \
                sample_f_list.append(['WRITE', 3, "['resource/' + package_name]),"])
    \
            sample_f_list.append(['WRITE', 2, "('share/' + package_name, ['package.xml']),"])
    \
                    for folder in [dire[dire.__len__() - 2]for dire in [dire.split("/") for dire in glob.glob("./src/model_pkg/*/", recursive = True)]]:
                        #append every folder in package into /share so files don't get loaded because you forget xyz
                        #print("writting %s" %folder)
                        sample_f_list.append(["WRITE", 4, "(os.path.join('share', package_name, '%s'), glob.glob('%s/*'))," % (folder, folder) ])
    \
        sample_f_list.append(['WRITE', 1, "],"])
    \
        sample_f_list.append(['WRITE', 1, "install_requires=['%s']," % install_requires])
    \
        sample_f_list.append(['WRITE', 1, "zip_safe=%s," % zip_safe])
    \
        sample_f_list.append(['WRITE', 1, "maintainer='%s'," % maintainer])
    \
        sample_f_list.append(['WRITE', 1, "maintainer_email='%s'," % maintainer_email])
    \
        sample_f_list.append(['WRITE', 1, "description='%s'," % description])
    \
        sample_f_list.append(['WRITE', 1, "license='%s'," % license])
    \
        sample_f_list.append(['WRITE', 1, "tests_require=['%s']," % tests_require])
    \
        sample_f_list.append(['WRITE', 1, "entry_points={"])
    \
            sample_f_list.append(['WRITE', 2, "'console_scripts': ["])
    \
                if(launch_conf.config_store_pkg.entry_point != None):
                    sample_f_list.append(['WRITE', 3, "'%s = model_pkg.%s:%s'" % (launch_conf.config_store_pkg.executable_name, launch_conf.config_store_pkg.executable_name, launch_conf.config_store_pkg.entry_point)])
    \
                else:
                    raise "NO ENTRY POINT FOR setup.py TO USE. SET ONE FOR THE CONFIG PACKAGE(package that stores all config files). THROWING ERROR TO STOP UNDEFINED BEHAVIOUR."
    \
            sample_f_list.append(['WRITE', 2, "],"])
    \
        sample_f_list.append(['WRITE', 1, "},"])
    \
    sample_f_list.append(['WRITE', 0, ")"])

    print(setup_py)
    f = open(setup_py, 'r')
    f_lines = f.readlines()
    f.close()
    f = open(setup_py, 'w')
    tab = "    "
    for i in range(0, sample_f_list.__len__()):
        l =  sample_f_list[i]
        if(l[0] == 'IGNORE'):
            f.write(f_lines[i])
        elif(l[0] == 'WRITE'):
            f.write((tab * l[1]) + l[2] + "\n")
        else:
            print('WARNING: Expected IGNORE or WRITE, got ' + l[0] + 'treating as IGNORE')
            f.write(f_lines[i])

    logger.debug("finished replacing setup.py with generated one.")

def generate_launch_py(launch_conf: launch_configuration, ):
    """
    generate a launch file based on launch_conf

    collects:
        1: all packages that are being built, 
        2: launch file directory, 
        3: misc launch variables that are in launch_configuration

    and then creates a launch.py file based off of those parameters for other functions in simple_run to launch.
    """
    logger.debug("generating new launch script based on launch configuration")

    #fetch share directory command, since this needs to be executed as a part of the launch file, append the command to be executed inside the launch file
    package_name_var_name = "package_name"
    share_directory_command = "ament_index_python.packages.get_package_share_directory(%s)" % package_name_var_name

    screen = "'screen'"
    ###
    # Packages/commands that go into launch file
    ###
    launch_commands = []

    """
    if gazebo fails to load, run the following commands(if on ubuntu) to install missing packages
    https://classic.gazebosim.org/tutorials?tut=ros2_installing

    sudo apt install ros-foxy-ros-core ros-foxy-geometry2
    sudo snap install gazebo

    launch setup based on:
    https://answers.ros.org/question/374976/ros2-launch-gazebolaunchpy-from-my-own-launch-file/
    """

    #get every line ready and constructed to be written into the new launch file
    launch_l_list = []


    #print(launch_conf.packages_to_run)

    f = open("./src/%s/launch/%s" % (launch_conf.config_store_pkg.name, launch_conf.launch_file), "w")
    launch_l_list = []

    launch_l_list.append([0, "from launch import LaunchDescription"])
    launch_l_list.append([0, "from launch_ros.actions import Node"])
    launch_l_list.append([0, "from launch.actions import ExecuteProcess"])
    launch_l_list.append([0, "import ament_index_python\n"])

    launch_l_list.append([0, "package_name = 'model_pkg'"])
    launch_l_list.append([0, "share_directory = ament_index_python.packages.get_package_share_directory(%s)\n" % package_name_var_name])
    launch_l_list.append([0, "urdf = share_directory + '/urdf/%s'" % (launch_conf.urdf_file_name + urdf_file_extension)])

    launch_l_list.append([ 0, "def generate_launch_description():"])
    \
        launch_l_list.append([1, "with open(urdf, 'r') as infp:"])
    \
            launch_l_list.append([2, "robot_desc = infp.read()\n\n"])
    \
        launch_l_list.append([ 1, "return LaunchDescription(["])
    \
        if(launch_conf.external_programs_to_run != None):
            for external_prog in launch_conf.external_programs_to_run:
                launch_l_list.append([2, "ExecuteProcess("])

                program_args = external_prog.as_process_conf_dict()
                for param in program_args:
                    launch_l_list.append([3, "%s=%s," % (param, program_args[param])])
                launch_l_list.append([2, "),"])
    \
        for pkg in launch_conf.packages_to_run:

            launch_l_list.append([2, "Node("])

            node_args = pkg.as_node_conf_dict()
            for param in node_args:
                launch_l_list.append([3, "%s=%s," % (param, node_args[param])])
            launch_l_list.append([ 2, "),"])
    \
        launch_l_list.append([ 1, "])"])

    tab = "    "
    for i in range(0, launch_l_list.__len__()):
        l =  launch_l_list[i]
        f.write((tab * l[0]) + l[1] + "\n")
    logger.debug("finished creating luanch script, ||%s|| " % launch_conf.launch_file)

def construct_bash_script(launch_conf: launch_configuration, ros_setup_bash_path="/opt/ros/foxy/setup.bash"):
    """
    Does several things relevant to loading launch configuration:
        1: removes previous build relics
        2: adds packages whose build statuses are set to true to colcon build, and builds them
        3: sources setup.sh for both ros2 and for this colcon build
        4: launches auto-generated 
    """
    bash_name = "simple_run_commands.sh"

    f = open("./%s"  % (bash_name), "w")

    #Set file to be executable by all
    logger.debug("giving underconstruction bash script execute privilege")
    os.system("chmod a+x ./%s" % (bash_name))
    
    #bash needs this becasuse ???
    logger.debug("writing to bash script")
    f.write("#!/bin/bash\n\n\n")
    
    #get rid of previous build relics
    f.write("rm -r build install\n\n")

    #collect all packages in "packages_to_launch" and add them to colcon build
    #apparently you can do list comprehension on string formatting. neat

    #this breaks every package down into seperate strings, adds a space before each package, and then combines them into one new string to append to the bash script
    pkgs_to_build = []
    for pkg in launch_conf.packages_to_run:
        if pkg.build == True:
            pkgs_to_build.append(pkg)

    f.write("colcon build --packages-select" +  \
        "".join( [" %s" % pkg.name for pkg in list(pkgs_to_build)]) + "\n\n" )

    #Source ros2, and the newly built package
    f.write("source %s\n\n" % ros_setup_bash_path)
    f.write("source install/setup.sh\n\n")

    #launch your package's launch file.
    f.write("ros2 launch %s  %s" % (launch_conf.config_store_pkg.name, launch_conf.launch_file))
    

    #close the write stream to make it unoccupied and launch the bash script as a sub process which pipes back to this temrinal
    f.close()
    
    #launch the launch file with your desired packages inside
    logger.debug("launching bash script")
    rc = subprocess.call("./%s" % bash_name)

def create_urdf_of_model(launch_conf: launch_configuration):
    """
    Take a FreeCAD model file named after the urdf in the launch_conf, and convert it to a URDF, and place .DAE files of the model inside the package model directory of the rviz config's parent package:

    I.E:
        If rviz_config.conf is stored in model_pkg, then auto_urdf.urdf will be stored in model_pkg<the root one>/models

    NOTE: !!!THE FREECAD MODEL SHOULD HAVE THE SAME NAME AS THE URDF FILE!!!
    """
    #)
    logger.debug("creating urdf file")

    #urdf_config_path = "urdf_file_settings.json"
    
    #tell launch conf to save relevant information to yaml
    launch_conf.save_self_as_yaml()
    #f = open(urdf_config_path, "w")


    #params = {
    #    "project_dir": os.getcwd() + "/",
    #    "pkg": launch_conf.config_store_pkg.name,
    #    "urdf_name": launch_conf.urdf_file_name,
    #    "log_folder": log_path_folder,
    #}
    #f.write(json.dumps(params))
    #f.close()

    os.system("python3 %s" % urdf_converter_macro_path)

    logger.info("exported FreeCAD model to urdf file, ||%s||" % (launch_conf.urdf_file_name + urdf_file_extension))

#env_to_use = real_rviz_env_conf
"""ros2 configuration to use, look at lauch configurations to see what each one does."""

def launch_gazebo_world(launch_conf: launch_configuration):
    """
    generate an urdf file, convert that to an sdf file, then launch that sdf file.
    
    BROKEN: I haven't found a way to get an sdf to launch in gazebo ignition. Help here needed
    """
#    create_urdf_of_model(env_to_use, freecad_macros_folder_name, model_file_name, launch_conf.urdf_file)
#    sdf_path =  "%s.sdf" % launch_conf.config_store_pkg.urdf_path
#    final_command = "gazebo.gz sdf -p %s" % (launch_conf.config_store_pkg.urdf_path)

#    sdf_as_bytes = subprocess.check_output(final_command, shell=True)
#    """gets gazebo to use its urdf -> sdf utility, and sub process captures its output as bytes"""
#    sdf_as_string = ''.join(map(chr, sdf_as_bytes))
#    """do ??? -^ to convert the bytes output to a string"""
#    sdf_file = open(sdf_path, "w")
#    """open a new file to write the sdf_as_string to."""
#    sdf_file.write(sdf_as_string)
#    sdf_file.close()
    
    launch_world_command = "gazebo.gz service -s /world/empty/create --reqtype ignition.msgs.EntityFactory --reptype ignition.msgs.Boolean --timeout 1000 --req 'sdf_filename: \"%s\", name: \"urdf_model\"'" % sdf_path
    print(launch_world_command)
    os.system(launch_world_command)

