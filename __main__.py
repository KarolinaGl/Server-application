import flask
import werkzeug

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    image_file = flask.request.files['image']
    filename = werkzeug.utils.secure_filename(image_file.filename)
    print("\nReceived image file name: " + image_file.filename)
    image_file.save(filename)
    return "Image uploaded successfully"


app.run(host="0.0.0.0", port=5000, debug=True)
