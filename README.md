
![](ROS2_easy.png) 

[![Github All Releases](https://img.shields.io/github/downloads/rydb/ROS2_easy/total.svg)]()

## Description

This is a collection of tools to remove ROS2's worflow hurdles for python3/colcon based projects

## Requirements

- [ROS2](https://docs.ros.org/en/foxy/Installation.html)(only tested on foxy)
- Bash
- RVIZ2
- colcon  

- Packages must be <span style="color:red"> colcon</span> based. Cmake packages are currently not supported
## Installation

```bash
pip install ros2_easy
```

## Tools:

## setup.py replacer:
		
when ran, the setup.py replacer will replace a package's old setup.py with one which adds every sub folder in your config storing package to PATHS, this way, you don't need to manually edit setup.py. Call this function, set its variables, and no longer worry about configs not being added to PATHS (should make this backup old one to an archive folder to make this not accidently destructive..) (also need to make it so folders inside folders get added...)

## launch file generator:

stream-line the process of creating a launch file by avoiding editing launch files them selves and instead using the launch_configuration class. simply define your packages/external programs to run with the package class/CMD_program classes respectively, add them to your launch_configuration, and the generator will make a launch file to accomidate them.
		
## ros2 enviorment runner:
		
when ran will: 

- delete old build relics

- generate a .sh bash script which sources ROS2

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
and hard coding parts(as seen in <span style="color:blue"> !!!insert model_pkg example here!!! </span>of the model via ```Model``` class, you can convert a FreeCAD model to a urdf.

A graphical version of this tool is TODO

## ROS2 file structure to use:

```python
Root_folder:
	thing_that_calls_this.py
		src/
			Config_Storing_Package/
			urdfs/
			models/
			rviz/
```		
		
(ONLY TESTED ON UBUNTU AS OF NOW)

## Contributing:



## TODO:
	Add Cmake support

	make FreeCAD converter graphical

