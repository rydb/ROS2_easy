
![](ROS2_easy.png) 


[![Github All Releases](https://img.shields.io/github/downloads/rydb/ROS2_easy/total.svg)]()

- [Description](#description)
- [Requirements](#requirements)
- [Optional Requirements:](#optional-requirements)
- [Installation](#installation)
- [To demo](#to-demo)
- [To use:](#to-use)
- [Tools:](#tools)
- [setup.py replacer:](#setuppy-replacer)
- [launch file generator:](#launch-file-generator)
- [ros2 enviorment runner:](#ros2-enviorment-runner)
- [gazebo sdf loader(HELP NEEDED):](#gazebo-sdf-loaderhelp-needed)
- [(FREECAD MODELS ONLY \& WIP): model -\> urdf converter](#freecad-models-only--wip-model---urdf-converter)


## Description

This is a collection of tools to remove ROS 2's worflow hurdles for python3/colcon based projects

## Requirements

- [ROS 2](https://docs.ros.org/en/foxy/Installation.html)(only tested on foxy)
- Bash
- RVIZ2
- colcon

## Optional Requirements:

- [snapcraft](https://snapcraft.io/snapcraft) + FreeCAD(if using the URDF converter)
## Installation

```bash
pip install ros2_easy
```
if using the model -> urdf -> sdf converter for FreeCAD as well:
```bash
sudo snap install freecad
freecad.pip install pycollada
freecad.pip install trimesh
```

## To demo

```
git clone https://github.com/rydb/ROS2_easy.git
run simple_run_caller.py
```

## To use:

1: ensure your ROS 2 file structure is in the following format:

```
/project_dir
	/src
		/example_pkg
			/rviz
				example_rviz.rviz
			/launch
			/example_pkg
				__init__.py
				sample_code.py
			/urdf

			/models
				(OPTIONAL)
				FreeCAD_model.FCstd
				
			package.xml
			setup.cfg
			setup.py
		/other_pkg1
		/other_pkg2
	simple_run_caller.py
	export_model_to_urdf.py  #if using the FreeCAD urdf_converter
```
2: define your packages in terms of ros2_easy ```Package``` objects. E.G:

```python
#for example package
example_pkg = Package("example_pkg", "sample_code", build=True, entry_point="main")

#for rviz(to be moved to common_packages later)
rviz2_config_name = "rviz_config_test.rviz"
rviz2_pkg = Package("rviz2", "rviz2", config=Config(config_file_name=rviz2_config_name), optional_launch_file_node_args= {"arguments": "['-d', share_directory + '/rviz/%s']" % rviz2_config_name})
```

3: define your ros2 project enviorment as a ros2_easy ```launch_configuration```. E.G:

```python
rviz_env_conf = launch_configuration(
    config_store_pkg=example_pkg,
    launch_file="example_launch.py",
    urdf_file_name="FreeCAD_model",
    packages_to_run=[example_pkg, rviz2_pkg, rqt_pkg, robot_state_publisher_pkg],
    )
	"""launch configuration for testing sample_code.py""""
```

4: run the tools you'd like to use

```python
#add all folders in example_pkg to .install folder
simple_run.replace_setup_py(rviz_env_conf)
#generate a launch file to run based on launch_configuration
simple_run.generate_launch_py(rviz_env_conf)
#(OPTIONAL AND WIP) convert a FreeCAD model defined in export_model_to_urdf.py
# and convert from model -> urdf
simple_run.create_urdf_of_model(rviz_env_conf)
# run launch configuration
simple_run.construct_bash_script(rviz_env_conf)


```

## Tools:

## setup.py replacer:
		
when ran, the setup.py replacer will replace a package's old setup.py with one which adds every sub folder in your config storing package to PATHS, this way, you don't need to manually edit setup.py. Call this function, set its variables, and no longer worry about configs not being added to PATHS (should make this backup old one to an archive folder to make this not accidently destructive..) (also need to make it so folders inside folders get added...)

## launch file generator:

stream-line the process of creating a launch file by avoiding editing launch files them selves and instead using the launch_configuration class. simply define your packages/external programs to run with the package class/CMD_program classes respectively, add them to your launch_configuration, and the generator will make a launch file to accomidate them.
		
## ros2 enviorment runner:
		
when ran will: 

- delete old build relics

- generate a .sh bash script which sources ROS 2

- colcon builds packages you've defined in your launch_configuration(clarify on this later),

- sources your built packages

- runs your generated launch file from the launch file generator

## gazebo sdf loader(HELP NEEDED):

converts your urdf to sdf and loads it in an empty gazebo world(add more details/features here)

<span style="color:red"> help needed here to better gazebo integration with this library!  </span>

## (FREECAD MODELS ONLY & WIP): model -> urdf converter

by moving the `export_model_to_urdf.py` script next to your simple_run caller script, and calling 
```python
 simple_run.create_urdf_of_model(<your_luanch_configuration>) 
```
you can hard code your model into a Model class equivilent, and then export that as a urdf.

A graphical version of this tool is TODO

