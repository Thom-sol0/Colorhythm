from pathlib import Path
from typing import Optional, Tuple, Union

import cv2


class Camera:
    def __init__(self, source: Union[int, str, Path] = 0):
        self.source = source if isinstance(source, int) else str(source)
        self.cap: Optional[cv2.VideoCapture] = None
        self._initialize_camera()

    def _initialize_camera(self) -> None:
        """Initialize the camera."""
        self.cap = cv2.VideoCapture(self.source)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {self.source}")
        
    @property
    def is_opened(self) -> bool:
        """Check if camera is opened."""
        return self.cap is not None and self.cap.isOpened()

    def get_frame(self) -> Tuple[bool, Optional[cv2.UMat]]:
        """Capture a frame from the camera.

        Returns:
            A tuple containing a boolean indicating success and the captured frame.
        """
        if self.cap is None:
            raise RuntimeError("Camera is not initialized.")
        ret, frame = self.cap.read()
        if not ret:
            return False, None
        return True, frame

    def release(self) -> None:
        """Release the camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def __enter__(self) -> 'Camera':
        """Support context manager for automatic resource management."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Ensure resources are released when exiting the context."""
        self.release()