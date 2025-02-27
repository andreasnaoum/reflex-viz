from typing import Dict, Optional
import rerun as rr
import rerun.blueprint as rrb


# For more information about Rerun Blueprint, visit: https://rerun.io/docs/concepts/blueprint
def create_default_rrb() -> rrb.Blueprint:
    """Create default rerun blueprint."""
    return rrb.Blueprint(
        rrb.Horizontal(
            rrb.Vertical(
                rrb.Tabs(
                    rrb.Spatial2DView(origin="cam2", name="Cam2"),
                    rrb.Spatial3DView(origin="Body3D", name="Body3D"),
                    rrb.Spatial3DView(origin="Face3D", name="Face3D"),
                ),
                rrb.Tabs(
                    rrb.Spatial2DView(origin="description", name="Failure Description"),
                    rrb.TextDocumentView(origin="Failure", name="Failure Status"),
                ),
                name="Visual Representation",
                row_shares=[3, 2],
            ),

            rrb.Vertical(
                rrb.Spatial2DView(origin="video", name="Cam1"),
                rrb.Tabs(
                    rrb.TextDocumentView(origin="Transcript", name="Transcript"),
                    rrb.TextDocumentView(origin="body", name="Body Classification"),
                    rrb.TextDocumentView(origin="Gaze", name="Gaze Classification"),
                ),
                rrb.Tabs(
                    rrb.TimeSeriesView(origin="Affect", name="Affect State"),
                    rrb.TimeSeriesView(origin="Positive", name="Positive Emotions"),
                    rrb.TimeSeriesView(origin="Negative", name="Negative Emotions"),
                    rrb.TimeSeriesView(origin="AUs", name="AUs"),
                    rrb.TimeSeriesView(origin="Speech", name="Speech Prosody"),
                ),
                name="More Data",
                row_shares=[3, 1, 1],
            ),
        ),
        rrb.BlueprintPanel(state="collapsed"),
        rrb.SelectionPanel(state="collapsed"),
        rrb.TimePanel(state="collapsed"),
    )

def create_video1_rrb() -> rrb.Blueprint:
    """Create rerun blueprint."""
    return rrb.Blueprint(
        rrb.Horizontal(
            rrb.Vertical(
                rrb.Tabs(
                    rrb.Spatial3DView(origin="Body3D", name="Body3D"),
                    rrb.Spatial3DView(origin="Face3D", name="Face3D"),
                ),
                rrb.Tabs(
                    rrb.TextDocumentView(origin="Failure", name="Failure Status"),
                    rrb.Spatial2DView(origin="description", name="Failure Description"),
                ),
                name="Visual Representation",
                row_shares=[3, 2],
            ),

            rrb.Vertical(
                rrb.Spatial2DView(origin="video", name="Cam1"),
                rrb.Tabs(
                    rrb.TextDocumentView(origin="Transcript", name="Transcript"),
                    rrb.TextDocumentView(origin="body", name="Body Classification"),
                    rrb.TextDocumentView(origin="Gaze", name="Gaze Classification"),
                ),
                rrb.Tabs(
                    rrb.TimeSeriesView(origin="Affect", name="Affect State"),
                    rrb.TimeSeriesView(origin="Positive", name="Positive Emotions"),
                    rrb.TimeSeriesView(origin="Negative", name="Negative Emotions"),
                    rrb.TimeSeriesView(origin="AUs", name="AUs"),
                    rrb.TimeSeriesView(origin="Speech", name="Speech Prosody"),
                ),
                name="More Data",
                row_shares=[3, 1, 1],
            ),
        ),
        rrb.BlueprintPanel(state="collapsed"),
        rrb.SelectionPanel(state="collapsed"),
        rrb.TimePanel(state="collapsed"),
    )
