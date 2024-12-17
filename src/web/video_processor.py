import threading
from typing import Optional
from src.utils.video_utils import encode_frame_to_base64
from src.utils.detection_utils import process_detection

class VideoProcessor:
    """Handles video processing and frame distribution"""
    def __init__(self, components, stream_manager):
        self.components = components
        self.stream_manager = stream_manager
        self._processing_thread: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()

    def start(self, video_path: str):
        """Start video processing in separate thread"""
        if self._processing_thread and self._processing_thread.is_alive():
            self.stop()
        
        self._stop_flag.clear()
        self._processing_thread = threading.Thread(
            target=self._process_video,
            args=(video_path,)
        )
        self._processing_thread.start()

    def stop(self):
        """Stop video processing"""
        self._stop_flag.set()
        if self._processing_thread:
            self._processing_thread.join()

    def _process_video(self, video_path: str):
        """Process video frames and broadcast results"""
        try:
            for frame in self.components.video_processor.process_video_stream(video_path):
                if self._stop_flag.is_set():
                    break

                # Process frame
                detections = self.components.object_detector.detect_objects(frame)
                frame = self.components.line_detector.draw_line(frame)

                # Process detections
                crossing_events = []
                for detection in enumerate(detections):
                    event = process_detection(
                        detection,
                        frame.shape[1],
                        self.components.line_detector,
                        self.components.bom_handler
                    )
                    if event:
                        crossing_events.append(event)

                # Broadcast results
                self.stream_manager.broadcast({
                    'frame': encode_frame_to_base64(frame),
                    'crossing_events': crossing_events
                })

        except Exception as e:
            self.stream_manager.broadcast({'error': str(e)})