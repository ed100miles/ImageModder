from app import app
from flask import render_template, request, redirect, jsonify, make_response
import cv2 
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from app import imgMods

@app.route('/')
def index():
    return redirect('/upload-image')

@app.route('/upload-image', methods=['POST', 'GET'])
def uploadimage():
    ok_file_exts = ['jpg', 'jpeg', 'png', 'gif', 'JPG', 'JPEG', 'PNG', 'GIF']
    wrong_ext = False
    if request.method == 'POST':
        try:
            image = request.files['image']
            if image.filename != '' and image.filename.split('.')[-1] in ok_file_exts:
                img = image.read()
                base_img = imgMods.upload_img_to_base64(img)
                return render_template('upload-image.html', image=base_img)
            else:
                wrong_ext = True
                return render_template('upload-image.html', wrong_ext = wrong_ext)
        except Exception as e:
            print(e)
        # else opencv performs operations on the existing image
        req = request.get_json()
        if req != None:
            ####### BGR RGB HACKY FIX  --- NEEDS PROPPER FIX ####
            blueness_val = float(req['redness'])
            redness_val = float(req['blueness'])
            greenness_val = float(req['greenness'])
            brightness_val = float(req['brightness'])
            saturation_val = float(req['saturation'])
            blur_sharp_val = float(req['blur_sharp'])
            rotation_val = int(req['rotation'])
            image_base64_str = req['img']
            # Base64 str to nparr so can perform opencv operations
            # print(rotation_val)
            img = imgMods.b64_to_nparr(image_base64_str)
            
            mod_img = imgMods.bgr_intensity(img, blueness_val, greenness_val, redness_val)
            mod_img = imgMods.brightness_saturation_mod(mod_img, brightness_val, saturation_val)
            mod_img = imgMods.blur_sharp_mod(mod_img, blur_sharp_val)
            mod_img = np.rot90(mod_img, -rotation_val)

            mod_img_b64 = imgMods.np_img_to_b64(mod_img)
            json_response = make_response(jsonify(mod_img_b64), 200)
            return json_response
    return render_template('upload-image.html')


