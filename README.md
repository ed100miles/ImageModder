# **ImageModder**
## Flask app for modifying images

### [Open in Heroku](https://imagemodder.herokuapp.com/)

---

## What does it do?

A flask app hosted on Heroku that allows the user to upload an image file and then perform a variety of opperations on their origional image. Operations include changing the brightness, saturation, blur/sharpness, orientation and intensity of red, green and blue colours. 

---

## How does it work?
The user choses an image to upload, this image is sent to the server, converted to a base64 string and sent back to the client side to be rendered. 

Sliders then appear to change values for different operations to perform on the image. When a slider value is changed, the imgMod() function in the app.js file is called. The values of the different image operation sliders, and the origional image base64 string, are sent as JSON via the Fetch API to the server. The server then converts the image base64 to a numpy array. The opencv-python library is then used to perform the various image operations on the numpy array. The array is then converted back to a base64 string and sent as a response back to the client, where the new string is rendered. The Fetch API alows this process to happen asynchronusly.  
