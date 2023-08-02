from flask import Flask, render_template
import os

FOLDER = os.path.join('static','images')
print(FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = FOLDER

@app.route('/')
@app.route('/index')
def show_index():


    image_names = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f))]
    latest_image = max(image_names, key=lambda f: os.path.getmtime(os.path.join(FOLDER, f)))
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], latest_image)
    return render_template("index.html", user_image = full_filename)


if __name__ == "__main__":
    app.run('0.0.0.0')



    