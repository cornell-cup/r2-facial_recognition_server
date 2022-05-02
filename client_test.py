from requests import post
import cv2
import time
import json

im = cv2.imread('Christopher_De Jesus.jpg')


im = cv2.resize(im, (0, 0), fx=0.25, fy=0.25)

cv2.imshow('Image pre-detection', im)

print('Starting')
start = time.time()
r = post('http://127.0.0.1:5000/face_recognition/detect',
         files={
             'image': im.tobytes()
         }, data={'shape': str(im.shape)}
         )
end = time.time()
print(f'Took {end-start}s to complete the task.')
results = json.loads(r.content.decode('utf-8'))
print(r, r.status_code, results)
name = results['matches'][0]

cv2.putText(im, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

cv2.imshow('Image post-detection', im)
cv2.waitKey(0)
