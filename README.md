
![](ROS2_easy.png) 

[![Github All Releases](https://img.shields.io/github/downloads/rydb/ROS2_easy/total.svg)]()

## Description

This is a collection of tools to remove ROS2's worflow hurdles.

## Dependencies

- ROS2(only tested on foxy)
- Bash
- RVIZ2
  
## Installation

```bash
pip install ros2_easy
```

## Tools:
	
	FreeCAD model -> urdf converter:
		(insert gif)
		
		convert FreeCAD models to urdf via the converter function. 
		
		#insert example here
		
		
	setup.py replacer:
		automatically replace a package's old setup.py with one which adds every sub folder in your config storing package to PATHS, this way,
		you don't need to manually edit setup.py. Call this function, set its variables, and no longer worry about configs not being added to PATHS
		(should make this backup old one to an archive folder to make this not accidently destructive..)
		(also need to make it so folders inside folders get added...)
		
	launch file generator:
		stream-line the process of creating a launch file by avoiding editing launch files them selves and instead using the launch_configuration class.
		
		simply define your packages/external programs to run with the package class/CMD_program classes respectively,
		add them to your launch_configuration, and the generator will make a launch file to accomidate them.
		
	ros2 enviorment runner:
		automatically: 
			delete old build relics
		
			generate a .sh bash script which sources ROS2
			
			colcon builds packages you've defined in your launch_configuration(clarify on this later),
			
			sources your built packages
			
			runs your generated launch file from the launch file generator

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

## To Use:
	See turtlebot3 example(need to add)


