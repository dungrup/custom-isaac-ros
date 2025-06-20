from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    container = ComposableNodeContainer(
        name='isaac_ros_vslam_zed2rosbag_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container_mt',
        output='screen',
        composable_node_descriptions=[
            # Left Image Format Converter
            ComposableNode(
                package='isaac_ros_image_proc',
                plugin='nvidia::isaac_ros::image_proc::ImageFormatConverterNode',
                name='image_format_node_left',
                parameters=[{
                    'encoding_desired': 'rgb8',
                    'image_width': 1280,
                    'image_height': 720,
                }],
                remappings=[
                    ('image_raw', '/zed/zed_node/left/image_rect_color'),
                    ('image', '/left/image_rect')
                ]
            ),
            # Right Image Format Converter
            ComposableNode(
                package='isaac_ros_image_proc',
                plugin='nvidia::isaac_ros::image_proc::ImageFormatConverterNode',
                name='image_format_node_right',
                parameters=[{
                    'encoding_desired': 'rgb8',
                    'image_width': 1280,
                    'image_height': 720,
                }],
                remappings=[
                    ('image_raw', '/zed/zed_node/right/image_rect_color'),
                    ('image', '/right/image_rect')
                ]
            ),
            # Visual SLAM Node
            ComposableNode(
                package='isaac_ros_visual_slam',
                plugin='nvidia::isaac_ros::visual_slam::VisualSlamNode',
                name='visual_slam_node',
                parameters=[{
                    'enable_slam_visualization': True,
                    'enable_landmarks_view': True,
                    'enable_observations_view': True,
                    'map_frame': 'map',
                    'odom_frame': 'odom',
                    'base_frame': 'zed_camera_center',
                    'camera_optical_frames': [
                        'zed_left_camera_optical_frame',
                        'zed_right_camera_optical_frame'
                    ]
                }],
                remappings=[
                    ('visual_slam/image_0', '/left/image_rect'),
                    ('visual_slam/camera_info_0', '/zed/zed_node/left/camera_info'),
                    ('visual_slam/image_1', '/right/image_rect'),
                    ('visual_slam/camera_info_1', '/zed/zed_node/right/camera_info'),
                ],
            )
        ]
    )

    return LaunchDescription([container])
