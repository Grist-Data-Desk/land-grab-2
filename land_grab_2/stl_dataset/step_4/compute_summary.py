import os

from land_grab_2.stl_dataset.step_1.build_dataset import calculate_summary_statistics


def run():
    print('Running: calculate_summary_statistics')
    required_envs = ['DATA']
    missing_envs = [env for env in required_envs if os.environ.get(env) is None]
    if any(missing_envs):
        raise Exception(f'RequiredEnvVar: The following ENV vars must be set. {missing_envs}')

    calculate_summary_statistics()


if __name__ == '__main__':
    run()
