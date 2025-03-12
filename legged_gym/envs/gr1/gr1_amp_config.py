# SPDX-FileCopyrightText: Copyright (c) 2021 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Copyright (c) 2021 ETH Zurich, Nikita Rudin
import glob

from legged_gym.envs.base.legged_robot_config import LeggedRobotCfg, LeggedRobotCfgPPO
from legged_gym.envs.gr1.gr1_config import GR1RoughCfg, GR1RoughCfgPPO
MOTION_FILES = glob.glob('/home/mao/Github_Project/AMP_for_Humanoid/datasets/mocap_motions_gr1/*')


class GR1AMPCfg(GR1RoughCfg):
    class env(GR1RoughCfg.env):
        num_envs = 4096
        include_history_steps = None  # Number of steps of history to include.
        num_observations = 44
        num_privileged_obs = 47
        reference_state_initialization = True
        reference_state_initialization_prob = 0.85
        amp_motion_files = MOTION_FILES
        num_actions = 12

    class init_state(GR1RoughCfg.init_state):
        pos = [0.0, 0.0, 1.0]  # x,y,z [m]
        default_joint_angles = {  # = target angles [rad] when action = 0.0
            'left_hip_roll_joint': 0.0,
            'left_hip_yaw_joint': 0.,
            'left_hip_pitch_joint': -0.14,
            'left_knee_pitch_joint': 0.28,
            'left_ankle_pitch_joint': -0.14,
            'left_ankle_roll_joint': -0.0,
            'right_hip_roll_joint': -0.0,
            'right_hip_yaw_joint': -0.,
            'right_hip_pitch_joint': -0.14,
            'right_knee_pitch_joint': 0.28,
            'right_ankle_pitch_joint': -0.14,
            'right_ankle_roll_joint': 0.0,

            # waist
            'waist_yaw_joint': 0.0,
            'waist_pitch_joint': 0.0,
            'waist_roll_joint': 0.0,

            # head
            'head_yaw': 0.0,
            'head_pitch': 0.0,
            'head_roll': 0.0,

            # left arm
            'left_shoulder_pitch_joint': 0.26,
            'left_shoulder_roll_joint': 0.0,
            'left_shoulder_yaw_joint': 0.0,
            'left_elbow_pitch_joint': -0.52,
            'left_wrist_yaw_joint': 0.0,
            'left_wrist_roll_link': 0.0,
            'left_wrist_pitch_joint': 0.0,

            # right arm
            'right_shoulder_pitch_joint': 0.26,
            'right_shoulder_roll_joint': 0.0,
            'right_shoulder_yaw_joint': 0.0,
            'right_elbow_pitch_joint': -0.52,
            'right_wrist_yaw_joint': 0.0,
            'right_wrist_roll_joint': 0.0,
            'right_wrist_pitch_joint': 0.0

        }

    class control(GR1RoughCfg.control):
        # PD Drive parameters:
        control_type = 'P'
        stiffness = {
            'hip_roll': 200, 'hip_yaw': 200, 'hip_pitch': 350,
            'knee_pitch': 350,
            'ankle_pitch': 20, 'ankle_roll': 5,
            # 'l_shoulder_pitch': 92.85, 'l_elbow_pitch': 112.06,
        }
        damping = {
            'hip_roll': 20, 'hip_yaw': 20, 'hip_pitch': 20,
            'knee_pitch': 20,
            'ankle_pitch': 2, 'ankle_roll': 8,
            # 'l_shoulder_pitch': 2.575, 'l_elbow_pitch': 3.1,
        }
        # action scale: target angle = actionScale * action + defaultAngle
        action_scale = 0.25
        # decimation: Number of control action updates @ sim DT per policy DT
        decimation = 10

    class terrain(GR1RoughCfg.terrain):
        mesh_type = 'plane'
        measure_heights = False

    class asset(GR1RoughCfg.asset):
        file = '{LEGGED_GYM_ROOT_DIR}/resources/robots/gr1t1/urdf/GR1T1_6DoF.urdf'
        foot_name = "foot_roll"
        knee_name = "shank"
        penalize_contacts_on = ["shoulder", "elbow", "thigh"]
        terminate_after_contacts_on = ["base", "waist"]
        self_collisions = 0  # 1 to disable, 0 to enable...bitwise filter

    class domain_rand:
        randomize_friction = False
        friction_range = [0.25, 1.75]
        randomize_base_mass = False
        added_mass_range = [-1., 1.]
        push_robots = False
        push_interval_s = 15
        max_push_vel_xy = 1.0
        randomize_gains = False
        stiffness_multiplier_range = [0.9, 1.1]
        damping_multiplier_range = [0.9, 1.1]

    class normalization:
        class obs_scales:
            lin_vel = 2.0
            lin_vel = 2.0
            ang_vel = 0.25
            dof_pos = 1.0
            dof_vel = 0.05
            imu = 0.5
            height_measurements = 5.0
        clip_observations = 50.
        clip_actions = 5.

    class noise:
        add_noise = False
        noise_level = 1.0  # scales other values

        class noise_scales:
            dof_pos = 0.03
            dof_vel = 1.5
            lin_vel = 0.1
            ang_vel = 0.3
            gravity = 0.05
            imu = 0.2
            height_measurements = 0.1

    class rewards(GR1RoughCfg.rewards):
        soft_dof_pos_limit = 0.95
        base_height_target = 0.25


        class scales:
            # reference motion tracking
            # joint_pos = 1.6
            # feet_clearance = 1.
            # feet_contact_number = 1.2
            # gait
            # feet_air_time = 1.
            # foot_slip = -0.05
            # feet_distance = 0.2
            # knee_distance = 0.2
            # contact
            # feet_contact_forces = -0.01
            # vel tracking
            tracking_lin_vel = 1.2
            tracking_ang_vel = 1.1
            vel_mismatch_exp = 0.5  # lin_z; ang x,y
            low_speed = 0.2
            track_vel_hard = 0.5
            # base pos
            default_joint_pos = 1.6
            # default_joint_roll_pos = 0.8
            orientation = 2.
            # base_height = 0.2
            base_acc = 0.2
            # energy
            action_smoothness = -0.002
            torques = -1e-5
            dof_vel = -5e-4
            dof_acc = -1e-7
            collision = -1.

    class commands:
        curriculum = False
        max_curriculum = 1.
        num_commands = 4  # default: lin_vel_x, lin_vel_y, ang_vel_yaw, heading (in heading mode ang_vel_yaw is recomputed from heading error)
        resampling_time = 10.  # time before command are changed[s]
        heading_command = False  # if true: compute ang vel command from heading error

        class ranges:
            lin_vel_x = [-0.6, 1.0]  # min max [m/s]
            lin_vel_y = [-0.3, 0.3]  # min max [m/s]
            ang_vel_yaw = [-1.57, 1.57]  # min max [rad/s]
            heading = [-3.14, 3.14]

    class sim:
        dt =  0.001
        substeps = 1
        gravity = [0., 0. ,-9.81]  # [m/s^2]
        up_axis = 1  # 0 is y, 1 is z

        class physx:
            num_threads = 10
            solver_type = 1  # 0: pgs, 1: tgs
            num_position_iterations = 4
            num_velocity_iterations = 0
            contact_offset = 0.01  # [m]
            rest_offset = 0.0   # [m]
            bounce_threshold_velocity = 0.1 #0.5 [m/s]
            max_depenetration_velocity = 1.0
            max_gpu_contact_pairs = 2**23 #2**24 -> needed for 8000 envs and more
            default_buffer_size_multiplier = 5
            contact_collection = 2 # 0: never, 1: last sub-step, 2: all sub-steps (default=2)


class GR1AMPCfgPPO(GR1RoughCfgPPO):
    runner_class_name = 'AMPOnPolicyRunner'

    class policy:
        init_noise_std = 1.0
        actor_hidden_dims = [512, 256, 128]
        critic_hidden_dims = [512, 256, 128]
        activation = 'elu' # can be elu, relu, selu, crelu, lrelu, tanh, sigmoid

    class algorithm(GR1RoughCfgPPO.algorithm):
        entropy_coef = 0.01
        amp_replay_buffer_size = 10000
        num_learning_epochs = 5
        num_mini_batches = 4
        learning_rate = 1.e-5  # 5.e-4

    class runner(GR1RoughCfgPPO.runner):
        run_name = ''
        experiment_name = 'gr1_amp_example'
        algorithm_class_name = 'AMPPPO'
        policy_class_name = 'ActorCritic'
        max_iterations = 3000  # number of policy updates
        num_steps_per_env = 60  # per iteration
        amp_reward_coef = 4.0
        amp_motion_files = MOTION_FILES
        amp_num_preload_transitions = 50000
        amp_task_reward_lerp = 0.8
        amp_discr_hidden_dims = [1024, 512]

        min_normalized_std = [0.5, 0.5, 0.6, 0.6, 0.3, 0.2] * 2
