from typing import Iterator, Union
import cv2
from pathlib import Path
from .data_types import VideoFrame


class VideoSource:
    """Handles video file reading and streaming."""

    def __init__(self, path: Union[str, Path]):
        """Initialize video capture from given path."""
        self.path = Path(path)
        self.capture = cv2.VideoCapture(str(self.path))
        if not self.capture.isOpened():
            raise ValueError(f"Failed to open video file: {self.path}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        """Release video capture resources."""
        if self.capture:
            self.capture.release()

    def stream_bgr(self) -> Iterator[VideoFrame]:
        """Stream video frames in BGR format."""
        while self.capture.isOpened():
            id_ = int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
            success, bgr = self.capture.read()

            if not success:
                break

            time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            yield VideoFrame(data=bgr, time=time_ms * 1e-3, id_=id_)

    def get_frame_count(self) -> int:
        """Get total number of frames in video."""
        return int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
