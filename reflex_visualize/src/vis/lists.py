import enum

# Adjust based on what you want to visualize
positive_emotions = [
    'Admiration', 'Adoration', 'Aesthetic Appreciation', 'Amusement',
    # 'Awe', 'Calmness', 'Contentment', 'Determination', 'Excitement', 'Interest',
    # 'Joy', 'Love', 'Pride', 'Relief', 'Satisfaction', 'Surprise (positive)', 'Triumph'
]

negative_emotions = [
    'Anger', 'Anxiety', 'Awkwardness', 'Boredom', 'Confusion', 'Contempt',
    # 'Disappointment', 'Disgust', 'Distress', 'Doubt', 'Embarrassment',
    # 'Empathic Pain', 'Envy', 'Fear', 'Guilt', 'Horror', 'Pain', 'Sadness',
    # 'Shame', 'Surprise (negative)', 'Tiredness'
]

aus = [
    'AU1 Inner Brow Raise', 'AU2 Outer Brow Raise', 'AU4 Brow Lowerer',
    'AU5 Upper Lid Raise', 'AU6 Cheek Raise', 'AU7 Lids Tight',
    'AU9 Nose Wrinkle', 'AU10 Upper Lip Raiser', 'AU12 Lip Corner Puller',
    # 'AU15 Lip Corner Depressor', 'AU25 Lips Part', 'AU26 Jaw Drop'
]

speech_emotions = [
    'Admiration', 'Adoration', 'Amusement', 'Anger',
    'Anxiety', 'Awe', 'Awkwardness', 'Boredom'
]


class CustomPoseLandmark(enum.IntEnum):
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_WRIST = 15
    RIGHT_WRIST = 16
    LEFT_PINKY = 17
    RIGHT_PINKY = 18
    LEFT_INDEX = 19
    RIGHT_INDEX = 20
    LEFT_THUMB = 21
    RIGHT_THUMB = 22
    LEFT_HIP = 23
    RIGHT_HIP = 24


POSE_CONNECTIONS = frozenset([
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5),
    (5, 6), (6, 8), (9, 10), (11, 12), (11, 13),
    (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22),
    (18, 20), (11, 23), (12, 24), (23, 24), (23, 25),
    (24, 26), (25, 27), (26, 28), (27, 29), (28, 30),
    (29, 31), (30, 32), (27, 31), (28, 32)
])
