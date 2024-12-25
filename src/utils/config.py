import json

class Config:

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):

        if hasattr(self, "data"):
            return  # Ensure init is only run once

        self.file_path = "config.json"
        self.data = {}
        self.load()

    def save(self):
        """Save the current configuration to a JSON file."""
        with open(self.file_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        """Load configuration from a JSON file."""
        try:
            with open(self.file_path, "r") as f:
                self.data.update(json.load(f))
        except FileNotFoundError:
            pass

    def update(self, config):
        """
        Update configuration values and save changes.
        :param config: Dictionary of values to update.
        """
        self.data = config
        self.save()

    def chunk_size(self):
        return self.data.get("chunk_size")

    def sample_rate(self):
        return self.data.get("sample_rate")

    def threshold(self):
        return self.data.get("threshold")

    def bands(self):
        return self.data.get("bands")

config = Config()