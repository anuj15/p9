import logging
from pathlib import Path

from utils.config_manager import ConfigManager


class LogManager:

    def __init__(self):
        self.config = ConfigManager()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.config.get("log_level"))

        log_file = Path(__file__).resolve().parents[1] / self.config.get("log_file_path")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, mode='a+', encoding='utf-8')
        console_handler = logging.StreamHandler()

        log_format = logging.Formatter("%(asctime)s - %(message)s")
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        if not self.logger.hasHandlers():
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
