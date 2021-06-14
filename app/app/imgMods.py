import cv2 
import numpy as np
import base64
from PIL import Image
from io import BytesIO
from app import imgMods

def upload_img_to_base64(img):
    '''Decode img from bytes to np.array. Then convert to base64str'''
    nparr = np.fromstring(img, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #bgr to rgb:
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    #convert np array to pil img, then pil img to base64
    pil_img = Image.fromarray(img_np)
    output_buffer = BytesIO()
    pil_img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base_img = str(base64.b64encode(byte_data))
    return base_img[2:-1]

def b64_to_nparr(base64str):
    return np.array(Image.open(BytesIO(base64.b64decode(base64str))).convert('RGB'))

def arr_to_uint8_225_max(arr):
    arr[arr>255] = 255
    return arr.astype('uint8')

def bgr_intensity(img, blueness_val, greenness_val, redness_val):
    b, g, r = cv2.split(img)
    b = np.rint(b * blueness_val).astype('uint16')
    g = np.rint(g * greenness_val).astype('uint16')
    r = np.rint(r * redness_val).astype('uint16')
    b = arr_to_uint8_225_max(b)
    g = arr_to_uint8_225_max(g)
    r = arr_to_uint8_225_max(r)
    return cv2.merge((b,g,r))

def np_img_to_b64(img_np):
    pil_img = Image.fromarray(img_np)
    output_buffer = BytesIO()
    pil_img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base_img = str(base64.b64encode(byte_data))
    return base_img[2:-1]

def brightness_saturation_mod(img, brightness_val, saturation_val):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    s = np.rint(s * saturation_val).astype('uint16')
    v = np.rint(v * brightness_val).astype('uint16')
    s = arr_to_uint8_225_max(s)
    v = arr_to_uint8_225_max(v)
    hsv_mod = cv2.merge((h,s,v))
    return cv2.cvtColor(hsv_mod, cv2.COLOR_HSV2BGR) 

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=0.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask.
    Full disclosure, this is stolen from:
    https://stackoverflow.com/questions/4993082/how-can-i-sharpen-an-image-in-opencv"""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def blur_sharp_mod(mod_img, blur_sharp_val):
    if blur_sharp_val > 0:
        mod_img = imgMods.unsharp_mask(mod_img, amount=blur_sharp_val)
    if blur_sharp_val < 0:
        for i in range(round(abs(blur_sharp_val))):
            kernel = (5,5)
            mod_img = cv2.GaussianBlur(mod_img, kernel, 0)
    return mod_img