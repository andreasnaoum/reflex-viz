from typing import Optional
from pathlib import Path
import re
import logging
import sys


def setup_logging(debug: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('reflex_viz.log')
        ]
    )


def configure_error_handling() -> None:
    """Configure global error handling."""

    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error("An unexpected error occurred:",
                      exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = global_exception_handler


def validate_participant_code(code: str) -> bool:
    """Validate participant code format."""
    pattern = r"^(C[1-3]|D[1-2])-([1-9]|1[0-1])$"
    return bool(re.match(pattern, code))


def get_participant_folder(code: str) -> Optional[Path]:
    """Get participant data folder path."""
    if not validate_participant_code(code):
        return None

    strategy = code[:2]
    strategy_folders = {
        "C1": "C1-Fixed-Low",
        "C2": "C2-Fixed-Medium",
        "C3": "C3-Fixed-High",
        "D1": "D1-Decay-Smooth",
        "D2": "D2-Decay-Rapid"
    }

    current_path = Path.cwd()
    origin_path = current_path.parent.parent
    return origin_path / 'Dataset' / strategy_folders[strategy] / code

    # return Path('Dataset') / strategy_folders[strategy] / code


def get_synchronized_frame(video_source, primary_frame_id):
    """
    Get a synchronized frame from the secondary camera.

    Applies appropriate frame skipping based on the primary frame ID.

    Args:
        video_source: VideoSource object for the secondary camera
        primary_frame_id: Frame ID from the primary camera

    Returns:
        VideoFrame or None if no frame is available
    """
    # Determine how many frames to skip based on the primary frame ID
    frames_to_skip = 4 if primary_frame_id % 3 == 0 else 3

    # Get the last frame after skipping the appropriate number
    frame2 = None
    for _ in range(frames_to_skip):
        next_frame = next(video_source.stream_bgr(), None)
        if next_frame is not None:
            frame2 = next_frame
        else:
            break

    return frame2
