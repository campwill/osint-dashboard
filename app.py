from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template, request as flask_request, redirect, url_for, flash
import os
from web_tools import *
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()
secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key


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
    user_url = flask_request.form.get('web_input')
    domain, ip_str, title, favi = website_information(user_url)
    cookies = get_cookies(user_url)
    headers = get_headers(user_url)
    ip_info = get_ip_info(ip_str)
    dns_records = get_records(domain)
    ssl_cert = get_ssl(domain)
    large_json = {
        "ip_info": ip_info if ip_info else {},
        "cookies": cookies if cookies else {},
        "headers": headers if headers else {},
        "dns_records": dns_records if dns_records else {},
        "ssl_info": ssl_cert if ssl_cert else {}
    }
    print(json.dumps(large_json))
    return render_template('web_tools.html', user_url=domain, ip_info=ip_str, title=title, favicon=favi, web_info=json.dumps(large_json))


if __name__ == '__main__':
    app.run(debug=True)
