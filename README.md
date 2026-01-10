# robotont_lite_description
Description package for robotont lite version that contains meshes, URDF and xacro files.

## Dependencies

1. List of dependencies

- rviz
- urdf
- xacro

2. Install dependencies

```
cd ~/<YOUR_WORKSPACE_NAME_HERE>
rosdep install --from-paths src --ignore-src -r -y
```

This package **depends on** the [`robotont_description`](https://github.com/robotont/robotont_description) package.

So, make sure that `robotont_description` is cloned into the **same ROS 2 workspace** as `robotont_lite_description`.

## Clone the repository
From the src folder of your workspace:

```
cd ~/<YOUR_WORKSPACE_NAME_HERE>/src
git clone https://github.com/robotont/robotont_lite_description.git
```

## Build
From the root of your workspace:

```
cd ~/<YOUR_WORKSPACE_NAME>
colcon build --packages-select robotont_lite_description
source install/setup.bash
```
## Usage

To display the robot model run:
```
ros2 launch robotont_lite_description display_robot_model.launch.py
```

Displays the robot's model in rviz, with different frame and lite module colors:

```bash
ros2 launch robotont_lite_description display_robot_model.launch.py primary_color:=light_blue
```

Supported formats for `primary_color` and `secondary_color`:
- color name:      primary_color:=lightblue 
- RGBA (0..1):     primary_color:="0.16 0.65 0.98 1.0"
- RGBA (0..255):   primary_color:="41 166 250 255"
- HEX:             primary_color:="#29a6faff" 

This launch file will start the necessary nodes and load the Robotont Lite description into RViz.

