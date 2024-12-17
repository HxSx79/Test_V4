def calculate_center_point(bbox):
    """Calculate center point of bounding box"""
    x_center = (bbox[0] + bbox[2]) / 2
    y_center = (bbox[1] + bbox[3]) / 2
    return x_center, y_center

def process_detection(detection, frame_width, line_detector, bom_handler):
    """Process single detection and return crossing event if applicable"""
    obj_id, (class_name, bbox) = detection
    x_center, y_center = calculate_center_point(bbox)
    
    if line_detector.detect_crossing(obj_id, (x_center, y_center), frame_width) == 'crossed':
        bom_info = bom_handler.get_part_info(class_name)
        return {
            'object_id': obj_id,
            'class_name': class_name,
            'bom_info': bom_info
        }
    return None