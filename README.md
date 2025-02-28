# REFLEX Dataset: A Multimodal Dataset of Human Reactions to Robot Failures and Explanations

REFLEX (Robotic Explanations to FaiLures and Human EXpressions) is a comprehensive multimodal dataset capturing human reactions to robot failures and subsequent explanations in collaborative settings. This dataset facilitates research into human-robot interaction dynamics, addressing the need to study reactions to both initial failures and explanations, as well as the evolution of these reactions in long-term interactions.

## Overview

The REFLEX dataset provides rich, annotated data on human responses to different types of failures, explanation levels, and explanation varying strategies. It contributes to the development of more robust, adaptive, and satisfying robotic systems capable of maintaining positive relationships with human collaborators, even during challenges like repeated failures.

The data was collected from a user study where participants collaborated with a robot on a task where the robot experienced programmed failures. Different explanation strategies were employed across participants to study their effects.

## Repository Structure

```
├── Dataset               # Download the dataset here
│   └── DatasetGuide.md   # Python dependencies for visualization
├── reflex_viz/           # Code for visualizing the multimodal data
│   ├── requirements.txt  # Python dependencies for visualization
│   └── main.py           # Main visualization script
├── LICENSE.md            # MIT License details
└── README.md             # This filet
```

## Dataset Access

The full dataset is available on Zenodo: [https://zenodo.org/records/14160783](https://zenodo.org/records/14160783)

## Quick Start

The repository includes a visualization tool built using [Rerun](https://www.rerun.io/), an open-source visualization tool for multimodal data.

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/reflex-viz.git
   cd reflex-viz
   ```

2. Install the dependencies for visualization:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Visualization Tool

To visualize participant interactions with the dataset:

```bash
python main.py --participant C1-1
```

Replace `C1-1` with the participant code following the format `{strategy}-{participant_number}`, where:
- Strategy is one of: C1, C2, C3, D1, or D2
- Participant number is between 1 and 11

See `DatasetGuide.md` for more detailed about the dataset.

#### Command-line Arguments

- `--participant`: Participant code in the format `{strategy}-{number}` (e.g., 'C1-1')
- `--max-frames`: Maximum number of frames to process (default: 18000)
- `--jpeg-quality`: JPEG compression quality for images from 1-100 (default: 15)
- `--data-path`: Path to the data directory (optional)
- `--face-3d`: Enable 3D face visualization
- `--gaze-3d`: Enable 3D gaze visualization
- `--body-3d`: Enable 3D body visualization
- `--openface-confidence`: Minimum confidence threshold for OpenFace data from 0.0-1.0 (default: 0.7)

### Visualization Features

The visualization integrates multiple data modalities synchronized by time (or frame):

- Video from Camera 1 with overlaid landmarks (face, body, eyes)
- Current failure phase, conversation, gaze, and pose classification as text
- Graphs displaying emotion values, FAU intensities, and arousal scores
- Timeline of the interaction phases

## Example Analysis

The dataset allows for various analyses, including:

1. Comparing human reactions to different robotic failures
2. Assessing the effectiveness of different explanation strategies
3. Studying how human satisfaction evolve with repeated failures
4. Analyzing multimodal behavioral patterns in response to robot explanations

One interesting insight from initial analysis shows lower confusion likelihood during pick failures compared to more complex carry-place failures, suggesting pick failures were perceived as easier to resolve.

## Reference

If you use our dataset, please cite [our paper](https://arxiv.org/abs/2502.14185):

```bibtex
@inproceedings{reflex_dataset,
    title={REFLEX Dataset: A Multimodal Dataset of Human Reactions to Robot Failures and Explanations}, 
    author={Parag Khanna and Andreas Naoum and Elmira Yadollahi and Mårten Björkman and Christian Smith},
    year={2025},
    eprint={2502.14185},
    archivePrefix={arXiv},
    primaryClass={cs.RO},
    url={https://arxiv.org/abs/2502.14185}, 
}
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
