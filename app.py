# -----Imports-----
import os
import uuid

# from UseModel import get_prediction
from CreateFrames import gen_frames
from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
from json import JSONEncoder
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# -----Load environmental variables-----
load_dotenv()

# -----App initalization-----
app = Flask(__name__)
CORS(app)

# -----API endpoints-----
# Main
@app.route('/')
def main():
    return render_template('index.html')

# Video
@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Get prediction
# @app.route('/predict', methods=['POST'])
# def pedict():
#     # Variables
#     final = ""

#     # Validate the image file
#     if "file" not in request.files:
#         return jsonify({"error": "Image not provided"}), 400
#     file = request.files["file"]
#     if file.filename == "":
#         return jsonify({"error": "No image selected"}), 400
    
#     # Generate a secure unique file name
#     filename = uuid.uuid4().hex+"_"+secure_filename(file.filename)

#     # Save the file
#     file.save(os.path.join(os.getenv("UP_DIR"), filename))

#     # Get the prediction
#     prediction = get_prediction(os.getenv("UP_DIR")+filename)

#     if prediction == 0:
#         final = "Color Dot"
#     elif prediction == 1:
#         final = "Color Patch"
#     else:
#         final = "Original"

#     return jsonify({"result": final}), 200

# -----Execute the app-----
if __name__ == "__main__":
    app.run(host="0.0.0.0")