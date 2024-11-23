from PIL import Image
import cv2
import csv
import numpy as np
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


def resize_image(input_path: str, output_path: str, new_width: int = 150) -> None:
    with Image.open(input_path) as img:
        original_width, original_height = img.size
        new_height = int((new_width / original_width) * original_height)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_img.save(output_path)
        logger.info(f"Image resized to {new_width}x{new_height} pixels.")


def apply_custom_colormap(
    input_path: str, output_path: str, colormap: int = cv2.COLORMAP_JET
) -> None:
    img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Cannot read image at {input_path}")
    colored_img = cv2.applyColorMap(img, colormap)
    cv2.imwrite(output_path, colored_img)
    logger.info(f"Custom colormap applied and saved to {output_path}.")


def csv_to_image(csv_file_path: str, output_image_path: str) -> Tuple[float, float]:
    depths = []
    pixel_matrix = []

    with open(csv_file_path, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        header = [column.strip() for column in next(reader)]
        logger.debug(f"Header row: {header}")

        if "depth" not in header:
            raise ValueError("'depth' column not found in the CSV file.")

        depth_index = header.index("depth")
        pixel_start_index = depth_index + 1

        for row in reader:
            if not row or not row[depth_index].strip():
                continue

            try:
                depth_value = float(row[depth_index].strip())
                depths.append(depth_value)
            except ValueError as e:
                raise ValueError(
                    f"Invalid depth value at row {reader.line_num}: '{row[depth_index]}'"
                ) from e

            pixel_values = []
            for value in row[pixel_start_index:]:
                value = value.strip()
                if not value:
                    continue
                try:
                    pixel_values.append(int(value))
                except ValueError as e:
                    raise ValueError(
                        f"Invalid pixel value '{value}' at row {reader.line_num}"
                    ) from e
            pixel_matrix.append(pixel_values)

    if not pixel_matrix:
        raise ValueError("No valid data found in the CSV file.")

    pixel_array = np.array(pixel_matrix, dtype=np.uint8)
    img = Image.fromarray(pixel_array, mode="L")
    img.save(output_image_path)
    logger.info(f"Image saved to {output_image_path}.")

    depth_min = min(depths)
    depth_max = max(depths)
    return depth_min, depth_max
