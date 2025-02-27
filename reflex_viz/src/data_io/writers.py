from typing import Any, Dict, List, Union
from pathlib import Path
import csv
import json
import numpy as np
import pandas as pd


class DataWriter:
    """Base class for data writers."""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, data: Any) -> None:
        """Write data to file."""
        raise NotImplementedError


class CSVWriter(DataWriter):
    """CSV file writer with support for different data formats."""

    def write(self, data: Union[List[Dict], pd.DataFrame],
              index: bool = False) -> None:
        """Write data to CSV file."""
        if isinstance(data, pd.DataFrame):
            data.to_csv(self.file_path, index=index)
        else:
            if not data:
                raise ValueError("Empty data provided")

            fieldnames = data[0].keys()
            with open(self.file_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)


class VideoWriter(DataWriter):
    """Video file writer with compression options."""

    def __init__(self, file_path: Union[str, Path], fps: float = 30.0,
                 codec: str = 'mp4v'):
        super().__init__(file_path)
        self.fps = fps
        self.codec = codec
        self._writer = None

    def write(self, frames: List[np.ndarray]) -> None:
        """Write frames to video file."""
        import cv2

        if not frames:
            raise ValueError("No frames provided")

        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*self.codec)

        self._writer = cv2.VideoWriter(
            str(self.file_path), fourcc, self.fps, (width, height)
        )

        try:
            for frame in frames:
                self._writer.write(frame)
        finally:
            if self._writer:
                self._writer.release()
