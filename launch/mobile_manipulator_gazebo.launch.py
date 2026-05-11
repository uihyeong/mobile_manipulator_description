import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def _share_parent(pkg: str) -> str:
    """패키지 share 디렉토리의 부모 경로 반환 (GAZEBO_MODEL_PATH 용)."""
    return os.path.dirname(get_package_share_directory(pkg))


def generate_launch_description():

    spawn_z = DeclareLaunchArgument('spawn_z', default_value='0.3')

    # Gazebo가 package:// URI 메시를 찾을 수 있도록 경로 추가
    gazebo_model_path = SetEnvironmentVariable(
        'GAZEBO_MODEL_PATH',
        ':'.join([
            _share_parent('open_manipulator_x_description'),
            _share_parent('realsense2_description'),
            _share_parent('scout_description'),
            os.environ.get('GAZEBO_MODEL_PATH', ''),
        ])
    )

    robot_description = ParameterValue(
        Command([
            'xacro ',
            PathJoinSubstitution([
                FindPackageShare('mobile_manipulator_description'),
                'urdf', 'mobile_manipulator.urdf.xacro'
            ]),
            ' use_sim:=true',
        ' laser_x:=0.05',
        ' laser_z:=0.77',
        ' imu_x:=-0.04',
        ' imu_z:=0.731',
        ]),
        value_type=str,
    )

    gazebo = ExecuteProcess(
        cmd=[
            'gazebo', '--verbose',
            '-s', 'libgazebo_ros_init.so',
            '-s', 'libgazebo_ros_factory.so',
        ],
        output='screen',
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
    )

    spawn = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'mobile_manipulator',
            '-z', LaunchConfiguration('spawn_z'),
        ],
        output='screen',
    )

    return LaunchDescription([
        gazebo_model_path,
        spawn_z,
        gazebo,
        robot_state_publisher,
        spawn,
    ])
