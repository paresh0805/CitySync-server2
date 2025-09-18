from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 📂 Folder to store uploaded images
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/issue", methods=["POST"])
def report_issue():
    try:
        description = request.form.get("description")
        location = request.form.get("location")
        citizen_id = request.form.get("citizenId")
        issue_type = request.form.get("issueType")
        image = request.files.get("image")

        if not description or not location or not citizen_id or not image:
            return jsonify({"success": False, "message": "Missing required fields"}), 400

        # Save uploaded image
        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        # You can insert issue details into DB here instead of just printing
        print("📌 New Issue Reported:")
        print("Citizen ID:", citizen_id)
        print("Location:", location)
        print("Issue Type:", issue_type)
        print("Description:", description)
        print("Image saved at:", filepath)

        return jsonify({
            "success": True,
            "message": "Issue reported successfully",
            "data": {
                "citizenId": citizen_id,
                "location": location,
                "issueType": issue_type,
                "description": description,
                "imagePath": filepath
            }
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"success": False, "message": "Server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

