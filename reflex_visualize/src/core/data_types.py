from dataclasses import dataclass
from typing import Dict, List, Optional
from pathlib import Path
import numpy.typing as npt

@dataclass
class VideoFrame:
    """Single frame from a video source with metadata."""
    data: npt.NDArray
    time: float
    id_: int

@dataclass
class VisualizationConfig:
    """Configuration parameters for visualization."""
    participant_code: str
    data_path: Optional[Path] = None
    max_frames: int = 18000
    jpeg_quality: int = 15
    face_3d: bool = False
    gaze_3d: bool = False
    body_3d: bool = False
    openface_confidence: float = 0.7

@dataclass
class EmotionData:
    """Container for emotion-related data."""
    positive_emotions: List[str]
    negative_emotions: List[str]
    speech_emotions: List[str]
    action_units: List[str]
