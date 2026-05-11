# mobile_manipulator_description

Scout Mini + OpenMANIPULATOR-X 모바일 매니퓰레이터 Gazebo 시뮬레이션 패키지.

자율주행 택배 로봇 캡스톤 프로젝트의 일부로, Scout Mini 위에 알루미늄 프레임과 OpenMANIPULATOR-X 로봇팔을 합체한 URDF 및 Gazebo 환경을 제공합니다.

## 구성

| 부품 | 규격 | 위치 (base_link 기준) |
|------|------|----------------------|
| Scout Mini | — | base |
| 알루미늄 프로파일 × 4 | 40×40×650 mm | z=0.394 (중심) |
| 상판 | 350×277×5 mm | z=0.7215 |
| OpenMANIPULATOR-X | — | x=-0.128, z=0.724 (후방, LiDAR 시야 확보) |
| LiDAR (RPLiDAR A2) | cylinder r=38mm | x=0.05, z=0.77 |
| IMU (EBIMU24GV6) | 35×35×13 mm | x=-0.04, z=0.731 |
| D435 카메라 | — | Scout Mini 전방 (sm.xacro 기본값) |

## 의존 패키지

```
scout_ros2 (수정본 포함, 아래 참고)
open_manipulator_x_description
realsense2_description
```

## 설치

### 1. 워크스페이스 준비

```bash
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws/src
git clone https://github.com/uihyeong/mobile_manipulator_description.git
```

### 2. scout_ros2 설치 (수정본)

`sm.xacro`에 `laser_x` / `imu_x` 파라미터가 추가된 수정본이 필요합니다.
원본(`westonrobot/scout_ros2`) 대신 이 레포에 포함된 패치 파일을 사용하세요.

```bash
# westonrobot 원본 clone
cd ~/ros2_ws2/src
git clone https://github.com/westonrobot/scout_ros2.git

# 수정된 sm.xacro 덮어쓰기
cp ~/colcon_ws/src/mobile_manipulator_description/patch/sm.xacro \
   ~/ros2_ws2/src/scout_ros2/scout_description/urdf/sm.xacro

# 빌드
cd ~/ros2_ws2
colcon build --packages-select scout_description --symlink-install
```

### 3. 빌드

```bash
source ~/ros2_ws2/install/setup.bash
cd ~/colcon_ws
colcon build --packages-select mobile_manipulator_description --symlink-install
```

## 실행

```bash
source ~/ros2_ws2/install/setup.bash
source ~/colcon_ws/install/setup.bash
ros2 launch mobile_manipulator_description mobile_manipulator_gazebo.launch.py
```

## 주요 설계 결정

- **팔 후방 배치** (`x=-0.128`): LiDAR 전방 시야를 확보하기 위해 팔을 후방에 배치
- **팔 gravity=false**: Gazebo 컨트롤러 없이도 joints=0 자세 유지
- **LiDAR z=0.77**: 상판 윗면(z=0.724)으로부터 25mm 여유 → 자기 충돌 방지
- **sm.xacro 수정**: `laser_x`, `imu_x` 파라미터 추가로 LiDAR/IMU x 위치를 launch에서 조정 가능

## 좌표 기준 (base_link)

```
z=0.069  Scout Mini 차체 상단 (메시 실측)
z=0.394  알루미늄 프로파일 중심
z=0.719  프로파일 상단 / 상판 하면
z=0.724  상판 상면 / 팔 arm_base_joint
z=0.731  IMU 중심
z=0.77   LiDAR 중심
```

## 관련 레포

- [elevator-button-robot](https://github.com/uihyeong/elevator-button-robot) — 엘리베이터 버튼 누르기 노드 (Gemini VLM / YOLO + IK)
