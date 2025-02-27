from typing import Dict, List, Optional
import rerun as rr
import cv2
import numpy as np
import pandas as pd

from src.core.data_types import VisualizationConfig, VideoFrame
from core.video import VideoSource
from data_io.readers import AudioDataReader, CSVReader
from utils.helpers import get_synchronized_frame
from vis.lists import *


class DataVisualizer:
    """Handles visualization of multi-modal participant data."""

    def __init__(self, config: VisualizationConfig):
        """Initialize visualizer with configuration."""
        # Store configuration
        self.config = config

        # Set up data paths
        self.video_cam1 = config.data_path / "video_cam1.mp4"
        self.video_cam2 = config.data_path / "video_cam2.mp4"

        # Check video availability
        self.video_cam2_found = self.video_cam2.is_file() if self.video_cam2 else False
        if not self.video_cam2_found:
            print(f"Warning: Video 2 not found at: {self.video_cam2}")

        # Load CSV data files
        self._load_data_files(config.data_path)

        # Initialize caches
        self.image_cache = {}

        # Set up Rerun visualization
        self._setup_rerun()

    def _load_data_files(self, data_path):
        """
        Load all data files from the data path.

        Args:
            data_path (Path): Path to the data directory
        """
        # Load analysis data - convert to records for sequential access
        analysis_df = CSVReader(data_path / "analysis.csv").read()
        self.analysis = analysis_df.to_dict('records') if not analysis_df.empty else []

        # Load data files
        self.times = CSVReader(data_path / "time.csv").read().set_index('Frame')
        self.openface = CSVReader(data_path / "openface.csv").read().set_index('frame')
        self.speech = AudioDataReader(data_path / "speech.csv").read()
        self.gaze = CSVReader(data_path / "gaze.csv").read()
        self.body = CSVReader(data_path / "body.csv").read()
        self.hume = CSVReader(data_path / "hume.csv").read()
        self.facetorch = CSVReader(data_path / "facetorch.csv").read()

    def _setup_rerun(self) -> None:
        """Configure rerun visualization settings."""
        if self.config.face_3d:
            rr.log("Face3D", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)
        if self.config.body_3d:
            rr.log("Body3D", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)

        # Create keypoint annotation information for each landmark
        keypoint_annotations = [
            rr.AnnotationInfo(id=landmark.value)
            for landmark in CustomPoseLandmark
        ]

        # Filter pose connections to include only body keypoints (indices 11-24)
        pose_connections = [
            connection for connection in POSE_CONNECTIONS
            if 11 <= connection[0] <= 24 and 11 <= connection[1] <= 24
        ]

        # Log annotation context with class description
        rr.log(
            "/",
            rr.AnnotationContext(
                rr.ClassDescription(
                    info=rr.AnnotationInfo(id=1),
                    keypoint_annotations=keypoint_annotations,
                    keypoint_connections=pose_connections
                )
            ),
            static=True,
        )

    def log_and_visualize(self):
        """Process and visualize video data from cameras."""
        # Use single camera mode if second camera not found
        if not self.video_cam2_found:
            self._process_single_camera()
            return

        with VideoSource(self.video_cam1) as video_source1, \
                VideoSource(self.video_cam2) as video_source2:

            for frame1 in video_source1.stream_bgr():
                # Adjust frame ID to match expected data indexing
                frame1.id_ += 1

                # Exit loop if we've reached the maximum frames
                if frame1.id_ > self.config.max_frames:
                    break

                # Get corresponding frame from camera 2 with appropriate skipping
                frame2 = get_synchronized_frame(video_source2, frame1.id_)

                # Log data for this frame pair
                self.log_frame_data(frame1, frame2)

    def _process_single_camera(self):
        """Process and visualize data from the primary camera only."""
        print("Processing with single camera mode")

        with VideoSource(self.video_cam1) as video:
            for frame in video.stream_bgr():
                # Adjust frame ID to match expected data indexing
                frame.id_ += 1

                # Exit loop if we've reached the maximum frames
                if frame.id_ > self.config.max_frames:
                    break

                # Log data for this frame
                self.log_frame_data(frame)

    def log_frame_data(self, frame1: VideoFrame, frame2: VideoFrame = None) -> None:
        """Log data for a single frame across all modalities."""
        rr.set_time_sequence("frame", frame1.id_)

        try:
            time_in_secs = self.times.loc[frame1.id_, 'Seconds']
            rr.set_time_seconds("time", time_in_secs)
        except KeyError:
            time_in_secs = -1.0

        rgb = cv2.cvtColor(frame1.data, cv2.COLOR_BGR2RGB)
        rr.log("video/image",
               rr.Image(rgb).compress(jpeg_quality=self.config.jpeg_quality))
        height, width, _ = rgb.shape

        if frame2 and frame2.data is not None:
            rgb = cv2.cvtColor(frame2.data, cv2.COLOR_BGR2RGB)
            rr.log("cam2/image",
                   rr.Image(rgb).compress(jpeg_quality=self.config.jpeg_quality))

        # Log various data modalities
        self._log_failure(frame1.id_)
        self._log_transcript(time_in_secs)
        self._log_face_and_gaze(frame1.id_)
        self._log_gaze_classification(frame1.id_)
        self._log_body_pose(frame1.id_, height, width)
        self._log_valence_arousal(frame1.id_)
        self._log_hume_data(frame1.id_)

    def _log_failure(self, frame):
        """
        Log failure information based on current frame.

        Args:
            frame (float): Current frame number
        """

        def log_no_failure():
            """Display the 'No Failure' message and empty image."""
            rr.log("Failure", rr.TextDocument("# No Failure", media_type=rr.MediaType.MARKDOWN))
            image_ = get_failure_image(f"visuals/empty.png")
            if image_ is not None:
                rr.log("description", rr.Image(image_).compress(jpeg_quality=15))

        def get_failure_image(image_path):
            if image_path in self.image_cache:  # Use cached image if available
                img = self.image_cache[image_path]
            else:
                try:
                    img = cv2.imread(image_path)
                    if img is not None:
                        self.image_cache[image_path] = img  # Cache the image for future use
                    else:  # Fall back to empty image
                        fallback_path = "visuals/empty.png"
                        if fallback_path not in self.image_cache:
                            fallback_image = cv2.imread(fallback_path)
                            if fallback_image is not None:
                                self.image_cache[fallback_path] = fallback_image
                        img = self.image_cache.get(fallback_path)
                except Exception as e:
                    return
            return img

        # If no analysis data
        if not self.analysis:
            log_no_failure()
            return

        # Get current phase
        current_phase = self.analysis[0]

        # Check if we've passed the current phase
        if frame > current_phase['End Frame']:
            # Remove the current phase and move to the next one
            self.analysis.pop(0)

            if not self.analysis:
                self._log_no_failure()
                return

            current_phase = self.analysis[0]

        # Check if we're within the current phase's time range
        if current_phase['Start Frame'] <= frame <= current_phase['End Frame']:
            # Log failure details
            round_num = current_phase['Round No.']
            action = current_phase['Action']
            state = current_phase['State']

            text = f"# {action} Failure at Round {round_num} - Phase: {state}"
            rr.log("Failure", rr.TextDocument(text, media_type=rr.MediaType.MARKDOWN))

            # Determine which image to show
            is_explanation_or_resolution = state in ["Explanation", "Resolution"]
            chosen = "1" if is_explanation_or_resolution else ""
            image_name = f"{action.lower()}{chosen}"

            # Load and log the appropriate image
            image = get_failure_image(f"visuals/{image_name}.png")
            if image is not None:
                rr.log("description", rr.Image(image).compress(jpeg_quality=20))
        else:
            log_no_failure()

    def _log_transcript(self, frame_time):
        """
        Log transcript and speech emotions for the current frame time.

        Args:
            frame_time (float): Current time in seconds
        """

        def clear_speech_displays():
            """Clear transcript and speech emotion displays."""
            rr.log("Transcript", rr.Clear(recursive=True))
            rr.log("Speech", rr.Clear(recursive=True))

        # Early return if no speech data or frame time is invalid
        if not self.speech or frame_time < 0:
            return

        # Process current speech segment
        current_speech = self.speech[0]

        # If we've passed the current speech segment, remove it and get the next one
        if frame_time > current_speech['end']:
            self.speech.pop(0)

            # If no more speech segments, clear displays and return
            if not self.speech:
                clear_speech_displays()
                return

            # Update to the next speech segment
            current_speech = self.speech[0]

        # Check if we're within the current speech segment's time range
        if current_speech['begin'] <= frame_time <= current_speech['end']:
            # Format and log the transcript
            speaker = current_speech['speaker']
            text = f"### {current_speech['text']} \n ({speaker})"
            rr.log("Transcript", rr.TextDocument(text, media_type=rr.MediaType.MARKDOWN))

            # Log all emotion values
            for emotion in speech_emotions:
                rr.log(f"Speech/{emotion}", rr.Scalar(current_speech[emotion]))
        else:
            # We're not in any active speech segment, clear displays
            clear_speech_displays()

    def _log_face_and_gaze(self, frame):
        """
        Log face and eye gaze data for the current frame.

        Args:
            frame (int): The current frame number
        """

        def clear_face_and_gaze_logs():
            """Clear all face and gaze visualizations."""
            log_paths = ["video/gaze", "video/face"]

            if self.config.gaze_3d:
                log_paths.append("Gaze3D")

            if self.config.face_3d:
                log_paths.append("Face3D")

            for path in log_paths:
                rr.log(path, rr.Clear(recursive=True))

        # Check if data exists for this frame
        if frame not in self.openface.index:
            clear_face_and_gaze_logs()
            return

        # Get data for this frame using the index
        frame_data = self.openface.loc[frame]

        # Handle case where we might have multiple faces for the same frame
        if isinstance(frame_data, pd.DataFrame):  # Multiple rows for the same frame
            if 'confidence' in frame_data.columns:  # Find the face with highest confidence
                frame_data = frame_data.loc[frame_data['confidence'].idxmax()]
            else:  # If no confidence column, just take the first one
                frame_data = frame_data.iloc[0]

        # Check if face detection was successful and confidence threshold is met
        success = False
        confidence = 0.0

        # Get success value
        if 'success' in frame_data.index:
            success_value = frame_data['success']
            if isinstance(success_value, (pd.Series, pd.DataFrame)):
                success_value = success_value.iloc[0]  # Get scalar value
            success = bool(int(success_value))

        # Get confidence value as scalar
        if 'confidence' in frame_data.index:
            confidence_value = frame_data['confidence']
            if isinstance(confidence_value, (pd.Series, pd.DataFrame)):
                confidence_value = confidence_value.iloc[0]  # Get scalar value
            confidence = float(confidence_value)

        # Check if success is True and confidence meets threshold
        if not success or confidence < self.config.openface_confidence:
            clear_face_and_gaze_logs()
            return

        # Extract and log 2D face landmarks
        if 'x_0' in frame_data:
            try:
                # Extract face landmark coordinates
                face_x = [frame_data[f'x_{i}'] for i in range(68) if f'x_{i}' in frame_data]
                face_y = [frame_data[f'y_{i}'] for i in range(68) if f'y_{i}' in frame_data]

                if face_x and face_y:
                    face_pairs = list(zip(face_x, face_y))
                    rr.log("video/face", rr.Points2D(face_pairs))
            except Exception as e:
                print(f"Error logging 2D face data: {e}")
                rr.log("video/face", rr.Clear(recursive=True))

        # Extract and log 2D gaze data
        try:
            if 'gaze_0_x' in frame_data and 'gaze_0_y' in frame_data:
                gaze_x = [frame_data['gaze_0_x'], frame_data['gaze_1_x']]
                gaze_y = [frame_data['gaze_0_y'], frame_data['gaze_1_y']]
                eye_gaze_pairs = list(zip(gaze_x, gaze_y))
                rr.log("video/gaze", rr.Points2D(eye_gaze_pairs))
        except Exception as e:
            print(f"Error logging 2D eye gaze data: {e}")
            rr.log("video/gaze", rr.Clear(recursive=True))

            # Filter for current frame
            frame_data = self.gaze[self.gaze['Frame'] == frame]

        # Log 3D face data if configured
        if self.config.face_3d:
            try:
                if 'X_0' in frame_data:
                    face_x = [frame_data[f'X_{i}'] for i in range(68) if f'X_{i}' in frame_data]
                    face_y = [frame_data[f'Y_{i}'] for i in range(68) if f'Y_{i}' in frame_data]
                    face_z = [frame_data[f'Z_{i}'] for i in range(68) if f'Z_{i}' in frame_data]

                    if face_x and face_y and face_z:
                        face_points = list(zip(face_x, face_y, face_z))
                        rr.log("Face3D", rr.Points3D(face_points))
            except Exception as e:
                print(f"Error logging 3D face data: {e}")
                rr.log("Face3D", rr.Clear(recursive=True))

        # Log 3D gaze data if configured
        if self.config.gaze_3d:
            try:
                if 'gaze_0_x' in frame_data and 'gaze_0_y' in frame_data and 'gaze_0_z' in frame_data:
                    gaze_x = [frame_data['gaze_0_x'], frame_data['gaze_1_x']]
                    gaze_y = [frame_data['gaze_0_y'], frame_data['gaze_1_y']]
                    gaze_z = [frame_data['gaze_0_z'], frame_data['gaze_1_z']]
                    eye_gaze_points = list(zip(gaze_x, gaze_y, gaze_z))
                    rr.log("Gaze3D", rr.Points3D(eye_gaze_points))
            except Exception as e:
                print(f"Error logging 3D eye gaze data: {e}")
                rr.log("Gaze3D", rr.Clear(recursive=True))

    def _log_gaze_classification(self, frame):
        """
        Log gaze classification data for the current frame.

        Args:
            frame (int): The current frame number
        """
        # Check if we have the gaze classification DataFrame
        if not hasattr(self, 'gaze') or self.gaze is None or self.gaze.empty:
            return

        # Filter for current frame
        frame_data = self.gaze[self.gaze['Frame'] == frame]

        if not frame_data.empty:
            # Get gaze classification text
            gaze_text = frame_data.iloc[0]['Gaze']

            # Format and log the text
            text = f"# {gaze_text}"
            rr.log("Gaze", rr.TextDocument(text, media_type=rr.MediaType.MARKDOWN))
        else:
            # Clear visualization if no data for this frame
            text = "Empty (Only on Failure Phases)"
            rr.log("Gaze", rr.TextDocument(text, media_type=rr.MediaType.MARKDOWN))

    def _log_body_pose(self, frame, height, width):
        """
        Log body pose data for the current frame.

        Args:
            frame (int): The current frame number
        """

        def clear_body_logs():
            """Clear all body pose visualizations."""
            log_paths = ["video/body"]

            if self.config.body_3d:
                log_paths.append("Body3D")

            for path in log_paths:
                rr.log(path, rr.Clear(recursive=True))

        # Check if we have body data for this frame
        body_data = self.body[self.body['Frame'] == frame]

        if body_data.empty:
            clear_body_logs()
            return

        # Get the first row of data for this frame
        row = body_data.iloc[0]

        # Check if we have valid keypoints (checking if shoulder keypoint exists)
        if pd.isna(row['11_x']) or pd.isna(row['11_y']):
            clear_body_logs()
            return

        # Extract 2D keypoints
        keypoints_x = []
        keypoints_y = []

        # Loop through body keypoints (11-24)
        for i in range(11, 25):
            x_col = f'{i}_x'
            y_col = f'{i}_y'
            vis_col = f'{i}_visibility'

            if x_col in row.index and y_col in row.index:
                # VISIBILITY OPTION: Only include points with good visibility if that data is available
                # visibility = row[vis_col] if vis_col in row.index else 1.0

                if not pd.isna(row[x_col]) and not pd.isna(row[y_col]):  # can be added: visibility > 0.5
                    keypoints_x.append(float(width * row[x_col]))
                    keypoints_y.append(float(height * row[y_col]))

        keypoint_pairs = [(x, y) for x, y in zip(keypoints_x, keypoints_y) if x is not None and y is not None]

        if keypoint_pairs:
            rr.log(
                "video/body",
                rr.Points2D(keypoint_pairs, class_ids=1, keypoint_ids=CustomPoseLandmark, radii=5, labels=None),
            )

        # Log 3D pose if selected
        if self.config.body_3d:
            if any(col for col in row.index if '_3d_' in col):
                keypoints_x = []
                keypoints_y = []
                keypoints_z = []

                for i in range(25):
                    x_col = f'{i}_3d_x'
                    y_col = f'{i}_3d_y'
                    z_col = f'{i}_3d_z'

                    if x_col in row.index and y_col in row.index and z_col in row.index:
                        if not pd.isna(row[x_col]) and not pd.isna(row[y_col]) and not pd.isna(row[z_col]):
                            keypoints_x.append(float(row[x_col]))
                            keypoints_y.append(float(row[y_col]))
                            keypoints_z.append(float(row[z_col]))
                        else:
                            keypoints_x.append(None)
                            keypoints_y.append(None)
                            keypoints_z.append(None)

                keypoint_pairs_3d = [(x, y, z) for x, y, z in zip(keypoints_x, keypoints_y, keypoints_z)
                                     if x is not None and y is not None and z is not None]

                if keypoint_pairs_3d:
                    rr.log(
                        "Body3D",
                        rr.Points3D(keypoint_pairs_3d, radii=5),
                    )

        # Log body pose classification
        text = "# Unknown"
        if 'Crossed Arms' in row and row['Crossed Arms']:
            text = "# Crossed Arms"
        elif 'Arms behind back' in row and row['Arms behind back']:
            text = "# Arms Behind Back"

        rr.log("body", rr.TextDocument(text, media_type=rr.MediaType.MARKDOWN))

    def _log_valence_arousal(self, frame):
        """
        Log valence and arousal data for the current frame.

        Args:
            frame (int): The current frame number
        """
        # Check if we have the FaceTorch DataFrame
        if not hasattr(self, 'facetorch') or self.facetorch is None or self.facetorch.empty:
            return

        # Filter for current frame
        frame_data = self.facetorch[self.facetorch['Frame ID'] == frame]

        if not frame_data.empty:
            # Get valence and arousal values
            try:
                valence = float(frame_data.iloc[0]['Valence'])
                arousal = float(frame_data.iloc[0]['Arousal'])

                # Log the valence/arousal values
                rr.log("Affect/Valence", rr.Scalar(valence))
                rr.log("Affect/Arousal", rr.Scalar(arousal))

                # Optionally log the emotion label if available
                # if 'FER Label' in frame_data.columns:
                #     emotion = frame_data.iloc[0]['FER Label']
                #     if emotion and not pd.isna(emotion):
                #         rr.log("Affect/Emotion", rr.TextDocument(f"# {emotion}",
                #                                                  media_type=rr.MediaType.MARKDOWN))
            except (ValueError, KeyError, TypeError) as e:
                rr.log("Affect", rr.Clear(recursive=True))
        else:
            # Clear visualization if no data for this frame
            rr.log("Affect", rr.Clear(recursive=True))

    def _log_hume_data(self, frame):
        """
        Log Hume emotion detection data for the current frame.

        Args:
            frame (int): The current frame number
        """

        def clear_hume_logs():
            """Clear all Hume data visualizations."""
            log_paths = ["Positive", "Negative", "AUs", "video/box"]

            for path in log_paths:
                rr.log(path, rr.Clear(recursive=True))

        # Check if we have the Hume DataFrame
        if not hasattr(self, 'hume') or self.hume is None or self.hume.empty:
            return

        # Filter for current frame
        frame_data = self.hume[self.hume['Frame'] == frame]

        if not frame_data.empty and not pd.isna(frame_data.iloc[0]['x']):
            # Get first row of data for this frame
            row = frame_data.iloc[0]

            try:
                # Log bounding box
                box = np.array([[row['x'], row['y'], row['w'], row['h']]], dtype=float)
                rr.log(
                    "video/box",
                    rr.Boxes2D(array=box, array_format=rr.Box2DFormat.XYWH),
                )

                # Log positive emotions
                for emotion in positive_emotions:
                    if emotion in row:
                        rr.log(f"Positive/{emotion}", rr.Scalar(float(row[emotion])))

                # Log negative emotions
                for emotion in negative_emotions:
                    if emotion in row:
                        rr.log(f"Negative/{emotion}", rr.Scalar(float(row[emotion])))

                # Log action units
                for au in aus:
                    if au in row:
                        au_name = au.replace(" ", "")
                        rr.log(f"AUs/{au_name}", rr.Scalar(float(row[au])))

            except (ValueError, KeyError, TypeError) as e:
                clear_hume_logs()
        else:
            # Clear visualizations if no data for this frame
            clear_hume_logs()
