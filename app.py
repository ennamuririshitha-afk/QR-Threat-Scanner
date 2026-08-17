from flask import Flask, render_template, request
from scanner import scan_qr
from analyzer import is_url, analyze_url
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# ==================================================
# UPLOAD FOLDER
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Automatically create uploads folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==================================================
# HOME
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")


# ==================================================
# ABOUT
# ==================================================

@app.route("/about")
def about():
    return render_template("about.html")


# ==================================================
# SCAN QR
# ==================================================

@app.route("/scan", methods=["POST"])
def scan():

    # ----------------------------------------------
    # Check uploaded file
    # ----------------------------------------------

    if "qr_image" not in request.files:

        return render_template(
            "result.html",
            qr_data="No file uploaded.",
            score=0,
            level="ERROR",
            reasons=["Please upload a QR Code image."],
            is_url=False
        )

    file = request.files["qr_image"]

    if file.filename == "":

        return render_template(
            "result.html",
            qr_data="No file selected.",
            score=0,
            level="ERROR",
            reasons=["Please select a QR Code image."],
            is_url=False
        )

    # ----------------------------------------------
    # Secure filename
    # ----------------------------------------------

    filename = secure_filename(file.filename)

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    # Save image
    file.save(filepath)

    print("\n================================")
    print("IMAGE SAVED:")
    print(filepath)
    print("================================\n")

    # ----------------------------------------------
    # Decode QR
    # ----------------------------------------------

    try:

        qr_data = scan_qr(filepath)

    except Exception as e:

        print("QR SCANNER ERROR:", e)

        return render_template(
            "result.html",
            qr_data="Scanner Error",
            score=0,
            level="ERROR",
            reasons=[
                "Unable to process the QR image.",
                str(e)
            ],
            is_url=False
        )

    print("\n================================")
    print("DECODED QR DATA:")
    print(qr_data)
    print("================================\n")

    # ----------------------------------------------
    # No QR Found
    # ----------------------------------------------

    if not qr_data or qr_data == "No QR Code Found":

        return render_template(
            "result.html",
            qr_data="No QR Code Found",
            score=0,
            level="NO QR FOUND",
            reasons=[
                "No QR Code was detected in this image.",
                "Please upload a clear QR Code image."
            ],
            is_url=False
        )

    # ----------------------------------------------
    # Check URL
    # ----------------------------------------------

    if not is_url(qr_data):

        return render_template(
            "result.html",
            qr_data=qr_data,
            score=0,
            level="PLAIN TEXT",
            reasons=[
                "QR Code contains plain text.",
                "No website URL was detected."
            ],
            is_url=False
        )

    # ----------------------------------------------
    # Analyze URL
    # ----------------------------------------------

    try:

        score, level, reasons = analyze_url(qr_data)

    except Exception as e:

        print("ANALYZER ERROR:", e)

        return render_template(
            "result.html",
            qr_data=qr_data,
            score=0,
            level="ANALYSIS ERROR",
            reasons=[
                "Unable to analyze this website.",
                str(e)
            ],
            is_url=True
        )

    print("\n================================")
    print("SECURITY ANALYSIS")
    print("URL       :", qr_data)
    print("RISK      :", score)
    print("THREAT    :", level)
    print("================================\n")

    # ----------------------------------------------
    # Result
    # ----------------------------------------------

    return render_template(
        "result.html",
        qr_data=qr_data,
        score=score,
        level=level,
        reasons=reasons,
        is_url=True
    )


# ==================================================
# 404 ERROR
# ==================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404


# ==================================================
# 500 ERROR
# ==================================================

@app.errorhandler(500)
def server_error(error):

    return render_template(
        "result.html",
        qr_data="Server Error",
        score=0,
        level="SERVER ERROR",
        reasons=[
            "An unexpected server error occurred."
        ],
        is_url=False
    ), 500


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    print("\n======================================")
    print("       QR THREAT SCANNER")
    print("======================================")
    print("Upload folder:")
    print(UPLOAD_FOLDER)
    print("\nServer:")
    print("http://127.0.0.1:5000")
    print("======================================\n")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )