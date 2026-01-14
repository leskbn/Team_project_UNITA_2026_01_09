import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # 1. 패키지 이름과 URDF 파일 이름 설정 (이 부분만 본인 환경에 맞게 수정하세요!)
    package_name = 'description_package'
    urdf_file_name = 'unita_robot_body.urdf'  # 만약 xacro라면 'my_robot.urdf.xacro'
    rviz_file_name = 'unita_robot.rviz'

    # 2. 파일 경로 찾기 (share 디렉토리 기준)
    pkg_path = get_package_share_directory(package_name)
    xacro_file = os.path.join(pkg_path, 'urdf', urdf_file_name)
    rviz_config_file = os.path.join(pkg_path, 'rviz', rviz_file_name)

    # 3. 로봇 설명(Robot Description) 파라미터 생성
    # xacro 명령어를 실행해서 URDF 내용을 문자열로 받아옵니다.
    robot_description = Command(['xacro ', xacro_file])

    # 4. 노드 설정
    
    # 4-1. Robot State Publisher: 로봇의 관절 상태를 받아 TF(좌표)를 계산
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}]
    )

    # 4-2. Joint State Publisher GUI: 관절을 움직이는 슬라이더 창 띄우기
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # 4-3. RViz2: 시각화 도구 실행
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    # 5. 실행할 노드들을 리스트로 반환
    return LaunchDescription([
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])