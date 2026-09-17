from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, RegisterEventHandler, EmitEvent, LogInfo
from launch.events import Shutdown
from launch.event_handlers import (
    OnProcessExit
)
from launch.substitutions import LaunchConfiguration, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    ## [Getting the values of the tracker-related launch arguments]
    config_file = LaunchConfiguration("config_file")
    depth_camera_info_topic_name = LaunchConfiguration("depth_camera_info_topic_name")
    depth_image_topic_name = LaunchConfiguration("depth_image_topic_name")
    display_nb_frames_skipped = LaunchConfiguration("display_nb_frames_skipped")
    headless_mode = LaunchConfiguration("headless_mode")
    init_file = LaunchConfiguration("init_file")
    init_method = LaunchConfiguration("init_method")
    init_topic  = LaunchConfiguration("init_topic")
    rgb_camera_info_topic_name = LaunchConfiguration("rgb_camera_info_topic_name")
    rgb_image_topic_name = LaunchConfiguration("rgb_image_topic_name")
    stream_qos_depth = LaunchConfiguration("stream_qos_depth")
    stream_qos_durability = LaunchConfiguration("stream_qos_durability")
    stream_qos_reliability = LaunchConfiguration("stream_qos_reliability")
    z_factor = LaunchConfiguration("z_factor")
    ## [Sequence launch arguments]
    init_pose_topic_name = "/other_tracker/pose"
    object_name  = LaunchConfiguration("object_name")

    # ------------------------------------------------------------------ #
    #  Launch arguments                                                    #
    # ------------------------------------------------------------------ #
    declared_args = [
       # BEGIN_RBT_ARGUMENTS
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            'config_file',
            description="Absolute path towards the JSON config file for the RBT",
            default_value=PathJoinSubstitution(
              [
                FindPackageShare('visp_tk_tutorials'),
                'config',
                'rbt',
                'configs',
                'depth-ccd-mask.json'
              ])
        ),
        DeclareLaunchArgument(
            "depth_camera_info_topic_name",
            description="Name of the depth camera topic.",
            default_value="/camera_rgb/depth/camera_info"
        ),
        DeclareLaunchArgument(
            "depth_image_topic_name",
            description="Name of the depth stream topic.",
            default_value="/camera_rgb/depth/image_raw"
        ),
        DeclareLaunchArgument(
            "display_nb_frames_skipped",
            description = "This parameter indicates the number of frames skipped during display",
            default_value="-1"
        ),
        DeclareLaunchArgument(
            "headless_mode",
            description = "If True, the node will not display anything, expecting that another takes in charge the GUI.",
            default_value="False"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            'init_file',
            description="Absolute path towards the `.init` file that indicates the clicks location to initialize the RBT",
            default_value=PathJoinSubstitution(
              [
                FindPackageShare('visp_tk_tutorials'),
                'config',
                'rbt',
                'models',
                'dragon',
                'dragon.init'
              ])
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "init_method",
            description="Initialization method to initialize the tracker. Default method is initialization by click.",
            default_value="topic"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "init_topic",
            description="If the ``init_method`` is set to topic, this parameter becomes **REQUIRED** and must be set to the topic of type ``geometry_msgs:msg::PoseStamped`` the tracker must use to get the init pose.",
            default_value=init_pose_topic_name
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "rgb_camera_info_topic_name",
            description="Name of the color camera topic.",
            default_value="/camera_rgb/color/camera_info"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "rgb_image_topic_name",
            description="Name of the color image topic.",
            default_value="/camera_rgb/color/image_raw"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "stream_qos_depth",
            description="The depth of the queue of both the RGB and depth image streams (they need to be the same) if depth is required.",
            default_value="5"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "stream_qos_durability",
            description="The durability of both the RGB and depth image streams (they need to be the same) if depth is required.",
            default_value="volatile"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "stream_qos_reliability",
            description="The reliability of both the RGB and depth image streams (they need to be the same) if depth is required.",
            default_value="best_effort"
        ),
        DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
            "z_factor",
            description="Factor to convert the depth image expressed as uint16_t into meters. For instance, if a value of ``1000`` in the raw depth image corresponds to ``1 meter``, the ``z_factor`` must be set to ``0.001``.",
            default_value="0.001"
        ),
      # END_RBT_ARGUMENTS
      DeclareLaunchArgument( # used to define the launch argument that can be passed from another launch file or from the console.
          "object_name",
          description="Name of the object to track in the sequence.",
          default_value="dragon"
      ),
      # END_SEQ_ARGS
        SetEnvironmentVariable(name='GOMP_SPINCOUNT', value='0'), # To enable OpenMP acceleration
      # END_SET_ENV
    ]

    # ------------------------------------------------------------------ #
    #  ROS2 bag node node                                                    #
    # ------------------------------------------------------------------ #
    # BEGIN_sequence_player
    sequence_folder = PathJoinSubstitution(
        [FindPackageShare("visp_tk_tutorials"), "sequence"]
    )
    sequence_player = Node(
        package='visp_tk_tutorials',
        # namespace="rbt_ns",
        executable='sequence_player_node',
        name='sequence_player',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'sequence_path' : sequence_folder},
            {'object_name': object_name},
            {'depth_image_topic_name': depth_image_topic_name},
            {'depth_camera_info_topic_name':depth_camera_info_topic_name},
            {'rgb_image_topic_name':rgb_image_topic_name},
            {'rgb_camera_info_topic_name':rgb_camera_info_topic_name},
            {'init_pose_topic_name': init_pose_topic_name}
        ]
      )
    # BEGIN_sequence_player

    # ------------------------------------------------------------------ #
    #  RBT tracker node                                               #
    # ------------------------------------------------------------------ #
    # BEGIN_RBT_NODE
    rbt_node = Node(
        package='visp_rbt',
        # namespace="rbt_ns",
        executable='visp_rbt_node',
        name='tracker_rbt',
        output='screen',
        emulate_tty=True,
        parameters=[
            {'config_file' : config_file},
            {'depth_camera_info_topic_name' : depth_camera_info_topic_name},
            {'depth_image_topic_name' : depth_image_topic_name},
            {'display_nb_frames_skipped' : display_nb_frames_skipped},
            {'headless_mode' : headless_mode},
            {'init_file' : init_file},
            {'init_method' : init_method},
            {'init_topic' : init_topic},
            {'rgb_camera_info_topic_name' : rgb_camera_info_topic_name},
            {'rgb_image_topic_name' : rgb_image_topic_name},
            {'stream_qos_depth' : stream_qos_depth},
            {'stream_qos_durability' : stream_qos_durability},
            {'stream_qos_reliability' : stream_qos_reliability},
            {'z_factor' : z_factor}
        ]
    )
    # BEGIN_RBT_NODE

    # BEGIN_SHUTDOWN
    shutdown_handler = RegisterEventHandler(
            OnProcessExit(
                target_action=rbt_node,
                on_exit=[
                    LogInfo(msg=("The tracking node was closed, turning off the launch file")),
                    EmitEvent(event=Shutdown(
                        reason="tracking node closed"))
                ]
            )
        )
    # END_SHUTDOWN

    return LaunchDescription(declared_args + [sequence_player, rbt_node, shutdown_handler])
