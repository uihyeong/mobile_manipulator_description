# mobile_manipulator_description

Scout Mini + OpenMANIPULATOR-X 모바일 매니퓰레이터 Gazebo 시뮬레이션 패키지.

자율주행 택배 로봇 캡스톤 프로젝트의 일부로, Scout Mini 위에 알루미늄 프레임과 OpenMANIPULATOR-X 로봇팔을 합체한 URDF 및 Gazebo 환경을 제공합니다.

## 구성

| 부품 | 규격 | 위치 (base\_link 기준) |
|------|------|----------------------|
| Scout Mini | — | base |
| 알루미늄 프로파일 × 4 | 40×40×650 mm | z=0.394 (중심) |
| 상판 | 350×277×5 mm | z=0.7215 |
| OpenMANIPULATOR-X | — | x=−0.128, z=0.724 (후방, LiDAR 시야 확보) |
| LiDAR (RPLiDAR A2) | cylinder r=38 mm | x=0.05, z=0.77 |
| IMU (EBIMU24GV6) | 35×35×13 mm | x=−0.04, z=0.731 |
| D435 카메라 | — | Scout Mini 전방 (sm.xacro 기본값) |

## 의존 패키지

설치 전에 아래 패키지들이 있어야 합니다.

### 1. scout\_ros2 (westonrobot)

이미 설치되어 있다면 **[sm.xacro 패치 적용](#2-smxacro-패치-적용)** 단계만 진행하세요.

없다면:
```bash
cd <your_ws>/src
git clone https://github.com/westonrobot/scout_ros2.git
```

### 2. sm.xacro 패치 적용

이 레포의 `sm.xacro`에는 LiDAR/IMU x 위치 조정 파라미터(`laser_x`, `imu_x`)가 추가되어 있습니다.
원본 scout\_ros2의 `sm.xacro`를 아래 파일로 **덮어쓰세요**.

```bash
# 이 레포를 먼저 clone 한 뒤
git clone https://github.com/uihyeong/mobile_manipulator_description.git

# scout_ros2의 sm.xacro 위치에 맞게 경로를 수정해서 복사
cp mobile_manipulator_description/patch/sm.xacro \
   <your_ws>/src/scout_ros2/scout_description/urdf/sm.xacro

# scout_description 재빌드
cd <your_ws>
colcon build --packages-select scout_description --symlink-install
```

### 3. open\_manipulator\_x\_description

```bash
cd <your_ws>/src
git clone -b humble https://github.com/ROBOTIS-GIT/open_manipulator_x.git
cd <your_ws>
colcon build --packages-select open_manipulator_x_description
```

### 4. realsense2\_description

```bash
sudo apt install ros-humble-realsense2-description
```

## 설치

위 의존성이 모두 준비된 후:

```bash
cd <your_ws>/src
git clone https://github.com/uihyeong/mobile_manipulator_description.git
cd <your_ws>
source /opt/ros/humble/setup.bash
colcon build --packages-select mobile_manipulator_description --symlink-install
```

## 실행

```bash
# 의존 워크스페이스들을 모두 source한 뒤
source <scout_ws>/install/setup.bash     # scout_ros2가 있는 워크스페이스
source <your_ws>/install/setup.bash

ros2 launch mobile_manipulator_description mobile_manipulator_gazebo.launch.py
```

## 주요 설계 결정

- **팔 후방 배치** (`x=−0.128`): LiDAR 전방 시야를 확보하기 위해 팔을 후방에 배치
- **팔 gravity=false**: Gazebo 컨트롤러 없이도 joints=0 자세 유지
- **LiDAR z=0.77**: 상판 윗면(z=0.724)으로부터 25 mm 여유 → 자기 충돌 방지
- **sm.xacro 수정**: `laser_x`, `imu_x` 파라미터 추가로 LiDAR/IMU x 위치를 launch 파일에서 조정 가능

## 좌표 기준 (base\_link)

```
z=0.069  Scout Mini 차체 상단 (메시 실측)
z=0.394  알루미늄 프로파일 중심
z=0.719  프로파일 상단 / 상판 하면
z=0.724  상판 상면 / 팔 arm_base_joint
z=0.731  IMU 중심
z=0.770  LiDAR 중심
```

## 관련 레포

- [elevator-button-robot](https://github.com/uihyeong/elevator-button-robot) — 엘리베이터 버튼 누르기 노드 (Gemini VLM / YOLO + IK)
