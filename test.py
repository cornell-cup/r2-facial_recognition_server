import requests

url = "http://127.0.0.1:5000/identify-face"

def test_request():
    files = {
        "image": open("stanley.png", "rb")
    }
    requests.post(url, files=files, verify=False)

test_request()

