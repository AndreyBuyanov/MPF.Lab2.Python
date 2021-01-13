from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from jinja2_base64_filters import jinja2_base64_filters
import base64
import os
from pathlib import Path
from models.urls import Urls


app = Flask(__name__)
app.jinja_options['extensions'].append('jinja2_base64_filters.Base64Filters')


@app.route('/')
@app.route('/index')
def main():
    urlsList = Urls.getUrlsList()
    return render_template('index.html', urlsList=urlsList)


@app.route('/go/<url>')
def go(url):
    realUrl = base64.b64decode(url).decode('utf-8')
    Urls.incrementUrl(realUrl)
    return redirect(realUrl)


def isAdminLogged():
    lock = Path("/tmp/admin.lock")
    return lock.is_file()


@app.route('/admin')
@app.route('/admin/index')
def admin():
    if isAdminLogged():
        urlsList = Urls.getUrlsList()
        return render_template('admin.html', urlsList=urlsList)
    else:
        return redirect('/admin/login')


@app.route('/admin/url/add', methods=['POST'])
def addUrl():
    if isAdminLogged():
        url = request.form.get('url')
        if url:
            Urls.addUrl(url)
        return redirect('/admin')
    else:
        return redirect('/admin/login')


@app.route('/admin/url/remove/<url_id>')
def removeUrl(url_id):
    if isAdminLogged():
        Urls.removeUrlById(int(url_id))
        return redirect('/admin')
    else:
        return redirect('/admin/login')


@app.route('/admin/login', methods=['GET', 'POST'])
def adminLogin():
    if isAdminLogged():
        return redirect('/admin')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        if login == 'admin' and password == 'admin':
            try:
                lock = open("/tmp/admin.lock", "w")
            finally:
                lock.close()
            return redirect('/admin')
        else:
            return render_template('login.html')


@app.route('/admin/logout')
def adminLogout():
    os.remove("/tmp/admin.lock")
    return redirect('/admin')
