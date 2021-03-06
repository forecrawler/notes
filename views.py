# -*- coding: utf-8 -*-

from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from flask import abort, jsonify, render_template, request, redirect, url_for, session
from app import app
from models import Note

#@app.route('/post', methods=['POST'])
#def post():
#    if not session.get('logged_in'):
#        abort(401)
#    if request.method == 'POST':
#        if request.form.get('content') and request.form.get('title'):
#            title = request.form['title']
#            content = request.form['content']
#            note = Note(title=title, content=content)
#            note.save()
#            return redirect(url_for('index'))
#    return redirect(url_for('add'))


@app.route('/add',methods=['GET', 'POST'])
def add():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form.get('title') and request.form.get('content'):
            title = request.form['title']
            content = request.form['content']
            note = Note(title=title, content=content)
            note.save()
            return redirect(url_for('index'))
    else:
        return render_template('add.html')


@app.route('/detail/<id>')
def detail(id):
    note = Note.objects(id=id)
    return render_template('detail.html', note=note)
#@app.route('/manage', methods=['GET'])
#def manage():
#    notes = Note.objects()
#    return render_template('manage.html', notes=notes)

@app.route('/')
def index():
    notes = Note.objects(archived=False)
    return render_template('index.html', notes=notes)

#@app.route('/archive/<id>',methods=['POST'])
#def archive_note(id):
#    try:
#        Note.objects(id=id).update(set__archived=True)
#    except Note.DoesNotExist:
#        abort(404)
#    return jsonify({'success': True})

#@app.route('/delete/<id>', methods=['POST'])
#def delete(id):
#    try:
#       Note.objects(id=id).delete() 
#    except Note.DoesNotExist:
#        abort(404)
#    return jsonify({'success': True})

@app.route('/login',methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('add'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin@admin.com':
            error = 'Invalid username'
        elif request.form['password'] != 'admin':
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            return redirect(url_for('add'))
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/rss')
def rss():
    feed = AtomFeed('Recent Aiticles',
            feed_url=request.url, url=request.url_root)
    notes = Note.objects.all()
    for note in notes:
        feed.add(note.title,
                note.content,
                content_type='html',
                author="KMLG",
                #url=note.detail(),
                id=note.id,
                updated=note.timestamp,
                #published=post.pub_date
                )
    return feed.get_response()
