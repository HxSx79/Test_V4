from dataclasses import dataclass
from src.data_processing.video_processor import VideoProcessor
from src.data_processing.bom_handler import BOMHandler
from src.detection.detector import ObjectDetector
from src.detection.line_detector import LineCrossingDetector

@dataclass
class ApplicationComponents:
    """Container for application components"""
    video_processor: VideoProcessor
    object_detector: ObjectDetector
    line_detector: LineCrossingDetector
    bom_handler: BOMHandler

    @classmethod
    def create(cls, model_path: str, bom_file: str):
        """Create and initialize all components"""
        return cls(
            video_processor=VideoProcessor(),
            object_detector=ObjectDetector(model_path),
            line_detector=LineCrossingDetector(),
            bom_handler=BOMHandler(bom_file)
        )