from google.cloud import vision
import io
import os
from google.protobuf.json_format import MessageToDict
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/.secrets/vision-key.json")

class OcrClient:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def extract_text_json(self, image_path):
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        # Perform OCR
        response = self.client.document_text_detection(image=image)

        if response.error.message:
            raise Exception(f"Google OCR API error: {response.error.message}")

        return response

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
                        word_text = ''.join([s["text"] for s in word["symbols"]])
                        bbox = word["boundingBox"]["vertices"]
                        id_str = f"{page_idx + 1}.{block_idx + 1}.{id_counter}"
                        id_counter += 1

                        lines.append({
                            "id": id_str,
                            "text": word_text,
                            "bounding_box": bbox,
                            "confidence": word.get("confidence", 1.0),
                            "block_type": block_type
                        })
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
            all_x = [pt["x"] for w in sorted_words for pt in w["bounding_box"] if "x" in pt]
            all_y = [pt["y"] for w in sorted_words for pt in w["bounding_box"] if "y" in pt]
            if all_x and all_y:
                merged_box = [
                    {"x": min(all_x), "y": min(all_y)},
                    {"x": max(all_x), "y": min(all_y)},
                    {"x": max(all_x), "y": max(all_y)},
                    {"x": min(all_x), "y": max(all_y)}
                ]
            else:
                merged_box = []

            avg_confidence = sum(w["confidence"] for w in sorted_words) / len(sorted_words)
            block_type = sorted_words[0].get("block_type", "UNKNOWN")

            result.append({
                "id": f"1.1.{i+1}",
                "text": text,
                "bounding_box": merged_box,
                "average_confidence": avg_confidence,
                "block_type": block_type,
            })
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
        print(f"Saved visualized image with bounding boxes and sources to {output_path}")
