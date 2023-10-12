from flask import Flask, render_template, request, redirect, url_for, flash
from web_tools import is_valid_url, website_information
app = Flask(__name__)
app.secret_key = '7469817409714-97142'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/web-input', methods=['GET', 'POST'])
def web_input():
    return render_template('web_input.html')


@app.route('/image-tools')
def image_tools():
    return render_template('image_tools.html')


@app.route('/file-tools')
def file_tools():
    return render_template('file_tools.html')


@app.route('/web_tool', methods=["POST"])
def web_tool():
    user_url = request.form.get('web_input')
    ip_info, domain, title, favi = website_information(user_url)
    return render_template('web_tools.html', user_url=domain, ip_info=ip_info, title=title, favicon=favi)


if __name__ == '__main__':
    app.run(debug=True)
