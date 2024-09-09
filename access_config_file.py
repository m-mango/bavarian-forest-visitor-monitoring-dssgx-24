import toml
import os

def get_aws_credentials():

    with open(os.path.join('config','aws_profile.toml'), 'r') as f:
        config = toml.load(f)
    
    # get the aws profile
    aws_profile = config['profile']['name']
    return aws_profile
