from app import app
from flask import render_template, request, redirect, jsonify, make_response
import cv2 
import numpy as np
import base64
from app import imgMods

app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

@app.route('/')
def index():
    return redirect('/upload-image')

@app.route('/upload-image', methods=['POST', 'GET'])
def uploadimage():
    if request.method == 'POST':
        try:
            ok_file_exts = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
            wrong_ext = False
            image = request.files['image']
            if image.filename != '' and image.filename.split('.')[-1] in ok_file_exts:
                img = image.read()
                base_img = imgMods.upload_img_to_base64(img)
                return render_template('upload-image.html', image=base_img)
            else:
                wrong_ext = True
                return render_template('upload-image.html', wrong_ext = wrong_ext)
        except Exception as e: # TODO: fix this awful exception handling!!!
            if str(e)[:3] == '413': # if 413 - if Req Entity Too Large:
                return render_template('upload-image.html', big_file=True)
            else:
                print(repr(e))
        # else imgMods performs operations on the existing image:
        req = request.get_json()
        if req != None:
            return imgMods.process_request(req)
    return render_template('upload-image.html')

