import os
import cv2

def extract_and_save_frame(video_path, timestamp, normalized_coordinates):
    """
    Extracts a frame from the video at the given timestamp, crops it using the given coordinates,
    and saves it in the 'cropped/<filename>/' folder with incrementing filenames.

    Args:
        video_path (str): Path to the video file.
        timestamp (str): Timestamp in 'mm:ss' or 'hh:mm:ss' format.
        normalized_coordinates (list): Normalized coordinates [ymin, xmin, ymax, xmax].

    Returns:
        str: Path to the saved cropped image.
    """
    # Convert timestamp to seconds
    def timestamp_to_seconds(timestamp):
        if len(timestamp.split(':')) == 3:  # Format hh:mm:ss
            h, m, s = map(int, timestamp.split(':'))
            return h * 3600 + m * 60 + s
        elif len(timestamp.split(':')) == 2:  # Format mm:ss
            m, s = map(int, timestamp.split(':'))
            return m * 60 + s
        else:
            raise ValueError("Invalid timestamp format")

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Failed to open video file '{video_path}'. Please check the file path.")

    # Get video FPS and dimensions
    fps = cap.get(cv2.CAP_PROP_FPS)
    success, frame = cap.read()
    if not success:
        raise ValueError(f"Failed to read a frame from '{video_path}'.")

    frame_height, frame_width, _ = frame.shape

    # Convert normalized coordinates to pixel coordinates
    def normalized_to_pixel_coordinates(normalized_coords, width, height):
        ymin, xmin, ymax, xmax = [coord / 1000 for coord in normalized_coords]  # Divide by 1000
        ymin_pixel = int(ymin * height)
        xmin_pixel = int(xmin * width)
        ymax_pixel = int(ymax * height)
        xmax_pixel = int(xmax * width)
        return [ymin_pixel+100, xmin_pixel+100, ymax_pixel+100, xmax_pixel+100]

    pixel_coordinates = normalized_to_pixel_coordinates(normalized_coordinates, frame_width, frame_height)

    # Convert timestamp to frame number
    total_seconds = timestamp_to_seconds(timestamp)
    frame_number = int(total_seconds * fps)

    # Set the video position to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    success, frame = cap.read()

    if success:
        # Crop the frame using the pixel coordinates
        ymin_pixel, xmin_pixel, ymax_pixel, xmax_pixel = pixel_coordinates
        #cropped_frame = frame[ymin_pixel:ymax_pixel, xmin_pixel:xmax_pixel]
        cropped_frame = frame
      

        # Create output directory
        filename_without_ext = os.path.splitext(os.path.basename(video_path))[0]
        
        # Replace invalid characters in filename (e.g., ":" or special symbols)
        sanitized_filename = "".join(c for c in filename_without_ext if c.isalnum() or c in " _-").strip()
        
        output_dir = os.path.join("static/cropped", sanitized_filename)
        
        try:
            os.makedirs(output_dir, exist_ok=True)
        except OSError as e:
            raise ValueError(f"Failed to create output directory '{output_dir}': {e}")

        # Find the next available filename
        existing_files = os.listdir(output_dir)
        existing_numbers = [
            int(f.split('_')[-1].split('.')[0]) for f in existing_files 
            if f.startswith("cropped_image_") and f.split('_')[-1].split('.')[0].isdigit()
        ]
        next_number = max(existing_numbers, default=0) + 1

        # Save the cropped image with an incremented filename
        output_path = os.path.join(output_dir, f"cropped_image_{next_number}.jpg")
        cv2.imwrite(output_path, cropped_frame)

        cap.release()
        return output_path
    else:
        cap.release()
        raise ValueError("Failed to extract frame from the video.")

# Example usage with separate timestamps and coordinates lists
# video_path = r"videos\APIs Explained (in 4 Minutes).mp4"  # Use raw string (r"") for Windows paths

# timestamps = ["02:57", "03:10"]
# coordinates = [
#     [171, 143, 863, 822],
#     [200, 150, 850, 800]
# ]

# if len(timestamps) != len(coordinates):
#     raise ValueError("The number of timestamps and coordinates must match.")

# for i in range(len(timestamps)):
#     try:
#         output_path = extract_and_save_frame(video_path, timestamps[i], coordinates[i])
#         print(f"Cropped image saved at: {output_path}")
#     except ValueError as e:
#         print(e)
