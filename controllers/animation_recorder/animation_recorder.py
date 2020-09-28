import argparse
from controller import Supervisor


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=float, default=10, help='Duration of the animation in seconds')
    parser.add_argument('--output', default='../../animation/index.html', help='Path at which the animation will be saved')
    args = parser.parse_args()

    robot = Supervisor()
    timestep = int(robot.getBasicTimeStep())
    robot.animationStartRecording(args.output)

    step_i = 0
    n_steps = (1000 * args.duration) / robot.getBasicTimeStep()
    while robot.step(timestep) != -1 and step_i < n_steps:
        step_i += 1

    robot.animationStopRecording()
    print('The animation is saved')
    robot.simulationQuit(0)

if __name__ == '__main__':
    main()
