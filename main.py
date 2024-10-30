import base64
import time
from io import BytesIO
from typing import List, Tuple

import cv2
import numpy as np
import paddle
import requests
from PIL import Image, ImageEnhance
from flask import Flask, request, jsonify, send_file
from paddleocr import PaddleOCR

isUseGpu = paddle.device.is_compiled_with_cuda()
print(f"isUseGpu: {isUseGpu}")  # 应输出 True
print(paddle.device.get_device())  # 应输出 'gpu:0'
# 初始化OCR模型
ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=isUseGpu)  # 指定语言为英语

app = Flask(__name__)

def get_image_type(data: bytes) -> str:
    """根据文件头字节手动检测图像类型"""
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return 'GIF'
    elif data[:2] == b'\xff\xd8':
        return 'JPEG'
    elif data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'PNG'
    elif data[:2] == b'BM':
        return 'BMP'
    return 'UNKNOWN'

def process_gif(image: Image.Image) -> Image.Image:
    """
    处理 GIF，将其所有帧叠加成单张静态图像，并返回为 JPG 格式。
    """
    frame_count = image.n_frames
    combined_image = None

    for i in range(frame_count):
        image.seek(i)
        rgb_image = image.convert("RGB")
        rgb_array = np.array(rgb_image)

        if combined_image is None:
            combined_image = rgb_array.astype(np.float32)
        else:
            combined_image += rgb_array

    combined_image = np.clip(combined_image / frame_count, 0, 255).astype(np.uint8)
    return Image.fromarray(combined_image)


def get_highest_confidence_text(ocr_result: List[List[Tuple]]) -> str:
    max_confidence_text = ""
    max_confidence = 0.0

    for line in ocr_result:
        for word_info in line:
            text, confidence = word_info[1][0], word_info[1][1]
            if confidence > max_confidence:
                max_confidence = confidence
                max_confidence_text = text

    return max_confidence_text if max_confidence_text else "No text detected"


def get_text_from_image(image: Image.Image) -> str:
    # 转换为灰度图像
    gray_image = image.convert('L')

    # 可选：增强对比度，提高识别效果
    enhancer = ImageEnhance.Contrast(gray_image)
    gray_image = enhancer.enhance(2.0)  # 参数 2.0 可以根据需要调整
    # 将灰度图像转换为 numpy 数组
    img_array = np.array(gray_image)

    # 因为 PaddleOCR 期望输入为 BGR 格式，需要将灰度图像转换为 BGR
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

    # 调用 OCR 识别
    ocr_result = ocr.ocr(img_bgr, cls=True)
    print(f"OCR Result: {ocr_result}")  # 打印 OCR 结果用于调试

    if not ocr_result:
        return "No text detected"

    return get_highest_confidence_text(ocr_result)


@app.route('/v1/image/ocr', methods=['POST'])
def get_text():
    start_time = time.time()
    # Step 1: 读取 URL 或 Base64
    url = request.form.get('url')
    image_base64 = request.form.get('image_base64')
    user_agent = request.form.get('useragent', 'Mozilla/5.0')

    if url:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        image = Image.open(BytesIO(response.content))
    elif image_base64:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
    else:
        return "No URL or Base64 data provided", 400

    img_type = get_image_type(image_data)

    # Step 3: 如果是 GIF，进行处理
    if img_type == 'GIF':
        final_image = process_gif(image)
    else:
        final_image = image

    # Step 4: OCR 识别
    step_4_start = time.time()
    text = get_text_from_image(final_image).strip()
    print(f"Step 4 - OCR Processing: {time.time() - step_4_start:.4f} seconds")

    # 总耗时
    total_time = time.time() - start_time
    print(f"Total Processing Time: {total_time:.4f} seconds")

    return text


@app.route('/v1/image/combined_gif', methods=['POST'])
def get_combined_image():
    url = request.form.get('url')
    image_base64 = request.form.get('image_base64')
    user_agent = request.form.get('useragent', 'Mozilla/5.0')

    if url:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers)
        image = Image.open(BytesIO(response.content))
    elif image_base64:
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
    else:
        return jsonify({"error": "No URL or Base64 data provided"}), 400

    img_type = get_image_type(image_data)

    if img_type == 'GIF':
        final_image = process_gif(image)
    else:
        final_image = image

    img_io = BytesIO()
    final_image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
