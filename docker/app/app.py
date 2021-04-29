import sqlite3

from flask import Flask, Response, render_template, request, flash, redirect, url_for, make_response
from flask_caching import Cache

import bleach
import markdown

import urllib
import pycurl

from io import BytesIO
import docker

from datetime import datetime
from time import sleep

from bleach.sanitizer import Cleaner
from bleach_whitelist import markdown_tags, markdown_attrs
from bleach.html5lib_shim import Filter

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

class LinkFilter(Filter):
    def __iter__(self):
        for token in Filter.__iter__(self):
            if token['type'] in ['StartTag', 'EmptyTag'] and token['data']:
                for attr, value in token['data'].items():
                    if attr[1] == 'src':
                        src = '/safeImage?url=' + urllib.parse.quote_plus(token['data'][attr])
                        token['data'][attr] = src
            yield token

cleaner = Cleaner(tags=markdown_tags, attributes=markdown_attrs, filters=[LinkFilter])

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis', "DEBUG": True, 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

app.config['SECRET_KEY'] = 'the random string'    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status')
def status():
    containers = client.containers.list(all=True)
    return render_template('status.html', containers=containers)

@app.route('/log')
def captainslog():
    conn = get_db_connection()
    db_notes = conn.execute('SELECT id, created, content FROM notes ORDER BY created DESC LIMIT 10;').fetchall()
    conn.close()
    
    cached = cache.get('all_notes')
    if cached:
        notes = cached
    else:
        notes = []
        for note in db_notes:
            note = dict(note)
            note['content'] = cleaner.clean(markdown.markdown(note['content']))
            notes.append(note)
        cache.set('all_notes', notes, timeout=300)
    return render_template('log.html', notes=notes)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    conn = get_db_connection()

    if request.method == 'POST':
        content = request.form['content']
        if not content:
            flash('Content is required!')
            return redirect(url_for('create'))
        conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        conn.commit()
        conn.close()
        cache.delete('all_notes')
        return redirect(url_for('captainslog'))

    return render_template('create.html')
    
@app.route('/safeImage/', methods=('GET', 'POST'))
def safeImage():
    url = request.args.get('url')
    c = pycurl.Curl()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.TIMEOUT_MS, 5000)
    body_writer = BytesIO()
    head_writer = BytesIO()
    c.setopt(pycurl.WRITEFUNCTION, body_writer.write)
    c.setopt(pycurl.HEADERFUNCTION, head_writer.write)
    result = {}
    
    # try / catch for timeout error 
    try: 
        c.perform()
        head_writer.seek(0)
        first = head_writer.readline()
        result['header'] = {}
        for line in head_writer:
            parts = line.decode('UTF-8').split(':' , 1)
            if len(parts) == 2:
                result['header'][parts[0]] = parts[1].strip()
        result['code'] = c.getinfo(pycurl.HTTP_CODE) 
        result['body'] = body_writer.getvalue()
        
        print(result['header'])
        
        response = make_response(result['body'])
        if 'content-type' in result['header']:
            response.headers['Content-Type'] = result['header']['content-type']
    except pycurl.error:
        response = make_response(body_writer.getvalue()) 

    return response

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')