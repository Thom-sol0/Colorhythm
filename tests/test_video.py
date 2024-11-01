import argparse
from typing import Optional

import cv2

from colorhythm.core.camera import Camera
from colorhythm.utils import io


def test_video(source: Optional[str] = None) -> None:
    """Test the video source by displaying the video feed.
    
    Args:
        source: Optional path to video file. If None, will prompt for camera selection.
    """
    selected_source = io.get_video_source(source)
    
    try:
        with Camera(selected_source) as camera:
            if not camera.is_opened:
                raise RuntimeError("Failed to open camera")

            while True:
                success, frame = camera.get_frame()
                if not success:
                    print("Failed to capture frame")
                    break

                cv2.imshow('Video Test', frame)
                
                # Press 'q' to quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
    except KeyboardInterrupt:
        print("\nStopping video test...")
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Video Test')
    parser.add_argument('--source', type=str, help='Path to video file')
    args = parser.parse_args()
    
    test_video(args.source)