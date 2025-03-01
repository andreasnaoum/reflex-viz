from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict


@dataclass
class Settings:
    """Global settings for the visualization package."""

    data_root: Path
    output_dir: Path
    max_frames: int = 1800
    jpeg_quality: int = 15
    debug_mode: bool = False

    @classmethod
    def from_dict(cls, config_dict: Dict) -> 'Settings':
        """Create Settings instance from dictionary."""
        return cls(
            data_root=Path(config_dict['data_root']),
            output_dir=Path(config_dict['output_dir']),
            max_frames=config_dict.get('max_frames', 1800),
            jpeg_quality=config_dict.get('jpeg_quality', 15),
            debug_mode=config_dict.get('debug_mode', False)
        )
