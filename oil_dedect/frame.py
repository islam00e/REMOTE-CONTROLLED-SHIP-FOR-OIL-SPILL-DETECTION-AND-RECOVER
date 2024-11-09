import cv2
import numpy as np

def random_crop(image, crop_size):
    """
    Randomly crop an image to a specified size.

    Args:
        image: The input image.
        crop_size: The desired size of the cropped image.

    Returns:
        The cropped image.
    """
    height, width = image.shape[:2]

    # Generate random crop coordinates
    x = np.random.randint(0, width - crop_size[0])
    y = np.random.randint(0, height - crop_size[1])

    cropped_image = image[y:y + crop_size[1], x:x + crop_size[0], :]
    return cropped_image

def random_flip(image):
    """
    Randomly flip an image horizontally or vertically.

    Args:
        image: The input image.

    Returns:
        The flipped image.
    """
    # Randomly flip the image horizontally or vertically
    flip_code = np.random.choice([0, 1, 2])

    flipped_image = cv2.flip(image, flip_code)
    return flipped_image

def random_rotate(image, angle_range):
    """
    Randomly rotate an image by an angle within a specified range.

    Args:
        image: The input image.
        angle_range: The range of rotation angles (in degrees).

    Returns:
        The rotated image.
    """
    # Generate a random rotation angle within the specified range
    angle = np.random.uniform(-angle_range, angle_range)

    # Rotate the image using OpenCV's warpAffine function
    center = (image.shape[1] // 2, image.shape[0] // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(image, rotation_matrix, image.shape)

    return rotated_image

def augment_image(image):
    """
    Apply a sequence of data augmentation techniques to an image.

    Args:
        image: The input image.

    Returns:
        The augmented image.
    """
    # Apply random cropping
    cropped_image = random_crop(image, (64, 64))

    # Apply random flipping
    flipped_image = random_flip(cropped_image)

    # Apply random rotation
    rotated_image = random_rotate(flipped_image, 10)

    return rotated_image
