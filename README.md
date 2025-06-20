# Use zed2 camera rosbags with Isaac ROS! 

Pretty self-explanatory 🤷‍♂️️

This repo is for those people who struggled working with NVIDIA's Isaac ROS VSLAM packages with custom rosbags (like me!). It took me forever to understand what's exactly needed by the package! Here is a helping hand! 

## Prerequisites

I work on a Jetson AGX Orin Dev Kit 64GB running JP6.2. I am not a big fan of docker so I installed the dependencies through the apt packages Nvidia provides (phew!). To get this package working install the following:

- [ROS 2](https://nvidia-isaac-ros.github.io/getting_started/isaac_apt_repository.html) (tested with Humble) 
- [Isaac ROS packages](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_visual_slam/isaac_ros_visual_slam/index.html#quickstart):
  - `isaac_ros_image_proc`
  - `isaac_ros_visual_slam`
- [ZED camera ROS 2 drivers](https://nvidia-isaac-ros.github.io/getting_started/hardware_setup/sensors/zed_setup.html) (for recording `/zed/zed_node/...` topics)

If you prefer working with dockers, follow Nvidia's advice when working with Jetsons and get yourself a nice big nvme stick. Do [this](https://nvidia-isaac-ros.github.io/getting_started/hardware_setup/compute/jetson_storage.html) to ensure your docker data is in the nvme and your not chewing up the limited memory in the Jetsons. Follow the rest of NVIDIA's instructions [to setup the environment](https://nvidia-isaac-ros.github.io/getting_started/dev_env_setup.html).

## Building the Package

From your ROS 2 workspace root:

```
cd ~/ros2_ws/src
git clone <this_repo>
cd ~/ros2_ws
colcon build --packages-select custom-isaac-ros
source install/setup.bash
```

Add to ~/.bashrc to make life easy :stuck_out_tongue_closed_eyes:

## Usage
1. Launch the Processing Pipeline
This will start the image format converters and Visual SLAM node:

```
ros2 launch custom-isaac-ros custom_vslam.launch.py
```

The visual slam node expects the images to be in rgb8 and the image dimensions should be even. You can do this using simple OpenCV but we will use Isaac ROS's Image processing [package](https://nvidia-isaac-ros.github.io/repositories_and_packages/isaac_ros_image_pipeline/index.html#packages) to do this instead. 

2. Play your rosbag. The rosbag should have the following topics

```
/zed/zed_node/left/image_rect_color
/zed/zed_node/right/image_rect_color
/zed/zed_node/left/camera_info
/zed/zed_node/right/camera_info
/tf
/tf_static
```

3. Visualize the results of VSLAM using:

```
rviz2 -d $(ros2 pkg prefix isaac_ros_visual_slam --share)/rviz/default.cfg.rviz

```

