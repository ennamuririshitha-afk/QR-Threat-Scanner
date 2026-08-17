import cv2


def scan_qr(image_path):

    detector = cv2.QRCodeDetector()

    image = cv2.imread(image_path)

    if image is None:
        return "No QR Code Found"

    data, points, _ = detector.detectAndDecode(image)

    if data:
        return data.strip()

    return "No QR Code Found"