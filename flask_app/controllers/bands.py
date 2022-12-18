from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.band import Band
from flask_app.models.user import User


@app.route('/new/band')
def new_band():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_band.html',user=User.get_by_id(data))


@app.route('/create/band',methods=['POST'])
def create_band():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Band.validate_bands(request.form):
        return redirect('/new/band')
    data = {
        "name": request.form["band_name"],
        "genre": request.form["band_genre"],
        "city": request.form["home_city"],
        "user_id": session["user_id"]
    }
    Band.save(data)
    return redirect('/dashboard')

@app.route('/edit/band/<int:id>')
def edit_band(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_band.html",band=Band.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/band',methods=['POST'])
def update_band():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Band.validate_bands(request.form):
        return redirect(f"/edit/band/{request.form['id']}")
    data = {
        "name": request.form["band_name"],
        "genre": request.form["band_genre"],
        "city": request.form["home_city"],
        "id": request.form['id']
    }
    Band.update(data)
    return redirect('/dashboard')

@app.route('/mybands')
def show_band():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        "id":session['user_id']
    }
    return render_template("mybands.html", user_bands = Band.get_user_bands(user_data), user=User.get_by_id(user_data))

@app.route('/destroy/band/<int:id>')
def destroy_band(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Band.destroy(data)
    return redirect('/dashboard')