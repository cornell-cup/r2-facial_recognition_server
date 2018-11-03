import socket
import sys
#added
import glob
import shutil
import os

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

#Connect to remote server
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
