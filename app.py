import os
import subprocess
import sys

# প্রয়োজনীয় লাইব্রেরি অটো-ইনস্টল করার ফাংশন
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# লাইব্রেরিগুলো চেক এবং ইনস্টল
try:
    from flask import Flask, request, send_file, jsonify
    from rembg import remove
    from PIL import Image
except ImportError:
    print("Installing dependencies... Please wait.")
    install('flask')
    install('rembg')
    install('pillow')
    from flask import Flask, request, send_file, jsonify
    from rembg import remove
    from PIL import Image

import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Background Remover API is Running!"

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    file = request.files['image']
    try:
        input_image = Image.open(file.stream)
        output_image = remove(input_image)
        
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # সার্ভার পোর্ট সেটআপ
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

