import cv2


def greyscale_frame(frame: cv2.UMat) -> cv2.UMat:
    """Convert the frame to greyscale."""
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

def apply_gaussian_blur(frame: cv2.UMat, blur_intensity: int) -> cv2.UMat:
    """Apply Gaussian blur to the frame with the specified blur intensity.
    
    Args:
        frame: Input frame to blur
        blur_intensity: Kernel size for Gaussian blur (must be odd)
    
    Returns:
        Blurred frame
    """
    if blur_intensity < 1:
        return frame
    
    # Ensure blur_intensity is odd
    kernel_size = max(1, blur_intensity + (blur_intensity % 2 == 0))
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)