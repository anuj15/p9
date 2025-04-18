import os
from pathlib import Path

import yaml


class ConfigManager:

    def __init__(self):
        root_dir = Path(__file__).resolve().parents[1]
        config_file_path = os.path.join(root_dir, "config.yml")
        with open(config_file_path) as f:
            self.data = yaml.safe_load(f)

    def get(self, key):
        env = self.data["environment"]
        env_config = self.data[env]
        return env_config.get(key, self.data.get(key))
