#!/usr/bin/env python3
import argparse
from pathlib import Path
import rerun as rr
import rerun.blueprint as rrb
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.data_types import VisualizationConfig
from vis.visualizer import DataVisualizer
from utils.helpers import validate_participant_code, get_participant_folder
from vis.layouts import create_default_rrb


def main():
    """Main entry point for the visualization."""
    parser = argparse.ArgumentParser(description="REFLEX Dataset - Rerun Visualization")
    parser.add_argument("--participant", type=str, required=True,
                        help="Participant code/ Folder Name (e.g., 'C1-1')")
    parser.add_argument("--max-frames", type=int, default=18000,
                        help="Maximum number of frames to process")
    parser.add_argument("--jpeg-quality", type=int, default=15,
                        help="JPEG compression quality for images (1-100)")
    parser.add_argument("--data-path", type=Path, default=None,
                        help="Path to the data directory (optional)")
    parser.add_argument("--face-3d", action="store_true",
                        help="Enable 3D face visualization")
    parser.add_argument("--gaze-3d", action="store_true",
                        help="Enable 3D gaze visualization")
    parser.add_argument("--body-3d", action="store_true",
                        help="Enable 3D body visualization")
    parser.add_argument("--openface-confidence", type=float, default=0.7,
                        help="Minimum confidence threshold for OpenFace data (0.0-1.0)")
    rr.script_add_args(parser)
    args = parser.parse_args()

    # Validate participant code and get data path
    if not validate_participant_code(args.participant):
        raise ValueError(f"Invalid participant code: {args.participant}")

    data_path = get_participant_folder(args.participant)
    if not data_path:
        raise ValueError(f"Could not find data for participant: {args.participant}")

    # Process video and associated data
    video_cam1 = data_path / "video_cam1.mp4"
    if not video_cam1:
        raise ValueError(f"Error: Video 1 not found or is not a file at: {video_cam1}")

    rr.script_teardown(args)
    default_blueprint = create_default_rrb()
    rr.script_setup(args, f"Participant-{args.participant}", default_blueprint)

    config = VisualizationConfig(
        participant_code=args.participant,
        data_path=data_path,
        max_frames=args.max_frames,
        jpeg_quality=args.jpeg_quality,
        face_3d=args.face_3d,
        gaze_3d=args.gaze_3d,
        body_3d=args.body_3d,
        openface_confidence=args.openface_confidence
    )

    visualizer = DataVisualizer(config)
    visualizer.log_and_visualize()




if __name__ == "__main__":
    main()
