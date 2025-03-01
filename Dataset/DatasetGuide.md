<a href="https://zenodo.org/records/14160783"><img src="https://img.shields.io/badge/Zenodo-Dataset-green"></a> 
<a href="https://arxiv.org/abs/2502.14185"><img src="https://img.shields.io/badge/arXiv-Paper-red"></a>

# REFLEX Dataset Guide

This guide provides detailed information about the REFLEX dataset, including its structure, contents, and how to access and visualize the data.

## Dataset Overview

The REFLEX dataset collects human behavioral reactions to robotic failures during a collaborative task. The data was recorded from a user study and has been processed for anonymization. This comprehensive multimodal dataset captures human responses to both robot failures and the explanations provided for these failures.

The dataset is available on Zenodo: [https://zenodo.org/records/14160783](https://zenodo.org/records/14160783)

### Explanation Strategies

There are five different explanation strategies in the dataset:

| ID | Strategy | Round 1 | Round 2 | Round 3 | Round 4 |
|----|----------|---------|---------|---------|---------|
| C1 | Fixed-Low | Low | Low | Low | Low |
| C2 | Fixed-Medium | Medium | Medium | Medium | Medium |
| C3 | Fixed-High | High | High | High | High |
| D1 | Decay-Slow | High | Medium | Low | None |
| D2 | Decay-Rapid | High | Low | Low | Low |

### Explanation Levels

- **Zero Level (Non-verbal)**: The robot shakes its head and goes into a handover pose after each failure.
- **Low (Action-based)**: The robot states the failure and asks for help. For example: "I failed to pick up the object", "Hand it to me".
- **Medium (Context-based)**: The robot explains the failure cause and asks for help. For example: "I can't pick up the object because it doesn't fit in my gripper", "Can you hand it over to me".
- **High (Context + History-based)**: The robot mentions a previous success, explains the current failure and its cause, and asks for help. For example: "I can detect the object, but I can't pick it up because it doesn't fit in my gripper", "Can you hand it over to me by placing it in my gripper?".

### Participants

- The dataset includes data from 55 participants (11 per strategy)
- Participants had no prior experience with physical robot interaction
- Participant demographics: Age M=26.63, SD=7.42; 21 Female, 33 Male, 1 Other
- Participants are labeled based on their assigned strategy (e.g., C1-1 for the first participant under the C1 strategy)

## Data Organization

The data is structured by strategy and participant as follows:

```
Strategy_Dir/
  - Participant_Dir/
    - analysis.csv
    - facetorch.csv
    - openface.csv
    - gaze.csv
    - hume.csv
    - body.csv
    - speech.csv
    - time.csv
    - video_cam1.mp4
    - video_cam2.mp4
```

## Dataset Components

Each participant folder contains the following data files:

- **Analysis** (`analysis.csv`): Contains information about system failures, including:
  - Participant code
  - Failure type
  - Explanation level
  - Phase
  - Start and end frame of failure

- **Facetorch** (`facetorch.csv`) - [Facetorch](https://github.com/tomas-gajarsky/facetorch)
  - Arousal/Valence levels
  - Presence of Facial Action Units (AUs)
  - Dominant Emotion (Out of six basic emotions and neutral)

- **OpenFace** (`openface.csv`) - [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace)
  - Eye Gaze (2D and 3D Landmarks, Eye Direction)
  - Head Pose Estimation
  - Face Landmarks
  - Facial Action Units 

- **Gaze** (`gaze.csv`)
  - Eye Gaze Classification (e.g., Robot, Task, Miscellaneous)

- **Hume** (`hume.csv`) - [Hume Expression Measurement API](https://www.hume.ai)
  - 48 Emotion likelihoods
  - Facial Action Units (0-1 score)
  - Gesture Detection (0-1 score)

- **Voice** (`speech.csv`) - [Hume Expression Measurement API](https://www.hume.ai)
  - Speech conversation data
  - Emotional likelihoods inferred from prosody

- **Body** (`body.csv`) - [MediaPipe Pose Landmark Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
  - Pose classifications (e.g., crossed arms, arms behind back)
  - 2D and 3D Pose Landmarks

- **Videos** (`video_cam1.mp4`, `video_cam2.mp4`)
  - Cam1: Robot's view
  - Cam2: Side camera
  - All participant faces were anonymized using black masks created with MediaPipe Pose Landmark detection

### Notes

- Data was synchronized based on the `video_cam1.mp4`
- The `hume.csv` and `gaze.csv` files contain data only for frames within failure periods.
- Failure events were divided into four phases:
    1. Pre-failure phase: Period before the failure occurs
    2. Failure phase: When the actual failure action takes place
    3. Explanation phase: When the robot provides an explanation for the failure
    4. Resolution phase: When the robot guides the participant to resolve the issue
