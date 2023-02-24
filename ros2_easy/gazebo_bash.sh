#!/bin/bash


killall ruby

export GZ_SIM_RESOURCE_PATH=/home/rydb/Projects/ROS2_easy/src:

gz sim /home/rydb/Projects/ROS2_easy/src/model_pkg/urdf/diff_bot.sdf

