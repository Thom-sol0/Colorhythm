from pathlib import Path
from typing import List, Optional, Union

import cv2


def get_available_video_sources(max_sources: int = 10) -> List[int]:
    """Get a list of available video sources."""
    available_sources = []
    for i in range(max_sources):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_sources.append(i)
        cap.release()
    return available_sources

def get_video_source(file_path: Optional[str] = None) -> Union[int, Path]:
    """Validate and return the video source or file path."""
    if file_path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Video file not found: {path}")
        return path

    available_sources = get_available_video_sources()
    if not available_sources:
        raise RuntimeError("No video sources available")

    print("Available video sources:", available_sources)
    while True:
        try:
            video_source = int(input("Please enter the video source number: "))
            if video_source in available_sources:
                return video_source
            print(f"Invalid source. Available sources are: {available_sources}")
        except ValueError:
            print("Please enter a valid number")