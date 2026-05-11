import easyocr

# Force EasyOCR to use CPU instead of CUDA/GPU
reader = easyocr.Reader(['en'], gpu=False)


def extract_text_from_image(image_path: str):

    results = reader.readtext(image_path)

    extracted_text = []

    confidence_scores = []

    for detection in results:

        # detection format:
        # (bbox, text, confidence)

        _, text, confidence = detection

        extracted_text.append(text)

        confidence_scores.append(confidence)

    final_text = " ".join(extracted_text)

    avg_confidence = (
        sum(confidence_scores) / len(confidence_scores)
        if confidence_scores else 0
    )

    return {
        "text": final_text,
        "confidence": round(avg_confidence, 2),
        "method": "easyocr"
    }