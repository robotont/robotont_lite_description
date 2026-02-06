from ament_index_python.packages import get_package_share_path
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

# TODO: look for a common utility place for this function
def _rgba_string_from_user_value(user_value: str) -> str:
    s = (user_value or "").strip()
    if not s:
        raise ValueError("Empty color string")

    # RGBA numeric input (space or comma separated)
    parts = s.replace(",", " ").split()
    if len(parts) == 4:
        nums = [float(p) for p in parts]
        if any(v > 1.0 for v in nums):
            nums = [v / 255.0 for v in nums]
        nums = [min(1.0, max(0.0, v)) for v in nums]
        return f"{nums[0]} {nums[1]} {nums[2]} {nums[3]}"

    # Hex input
    if s.startswith("#") and len(s) in (7, 9):
        hexv = s[1:]
        r = int(hexv[0:2], 16)
        g = int(hexv[2:4], 16)
        b = int(hexv[4:6], 16)
        a = int(hexv[6:8], 16) if len(hexv) == 8 else 255
        return f"{r/255.0} {g/255.0} {b/255.0} {a/255.0}"

    # Color names
    name = s.lower().replace("_", "")
    try:
        from PIL import ImageColor
        r, g, b, a = ImageColor.getcolor(name, "RGBA")
        return f"{r/255.0} {g/255.0} {b/255.0} {a/255.0}"
    except Exception:
        fallback = {
            "lightblue": "0.16 0.65 0.98 1.0",
            "blue":      "0.00 0.35 0.90 1.0",
            "yellow":    "1.00 1.00 0.00 1.0",
            "black":     "0.10 0.10 0.10 1.0",
            "purple":    "0.45 0.20 0.65 1.0",
            "gray":      "0.75 0.75 0.75 1.0",
            "darkgreen": "0.00 0.45 0.25 1.0",
            "green":     "0.00 0.80 0.30 1.0",
        }
        if name in fallback:
            return fallback[name]
        raise ValueError(
            f"Unknown color '{user_value}'. Provide RGBA ('0 1 0 1'), hex ('#00ff00'), "
            f"or install Pillow for CSS color names."
        )
    
def launch_setup(context, *args, **kwargs):
    namespace = LaunchConfiguration('namespace').perform(context)
    frame_prefix = LaunchConfiguration('frame_prefix').perform(context)
    model = LaunchConfiguration("model").perform(context).strip()
    generation = LaunchConfiguration("generation").perform(context).strip()
    primary_in = LaunchConfiguration("primary_color").perform(context)
    secondary_in = LaunchConfiguration("secondary_color").perform(context)

    lite_pkg = get_package_share_path("robotont_lite_description")
    gen_pkg = get_package_share_path("robotont_description")

    if model:
        robot_model_path = model
    else:
        if generation == "3":
            robot_model_path = str(gen_pkg / "urdf/gen3/robotont.urdf.xacro")
        elif generation == "2.1":
            robot_model_path = str(gen_pkg / "urdf/gen2_1/robotont.urdf.xacro")
        else:
            robot_model_path = str(lite_pkg / "urdf/lite3/robotont_lite.urdf.xacro")

    primary_rgba = _rgba_string_from_user_value(primary_in)
    secondary_rgba = _rgba_string_from_user_value(secondary_in)

    robot_description = ParameterValue(
        Command([
            "xacro ", robot_model_path,
            ' prefix:=', frame_prefix,
            ' main_color:="', primary_rgba, '"',
            ' second_color:="', secondary_rgba, '"',
        ]),
        value_type=str,
    )

    print("Uploading Robotont Lite description...")
    print (f"  generation: {generation}")
    print (f"  namespace: '{namespace}'")
    print (f"  frame_prefix: '{frame_prefix}'")
    print (f"  primary_color: '{primary_rgba}'")
    print (f"  secondary_color: '{secondary_rgba}'")
    print (f"  robot_model_path: '{robot_model_path}'")
    print (f"  robot_description length: {robot_description}")
    
    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=namespace,
            parameters=[{'robot_description': robot_description}],
        )
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument("model", default_value=""),
        DeclareLaunchArgument('namespace', default_value=''),
        DeclareLaunchArgument('frame_prefix', default_value=''),
        DeclareLaunchArgument('generation', default_value='lite3'),
        DeclareLaunchArgument("primary_color", default_value="0.16 0.65 0.98 1.0"),
        DeclareLaunchArgument("secondary_color", default_value="0.0 1.0 1.0 1.0"),
        OpaqueFunction(function=launch_setup)
    ])