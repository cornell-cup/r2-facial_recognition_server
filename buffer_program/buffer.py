import socket
import sys
import glob
import shutil
import os

# get image from the Rasberry Pi via socket
def get_image():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()
    print('Socket Created')

    host = '192.168.4.148'
    port = 6000

    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    # Connect to remote server
    s.connect((remote_ip , port))
    print('Socket Connected to ' + host + ' on ip ' + remote_ip)

    filename = open('camerashot.jpg', 'wb')
    while True:
        strng = s.recv(1024)
        if not strng:
            break
        filename.write(strng)

    filename.close()
    print('received, yay!')

    s.close()

# Copy images to fr_program dir: need to change after figuring out the address
def changeDir():
    src_dir = "source_directory"
    dst_dir = "destination_directory"
    for jpgfile in glob.iglob(os.path.join(src_dir, "*.jpg")):
        shutil.copy(jpgfile, dst_dir)

#remove unwanted images from the buffer_program dir
def removeIm():
    for i in glob.glob("*.jpg"):
        os.remove(i)

def main():
    get_image()

