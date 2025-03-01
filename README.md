<a href="https://zenodo.org/records/14160783"><img src="https://img.shields.io/badge/Zenodo-Dataset-green"></a> 
<a href="https://arxiv.org/abs/2502.14185"><img src="https://img.shields.io/badge/arXiv-Paper-red"></a>

# REFLEX Dataset: A Multimodal Dataset of Human Reactions to Robot Failures and Explanations



## Overview

REFLEX (Robotic Explanations to FaiLures and Human EXpressions) is a comprehensive multimodal dataset capturing human reactions to robot failures and subsequent explanations in collaborative settings. This dataset facilitates research into human-robot interaction dynamics, addressing the need to study reactions to both initial failures and explanations, as well as the evolution of these reactions in long-term interactions.

The data was collected from a [user study](https://arxiv.org/abs/2303.16010) where participants collaborated with a robot on a task where the robot experienced programmed failures. Different explanation strategies were employed across participants to study their effects.

## Repository Structure

```
├── Dataset               
│   ├── Data               # Download the dataset here
│   └── DatasetGuide.md    # Python dependencies for visualization
├── reflex_visualization/  # Code for visualizing the multimodal data
│   ├── requirements.txt   # Python dependencies for visualization
│   └── src                # Visualization Code
│       ├── ...            
│       └── main.py        # Main visualization script
├── LICENSE.md             # MIT License details
└── README.md              # This file
```

## Quick Start

The repository includes a visualization tool built using [Rerun](https://www.rerun.io/), an open-source visualization sdk for multimodal data.

### Installation and Run the Visualization Tool

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/reflex-viz.git
   ```

2. Download the Data from [Zenodo](https://zenodo.org/records/14160783) and place them under the Dataset folder.

3. Install the dependencies for visualization:
   ```bash
   cd reflex-visualization
   pip install -r requirements.txt
   ```

4. To visualize a participant interaction with the dataset:
   ```bash
   python src/main.py --participant C1-1
   ```
Replace `C1-1` with the participant code following the format `{strategy}-{participant_number}`, where:
- Strategy is one of: C1, C2, C3, D1, or D2
- Participant number is between 1 and 11

See [`DatasetGuide.md`](Dataset/DatasetGuide.md) for more detailed about the dataset.

#### Command-line Arguments

- `--participant`: Participant code in the format `{strategy}-{number}` (e.g., 'C1-1')
- `--max-frames`: Maximum number of frames to process (optional, default: `None`)
- `--jpeg-quality`: JPEG compression quality for images from 1-100 (optional, default: 15)
- `--data-path`: Path to the data directory (optional)
- `--face-3d`: Enable 3D face visualization (optional, default: false)
- `--gaze-3d`: Enable 3D gaze visualization (optional, default: false)
- `--body-3d`: Enable 3D body visualization (optional, default: false)
- `--openface-confidence`: Minimum confidence threshold for OpenFace from 0.0-1.0 (optional, default: 0.7)

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
