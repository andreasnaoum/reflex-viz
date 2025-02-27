"""Core functionality for video processing and data handling."""
from .data_types import VideoFrame, VisualizationConfig, EmotionData
from .video import VideoSource

__all__ = ['VideoFrame', 'VisualizationConfig', 'EmotionData', 'VideoSource']
