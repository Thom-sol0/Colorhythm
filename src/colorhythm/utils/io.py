from pathlib import Path
from typing import List, Optional, Union
import logging
from contextlib import contextmanager
import os
import sys

import cv2

@contextmanager
def suppress_stdout_stderr():
    """Context manager to suppress stdout and stderr."""
    # Save the current file descriptors
    old_stdout_fd = os.dup(sys.stdout.fileno())
    old_stderr_fd = os.dup(sys.stderr.fileno())

    # Open null device
    with open(os.devnull, 'w') as devnull:
        # Replace stdout and stderr with devnull
        os.dup2(devnull.fileno(), sys.stdout.fileno())
        os.dup2(devnull.fileno(), sys.stderr.fileno())

    try:
        yield
    finally:
        # Restore original stdout and stderr
        os.dup2(old_stdout_fd, sys.stdout.fileno())
        os.dup2(old_stderr_fd, sys.stderr.fileno())
        # Clean up file descriptors
        os.close(old_stdout_fd)
        os.close(old_stderr_fd)


def get_available_video_sources(max_sources: int = 10) -> List[int]:
    """
    Get a list of available video sources with complete warning suppression.
    """
    available_sources = []

    with suppress_stdout_stderr():
        for i in range(max_sources):
            try:
                cap = cv2.VideoCapture(i)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        available_sources.append(i)
                cap.release()
            except (cv2.error, OSError, IOError):
                continue

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