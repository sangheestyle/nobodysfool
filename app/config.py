import os.path
import json


class Config:
    GITHUB_ID = None
    GITHUB_TOKEN = None
    with open('github_account.json') as fp:
        data = json.load(fp)
        GITHUB_ID = data['github_id']
        GITHUB_TOKEN = data['github_token']


config = {'default': Config}
