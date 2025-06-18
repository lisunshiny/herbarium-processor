from google.cloud import vision
import io
import os
from google.protobuf.json_format import MessageToDict
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont, ExifTags
import cv2
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser(
    "~/.secrets/vision-key.json"
)


class OcrClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.preprocessor = ImagePreprocessor(correct_perspective=True)

    def extract_text_json(self, image_path):
        # Get the base name of the file without extension
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        preprocessed_path = f"../../tmp/ocr_preprocessed_{base_name}.jpg"
        preprocessed_path = os.path.normpath(preprocessed_path)
        self.preprocessor.preprocess_and_save(image_path, preprocessed_path)

        with io.open(preprocessed_path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Perform OCR
        response = self.client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(f"Google OCR API error: {response.error.message}")

        lines = self.parse_google_ocr_response(response)
        merged_lines = self.merge_to_lines(lines)
        self.visualize_bounding_boxes(
            merged_lines, preprocessed_path, preprocessed_path
        )

        return merged_lines

    def parse_google_ocr_response(self, response):
        response_dict = MessageToDict(response._pb)

        lines = []
        id_counter = 1

        try:
            pages = response_dict["fullTextAnnotation"]["pages"]
        except KeyError:
            return []

        for page_idx, page in enumerate(pages):
            for block_idx, block in enumerate(page.get("blocks", [])):
                block_type = block.get("blockType", "UNKNOWN")

                for para_idx, para in enumerate(block.get("paragraphs", [])):
                    for word_idx, word in enumerate(para.get("words", [])):
                        word_text = "".join([s["text"] for s in word["symbols"]])
                        bbox = word["boundingBox"]["vertices"]
                        id_str = f"{page_idx + 1}.{block_idx + 1}.{id_counter}"
                        id_counter += 1

                        lines.append(
                            {
                                "id": id_str,
                                "text": word_text,
                                "bounding_box": bbox,
                                "confidence": word.get("confidence", 1.0),
                                "block_type": block_type,
                            }
                        )
        return lines

    def merge_to_lines(self, words, max_gap=30):
        lines = defaultdict(list)

        for w in words:
            y = round(w["bounding_box"][0]["y"] / max_gap)  # naive line grouping
            lines[y].append(w)

        result = []
        for i, (line_key, word_list) in enumerate(sorted(lines.items())):
            sorted_words = sorted(word_list, key=lambda w: w["bounding_box"][0]["x"])
            text = " ".join(w["text"] for w in sorted_words)

            # Merge all points into one bounding box (min-x, min-y) to (max-x, max-y)
            all_x = [
                pt["x"] for w in sorted_words for pt in w["bounding_box"] if "x" in pt
            ]
            all_y = [
                pt["y"] for w in sorted_words for pt in w["bounding_box"] if "y" in pt
            ]
            if all_x and all_y:
                merged_box = [
                    {"x": min(all_x), "y": min(all_y)},
                    {"x": max(all_x), "y": min(all_y)},
                    {"x": max(all_x), "y": max(all_y)},
                    {"x": min(all_x), "y": max(all_y)},
                ]
            else:
                merged_box = []

            avg_confidence = sum(w["confidence"] for w in sorted_words) / len(
                sorted_words
            )
            block_type = sorted_words[0].get("block_type", "UNKNOWN")

            result.append(
                {
                    "id": f"1.1.{i+1}",
                    "text": text,
                    "bounding_box": merged_box,
                    "average_confidence": avg_confidence,
                    "block_type": block_type,
                }
            )
        return result

    def visualize_bounding_boxes(self, words, image_path, output_path):
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()

        for word in words:
            bbox = word.get("bounding_box", [])
            source = word.get("id", "")
            if len(bbox) == 4:
                points = [tuple((v.get("x", 0), v.get("y", 0))) for v in bbox]
                draw.line(points + [points[0]], fill="red", width=2)
                draw.text(points[0], source, fill="blue", font=font)

        image.save(output_path)
        print(
            f"Saved visualized image with bounding boxes and sources to {output_path}"
        )


class ImagePreprocessor:
    """
    Preprocess images for improved OCR accuracy using grayscale conversion,
    sharpening, resizing, contrast stretching, denoising, and optional
    perspective correction.

    Usage:
        pre = ImagePreprocessor(correct_perspective=True)

        # To get a processed image as an OpenCV array:
        processed = pre.preprocess_for_ocr("input.jpg")

        # To save the processed image to disk:
        pre.preprocess_and_save("input.jpg", "output.jpg")
    """

    def __init__(self, correct_perspective=True):
        self.correct_perspective = correct_perspective

    def preprocess_for_ocr(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Unable to load image: {image_path}")

        if self.correct_perspective:
            img = self._apply_perspective_correction(img)

        # Step 1: Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step 2: Sharpen image to improve text clarity
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(gray, -1, kernel)

        # Step 3: Resize if resolution is low
        height, width = sharpened.shape
        if height < 1000:
            sharpened = cv2.resize(
                sharpened, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC
            )

        # Step 4: Light contrast stretch
        processed = cv2.convertScaleAbs(sharpened, alpha=1.2, beta=10)

        # Step 5: Denoise (optional)
        denoised = cv2.fastNlMeansDenoising(processed, h=15)

        return denoised

    def _apply_perspective_correction(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 50, 200)

        contours, _ = cv2.findContours(
            edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                screen_cnt = approx
                break
        else:
            return img  # No correction if no 4-point contour found

        pts = screen_cnt.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        (tl, tr, br, bl) = rect
        width_a = np.linalg.norm(br - bl)
        width_b = np.linalg.norm(tr - tl)
        max_width = max(int(width_a), int(width_b))

        height_a = np.linalg.norm(tr - br)
        height_b = np.linalg.norm(tl - bl)
        max_height = max(int(height_a), int(height_b))

        dst = np.array(
            [
                [0, 0],
                [max_width - 1, 0],
                [max_width - 1, max_height - 1],
                [0, max_height - 1],
            ],
            dtype="float32",
        )

        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(img, M, (max_width, max_height))
        return warped

    def save_preprocessed_image(self, image, save_path):
        cv2.imwrite(save_path, image)

    def preprocess_and_save(self, image_path, output_path):
        image = self.preprocess_for_ocr(image_path)
        self.save_preprocessed_image(image, output_path)
        return output_path
