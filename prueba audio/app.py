from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///song.db'
db = SQLAlchemy(app)

class Portafolio(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    song = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Song %r' % self.id

@app.route("/", methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        song_title = request.form['name']
        song_link = request.form['song']
        
        new_song = Portafolio(name = song_title, song = song_link)

        try:
            db.session.add(new_song)
            db.session.commit()
            return redirect('/')

        except:
            return 'no c pudo'

    else:
        songs = Portafolio.query.order_by(Portafolio.date_created).all()
        return render_template('index.html', songs=songs)

@app.route('/delete/<int:id>')
def delete(id):
    song_to_delete = Portafolio.query.get_or_404(id)

    try:
        db.session.delete(song_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'no c pudo'

@app.route('/admin', methods = ['POSt','GET'])
def auten():
    if request.method == 'POST':
        u_key = request.form['key']
        key = 'hola'
        if u_key == key:
            return redirect('/admin_song')

    else:
        return render_template('admin.html')

@app.route('/admin_song')
def admin_song():
    return render_template('admin_pa.html')

if __name__ == "__main__":
    app.run(debug = True)