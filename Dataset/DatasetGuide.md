# REFLEX Dataset Guide

This guide provides detailed information about the REFLEX dataset, including its structure, contents, and how to access and visualize the data.

## Dataset Overview

The REFLEX dataset collects human behavioral reactions to robotic failures during a collaborative task. The data was recorded from a user study and has been processed for anonymization. This comprehensive multimodal dataset captures human responses to both robot failures and the explanations provided for these failures.

The dataset is available on Zenodo: [https://zenodo.org/records/14160783](https://zenodo.org/records/14160783)

## Experimental Setup

In the Human-Robot Collaboration (HRC) task:
- Users placed objects on a table in front of the robot
- The robot would pick up objects, carry and place them on a shelf
- Users interacted with the robot in four rounds, with four objects per round
- Pre-programmed 11 robotic failures occurred during the Pick, Carry, and Place actions
- Upon failure, the robot provided explanations according to one of five different explanation strategies
- The experiment was recorded using two cameras:
  - Camera 1: Focused on both the user and the robot
  - Camera 2: Placed on the robot's torso, focused solely on the user

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

### Notes

- The `hume.csv` and `gaze.csv` files contain data only for frames within failure periods.

## Data Collection and Processing

- Data was sampled at a frequency of 4.4 Hz based on the video frame rate
- All participant faces were anonymized using black masks created with MediaPipe Pose Landmark detection
- Failure events were divided into four phases:
  1. Pre-failure phase: Period before the failure occurs
  2. Failure phase: When the actual failure action takes place
  3. Explanation phase: When the robot provides an explanation for the failure
  4. Resolution phase: When the robot guides the participant to resolve the issue

## Visualization Tool

The repository includes a visualization tool built using [Rerun](https://www.rerun.io/), an open-source visualization tool for multimodal data.

### Installation

Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Visualization Tool

Basic usage:
```bash
python main.py --participant C1-1
```

This command visualizes data from the first participant under the Fixed-Low (C1) strategy.



# About Dataset

This dataset collects human behavioral reactions to robotic failures. This data was recorded from a user study and has been processed for anonymization.

https://zenodo.org/records/14160783

## About Data 

This description gives a detailed process on how the data was collected. It should describe the conditions under which the data was recorded and also the devices used to record the data.

### Data Organisation

The data is structured by strategy and participant, as shown below:
```
Strategy Dir/
  -Participant Dir/
    - analysis
    - facetorch
    - openface
    - gaze
    - hume
    - body
    - speech
    - time
```
We employed five different strategies (C1, C2, C3, D1, D2), collecting data from 11 participants for each strategy. The data for each participant is organized within a corresponding folder.

Participants are labeled based on their assigned strategy. For example, data from the first participant under the “Fixed Low” (C1) strategy can be found in the C1-1 subfolder within the C1 directory.

### Collected Data 

Each participant folder contains various datasets related to different modalities, outlined below:

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

---
