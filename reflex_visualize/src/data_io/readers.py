from typing import Dict, List, Optional, Union, Any
import csv
import json
import pandas as pd
import numpy as np
from pathlib import Path


class DataReader:
    """Base class for data readers."""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

    def read(self) -> Any:
        """Read and parse file data."""
        raise NotImplementedError


class CSVReader(DataReader):
    """CSV file reader with advanced parsing capabilities."""

    def __init__(self, file_path: Union[str, Path], encoding: str = 'utf-8'):
        super().__init__(file_path)
        self.encoding = encoding

    def read(self, **kwargs) -> pd.DataFrame:
        """Read CSV file into pandas DataFrame."""
        try:
            return pd.read_csv(self.file_path, encoding=self.encoding, **kwargs)
        except Exception as e:
            raise ValueError(f"Error reading CSV {self.file_path}: {str(e)}")


class AudioDataReader(CSVReader):
    """Specialized reader for audio data with emotion annotations."""

    def read(self) -> List[Dict]:
        """Read and parse audio data with emotion scores."""
        df = super().read()
        try:
            required_columns = ['Id', 'Text', 'BeginTime', 'EndTime']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Missing required columns: {required_columns}")

            return [{
                'speaker': row['Id'],
                'text': row['Text'],
                'begin': float(row['BeginTime']),
                'end': float(row['EndTime']),
                'Admiration': float(row['Admiration']),
                'Adoration': float(row['Adoration']),
                'Amusement': float(row['Amusement']),
                'Anger': float(row['Anger']),
                'Anxiety': float(row['Anxiety']),
                'Awe': float(row['Awe']),
                'Awkwardness': float(row['Awkwardness']),
                'Boredom': float(row['Boredom']),
            } for _, row in df.iterrows()]

        except Exception as e:
            raise ValueError(f"Error processing audio data: {str(e)}")


class EmotionReader(CSVReader):
    """Reader for emotion-related data files."""

    def read(self) -> Dict[str, List[str]]:
        """Read emotion data and return structured format."""
        df = super().read()
        return {
            'positive_emotions': df['positive_emotions'].tolist(),
            'negative_emotions': df['negative_emotions'].tolist(),
            'speech_emotions': df['speech_emotions'].tolist(),
            'action_units': df['action_units'].tolist()
        }


class BodyPoseReader(CSVReader):
    """Reader for body pose estimation data."""

    def read(self) -> Dict[int, Dict]:
        """Read body pose data indexed by frame."""
        df = super().read()
        return {
            row['frame']: {
                'keypoints': json.loads(row['keypoints']),
                'confidence': row['confidence'],
                'pose_classification': row['pose_classification']
            }
            for _, row in df.iterrows()
        }


class VideoReader(DataReader):
    """Reader for video files with metadata."""

    def read(self) -> Dict:
        """Read video metadata."""
        import cv2
        cap = cv2.VideoCapture(str(self.file_path))
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {self.file_path}")

        metadata = {
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'duration': float(cap.get(cv2.CAP_PROP_FRAME_COUNT) /
                              cap.get(cv2.CAP_PROP_FPS))
        }
        cap.release()
        return metadata
