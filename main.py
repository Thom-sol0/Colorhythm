import argparse
import sys

import cv2

from colorhythm.core.camera import Camera
from colorhythm.core.processing import apply_gaussian_blur
from colorhythm.utils import io


class VideoProcessor:
    def __init__(self, camera: Camera, window_name: str = 'Video Feed'):
        self.camera = camera
        self.window_name = window_name
        self._setup_window()

    def _setup_window(self) -> None:
        cv2.namedWindow(self.window_name)
        cv2.createTrackbar('Blur Intensity', self.window_name, 1, 20, 
                          lambda x: None)

    def process_frame(self, frame: cv2.UMat) -> cv2.UMat:
        blur_intensity = cv2.getTrackbarPos('Blur Intensity', self.window_name)
        # Ensure blur intensity is odd and at least 1
        blur_intensity = max(1, blur_intensity + (blur_intensity % 2 == 0))
        return apply_gaussian_blur(frame, blur_intensity)

    def run(self) -> None:
        if not self.camera.is_opened:
            print("Error: Camera not initialized", file=sys.stderr)
            return

        try:
            while True:
                success, frame = self.camera.get_frame()
                if not success:
                    print("Failed to capture frame", file=sys.stderr)
                    break

                processed_frame = self.process_frame(frame)
                cv2.imshow(self.window_name, processed_frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            print("\nStopping video processing...")
        finally:
            self.cleanup()

    def cleanup(self) -> None:
        self.camera.release()
        cv2.destroyAllWindows()

def main() -> None:
    """Main function to process video input with blur effect"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Video Processing Application')
    parser.add_argument('--source-path', type=str, help='Path to the video file')
    args = parser.parse_args()

    selected_source = io.get_video_source(args.source_path)  # Input and/or validate video source
    with Camera(selected_source) as camera:
        processor = VideoProcessor(camera)
        processor.run()

if __name__ == "__main__":
    main()