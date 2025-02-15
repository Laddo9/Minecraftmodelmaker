from flask import Flask, request, send_file, jsonify
from PIL import Image
import json
import numpy as np
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return "Minecraft 2D to 3D Model Converter API is running!"

@app.route("/convert", methods=["POST"])
def convert_to_3d():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    image = Image.open(file_path).convert("RGBA")
    width, height = image.size
    pixels = np.array(image)

    model_json = {
        "format_version": "1.12.0",
        "minecraft:geometry": [
            {
                "description": {
                    "identifier": "geometry.custom_model",
                    "texture_width": width,
                    "texture_height": height,
                    "visible_bounds_width": width / 16,
                    "visible_bounds_height": height / 16,
                    "visible_bounds_offset": [0, height / 32, 0]
                },
                "bones": []
            }
        ]
    }

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[y, x]
            if a == 0:
                continue

            cube = {
                "name": f"pixel_{x}_{y}",
                "pivot": [x - width / 2, -y + height / 2, 0],
                "cubes": [
                    {
                        "origin": [x - width / 2, -y + height / 2, 0],
                        "size": [1, 1, 1],
                        "uv": [x, y],
                    }
                ]
            }
            model_json["minecraft:geometry"][0]["bones"].append(cube)

    output_path = os.path.join(UPLOAD_FOLDER, "minecraft_model.json")
    with open(output_path, "w") as json_file:
        json.dump(model_json, json_file, indent=4)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
