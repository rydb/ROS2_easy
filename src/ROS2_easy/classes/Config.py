from dataclasses import dataclass
from typing import Optional

@dataclass
class Config():
    """A ros2 package's config information"""

    config_file_name: Optional[str] = None
    """name of configuration file for this configuration"""