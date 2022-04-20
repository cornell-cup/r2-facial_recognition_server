from requests import post
import cv2

im = cv2.imread('r2_facial_recognition/server/uploads/Christopher_De Jesus.jpeg')

im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

r = post('http://127.0.0.1:5000/face_recognition/detect',
     files={
         'image': im.tobytes()
     }, data={'shape': str(im.shape)})

print(r, r.status_code)
