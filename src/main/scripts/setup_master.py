import os
import argparse
from shell_command import shell_call
from contextlib import contextmanager


@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    yield
    os.chdir(previous_dir)


def setup(config_file, deployment_id, ssh_key_file):
    with pushd(os.getcwd() + '/../gcloud'):
        mesos_marathon_setup_cmd = "python mesos_marathon_setup.py --config_file " + config_file + \
                                   " --deployment_id " + deployment_id + " --ssh_key_file " + ssh_key_file
        shell_call(mesos_marathon_setup_cmd)

        hydra_setup_cmd = "python hydra_setup_script.py --deployment_id " + deployment_id
        shell_call(hydra_setup_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to setup Mesos/Marathon cluster on Google Compute '
                                                 'Engine instances. It will also install Hydra on one of master nodes.')
    parser.add_argument('--config_file', '-f', type=str, default=os.getcwd() + "/setup_config.ini",
                        help='Absolute path of configuration file which dictates the number of master/slave nodes '
                             'along with their machine type. Default is ' + os.getcwd() + '/setup_config.ini .')
    parser.add_argument('--deployment_id', '-i', type=str,
                        help='Each cluster deployment needs to have a unique identifier. '
                             'This helps in creating multiple deployments in parallel.', required=True)
    parser.add_argument('--ssh_key_file', '-k', type=str, default=os.environ['HOME'] + "/.ssh/id_rsa.pub",
                        help='SSH public key absolute path. It would be used to get passwordless login to cloud '
                             'instances. Default is ~/.ssh/id_rsa.pub')
    # parser.add_argument('--cont', '-t', action='store_true',
    #                    help='If your script fails because of any reason in middle of somethhing, use this flag. '
    #                         'This flag will resume the script from failed step. ')
    parser.add_argument('--clean', '-c', action='store_true', help='cleanup instances')

    args = parser.parse_args()

    setup(args.config_file, args.deployment_id, args.ssh_key_file)
