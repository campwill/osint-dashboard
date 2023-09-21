from flask import Flask, render_template, request, redirect, url_for, flash
from web_tools import is_valid_url
app = Flask(__name__)
app.secret_key = 'Secret-Key???'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/web-input', methods=['GET', 'POST'])
def web_input():
    if request.method == 'POST':
        user_url = request.form.get('web_input')
        if is_valid_url(user_url):
            return render_template('web_tools.html', user_url=user_url)
        else:
            return render_template('web_input.html', error=True)
    else:
        return render_template('web_input.html', error=False)


@app.route('/image-tools')
def image_tools():
    return render_template('image_tools.html')


@app.route('/file-tools')
def file_tools():
    return render_template('file_tools.html')


@app.route('/web_tool')
def web_tool():

    return render_template('web_tools.html')


if __name__ == '__main__':
    app.run(debug=True)
