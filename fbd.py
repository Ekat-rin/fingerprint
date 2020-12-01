from processing_request import app
from fingerprint import fingerprint_app, HOST_PORT

if __name__ == '__main__':
    app.run(debug=True)
    fingerprint_app.run(HOST_PORT, debug=True)
