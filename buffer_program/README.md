# r2-facial_recognition_server buffer program
Arthor Rong Tan, Stanley Lin
This program is part of the R2 facial recognition server code.

### Description
It serves as a Buffer program in Java. And this program is always listening to the web socket.

### Input
There are two thread that the program is running.
For the first thread, there is a constantly-listening program, which will listen to the web socket from the client program 1 to receive face image
For the first thread, there is a constantly-listening program, which will listen to the web socket from the facial recognition program to receive JSON

### Function 
For the first thread, we want to get the face image, preprocess it, and send to the facial recognition program. 
For the second thread, we want to get the JSON, preprocess it, and send to Client Program 2. 