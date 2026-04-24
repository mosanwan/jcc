"""本地 OCR — 识别数字和简单文本"""

import cv2
import numpy as np


def preprocess_for_ocr(img: np.ndarray) -> np.ndarray:
    """预处理：灰度 → 二值化，提高 OCR 准确率"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def crop_zone(img: np.ndarray, zone: tuple) -> np.ndarray:
    """从全屏截图中裁剪指定区域 (x, y, w, h)"""
    x, y, w, h = zone
    return img[y:y + h, x:x + w]


def recognize_number(img: np.ndarray, zone: tuple) -> int | None:
    """识别指定区域内的数字

    先用本地模板匹配，后续可接入 OCR 引擎。
    目前用 Tesseract 作为 fallback。
    """
    cropped = crop_zone(img, zone)
    processed = preprocess_for_ocr(cropped)

    try:
        import pytesseract
        text = pytesseract.image_to_string(
            processed,
            config="--psm 7 -c tessedit_char_whitelist=0123456789",
        )
        text = text.strip()
        return int(text) if text.isdigit() else None
    except ImportError:
        # pytesseract 未安装，返回 None
        return None
    except ValueError:
        return None


def recognize_text(img: np.ndarray, zone: tuple) -> str:
    """识别指定区域内的文本"""
    cropped = crop_zone(img, zone)
    processed = preprocess_for_ocr(cropped)

    try:
        import pytesseract
        text = pytesseract.image_to_string(processed, lang="chi_sim+eng", config="--psm 7")
        return text.strip()
    except ImportError:
        return ""
