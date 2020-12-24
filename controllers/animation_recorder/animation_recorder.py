#!/usr/bin/env python3
#
# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from controller import Supervisor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=float, default=10, help='Duration of the animation in seconds')
    parser.add_argument('--output', default='../../animation/index.html', help='Path at which the animation will be saved')
    args = parser.parse_args()

    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    receiver = robot.getDevice('receiver')
    receiver.enable(timestep)

    robot.step(timestep)
    robot.animationStartRecording(args.output)

    step_i = 0
    done = False
    n_steps = (1000 * args.duration) / robot.getBasicTimeStep()
    while not done and robot.step(timestep) != -1 and step_i < n_steps:
        step_i += 1
        if receiver.getQueueLength() > 0:
            if receiver.getData().decode('utf-8') == 'done':
                done = True
            receiver.nextPacket()

    robot.animationStopRecording()
    for _ in range(10):
        robot.step(timestep)
    print('The animation is saved')
    robot.simulationQuit(0)


if __name__ == '__main__':
    main()
