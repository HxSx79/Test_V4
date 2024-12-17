import os
import json
from flask import Flask, Response, request, jsonify, render_template
from src.config.settings import SECRET_KEY, MODEL_PATH, BOM_FILE
from src.utils.file_handler import allowed_file, save_uploaded_file
from .components import ApplicationComponents
from .stream_manager import StreamManager
from .video_processor import VideoProcessor

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    # Initialize components
    components = ApplicationComponents.create(MODEL_PATH, BOM_FILE)
    stream_manager = StreamManager()
    video_processor = VideoProcessor(components, stream_manager)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'video' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'})
            
        file = request.files['video']
        if not file or not file.filename:
            return jsonify({'success': False, 'error': 'No file selected'})
            
        if not allowed_file(file.filename):
            return jsonify({'success': False, 'error': 'Invalid file type'})
            
        try:
            file_path = save_uploaded_file(file)
            return jsonify({'success': True, 'video_path': file_path})
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

    @app.route('/stream')
    def stream():
        def generate():
            client = stream_manager.add_client()
            try:
                while client.active:
                    try:
                        data = client.queue.get(timeout=30)
                        yield f"data: {json.dumps(data)}\n\n"
                    except queue.Empty:
                        yield "data: {}\n\n"  # Keep-alive
            finally:
                stream_manager.remove_client(client)
        
        return Response(generate(), mimetype='text/event-stream')

    @app.route('/start-processing', methods=['POST'])
    def start_processing():
        data = request.get_json()
        video_path = data.get('video_path')
        
        if not video_path or not os.path.exists(video_path):
            return jsonify({'success': False, 'error': 'Invalid video path'})
            
        video_processor.start(video_path)
        return jsonify({'success': True})

    return app