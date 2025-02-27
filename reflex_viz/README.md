# About Dataset

This dataset collects human behavioral reactions to robotic failures. This data was recorded from a user study and has been processed for anonymization.
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
    - voice
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

- **Voice** (`voice.csv`) - [Hume Expression Measurement API](https://www.hume.ai)
  - Speech conversation data
  - Emotional likelihoods inferred from prosody

- **Body** (`body.csv`) - [MediaPipe Pose Landmark Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
  - Pose classifications (e.g., crossed arms, arms behind back)
  - 2D and 3D Pose Landmarks

---

### Notes

- The `hume.csv` and `gaze.csv` files contain data only for frames within failure periods.

## Reference

If you use our dataset, please cite [our paper]():

```
@inproceedings{human_behavior_reaction,
  title={},
  author={},
  booktitle={},
  year={}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
