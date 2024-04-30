import os
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_path = os.path.join("C:/Users/chern/KURSOVAYA/Decision-support-system/src", file.filename)

    # Save the file to disk
    file.save(file_path)

    # Return the file name as a JSON response
    return {"filename": file.filename}

if __name__ == "__main__":
    app.run()