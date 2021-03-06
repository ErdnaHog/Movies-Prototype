from flask import Blueprint
from flask import render_template, request, redirect, url_for, Markup, jsonify, flash
from flask_login import current_user, login_required
from package.movie.forms import CreateMovieForm, ModifyMovieForm
from package.movie.classes import Movie
from package.user.classes import Admin
from package.movie.utilis import save_picture, save_video
from package.utilis import check_admin, check_rights
import shelve, datetime

movie_blueprint = Blueprint("movie", __name__)

#* User Movie

@movie_blueprint.route("/movie/<movie_id>")
def movie_detail(movie_id):
    movie_id = movie_id
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]        
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    movie_class = Movies_dict[movie_id]
    try:
        current_user.get_email()
        user_logged = True
    except:
        user_logged = False
    Rental_dict = db["rental"]
    rent_status = False
    for rental in Rental_dict.values():
        print(movie_class, rental.get_movie_class())
        if rental.get_movie_class().get_movie_name() == movie_class.get_movie_name():
            rent_price = rental.get_price()
            rent_status = True
            break
    return render_template("User 2/detail.html", title=movie_class.get_movie_name(), movie=movie_class, user_logged=user_logged)


#* Admin Promotion
@movie_blueprint.route("/admin/movies")
@login_required
def admin_movies():
    check_admin()
    check_rights()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    db.close()
    return render_template("Admin/movie/movies.html", title="Movies", Movies_dict=Movies_dict)

@movie_blueprint.route("/admin/movie/<movie_id>")
def admin_movie_detail(movie_id):
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    db.close()
    movie_class = Movies_dict[movie_id]
    return render_template("Admin/movie/movie_detail.html", title="Movie Detail", movie_class=movie_class)

@movie_blueprint.route("/admin/movies/add_movie", methods=["POST","GET"])
@login_required
def add_movie():
    check_admin()
    check_rights()
    form = CreateMovieForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
        Movie.id = list(Movies_dict.values())[-1].get_id()
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    genre_list = db["genre_list"]    
    form.movie_genre.choices = genre_list
    if request.method =="POST" and form.validate_on_submit():        
        movie_name = form.movie_name.data
        movie_poster = save_picture(form.movie_poster.data, "movie poster")
        movie_description = form.movie_description.data
        movie_genre = form.movie_genre.data        
        movie_casts = form.movie_casts.data
        movie_director = form.movie_director.data
        movie_fullvideo = save_video(form.movie_fullvideo.data, "movie fullvideo")
        movie_trailer = save_video(form.movie_trailer.data, "movie trailer")
        movie_duration = form.movie_duration.data
        movie_release_date = form.movie_release_date.data
        # date
        month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        year, month, day = str(movie_release_date).split('-')
        movie_release_date = day + " " + month_list[int(month)-1] + " " + year
        movie_language = form.movie_language.data
        movie_subtitles = form.movie_subtitles.data
        movie_class = Movie(movie_name, movie_poster, movie_description, movie_genre, movie_casts, movie_director, movie_fullvideo, movie_trailer, movie_duration, movie_release_date, movie_language, movie_subtitles)
        movie_id = movie_class.get_id()    
        Movies_dict[movie_id] = movie_class
        db["movies"] = Movies_dict        
        db.close()
        flash("Movie has been added !", "success")
        return redirect(url_for("movie.admin_movies"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Some field(s) are incorrect. Please try again", "danger")
    elif request.method == "GET":
        form.movie_name.data = ""
        form.movie_description.data = ""
        form.movie_genre.data = ""
        form.movie_casts.data = ""
        form.movie_director.data = ""
        form.movie_duration.data = ""
        form.movie_release_date.data = ""
        form.movie_language.data = "English"
        form.movie_subtitles.data = "Chinese"
        db.close()        
    return render_template("Admin/movie/add_movie.html", title="Add Movie", form=form)

@movie_blueprint.route("/admin/movies/modify_movie/<movie_id>", methods=["POST", "GET"])
@login_required
def modify_movie(movie_id):
    check_admin()
    check_rights()
    movie_id = movie_id
    form = ModifyMovieForm()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
    except:
        Movies_dict = {}
        db["movies"] = Movies_dict
    genre_list = db["genre_list"]
    form.movie_genre.choices = genre_list
    movie_class = Movies_dict[movie_id]
    fullvideo_source = movie_class.get_movie_fullvideo()
    trailer_source = movie_class.get_trailer()
    image_source = movie_class.get_poster()
    if form.validate_on_submit():
        movie_name = form.movie_name.data
        movie_poster = save_picture(form.movie_poster.data, "movie poster")
        movie_description = form.movie_description.data
        movie_genre = form.movie_genre.data
        movie_casts = form.movie_casts.data
        movie_director = form.movie_director.data
        movie_fullvideo = save_video(form.movie_fullvideo.data, "movie fullvideo")
        movie_trailer = save_video(form.movie_trailer.data, "movie trailer")
        movie_duration = form.movie_duration.data
        movie_release_date = form.movie_release_date.data
        # date
        month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        year, month, day = str(movie_release_date).split('-')
        movie_release_date = day + " " + month_list[int(month)-1] + " " + year
        movie_language = form.movie_language.data
        movie_subtitles = form.movie_subtitles.data
        movie_class = Movies_dict[movie_id]
        movie_class.set_all_attributes(movie_name, movie_poster, movie_description, movie_genre, movie_casts, movie_fullvideo, movie_trailer, movie_duration, movie_release_date, movie_language, movie_subtitles, movie_director)
        Movies_dict[movie_id] = movie_class
        db["movies"] = Movies_dict        
        db.close()
        flash("Movie has been modified !", "success")
        return redirect(url_for("movie.admin_movies"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("Some field(s) are incorrect. Please try again", "danger")
    elif request.method == "GET":        
        form.movie_name.data = movie_class.get_movie_name()        
        form.movie_description.data = movie_class.get_description()
        form.movie_genre.data = movie_class.get_genre_list()
        form.movie_casts.data = movie_class.get_casts()
        form.movie_director.data = movie_class.get_director()        
        form.movie_duration.data = movie_class.get_duration()
        day, month, year = movie_class.get_release_date().split(" ")
        month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        movie_release_date = year + '-' + str(month_list.index(month)+1) + '-' + day
        form.movie_release_date.data = movie_release_date
        form.movie_language.data = movie_class.get_language()
        form.movie_subtitles.data = movie_class.get_subtitles()
    return render_template("Admin/movie/modify_movie.html", title="Modify Movie Theatre", form=form, image_source=image_source, trailer_source=trailer_source, fullvideo_source=fullvideo_source)

@movie_blueprint.route("/admin/movies/delete", methods=["POST","GET"])
@login_required
def delete_movie():
    check_admin()
    check_rights()
    db = shelve.open('shelve.db', 'c')
    try:
        Movies_dict = db["movies"]
        Deleted_list = db["deleted_movies"]
    except:
        Movies_dict = {}
        Deleted_list = []
        db["movies"] = Movies_dict
        db["deleted_movies"] = Deleted_list
    list_of_to_be_deleted_movies = request.json
    for movie_id in list_of_to_be_deleted_movies:
        delete_movie = Movies_dict[movie_id]        
        Deleted_list.append([delete_movie, datetime.date.today()])
        del Movies_dict[movie_id]
    db["movies"] = Movies_dict
    db["deleted_movies"] = Deleted_list
    db.close()
    return redirect(url_for("movie.admin_movies"))

@movie_blueprint.route("/get_video/<movie_id>", methods=["POST","GET"])
def get_video(movie_id):
    db = shelve.open('shelve.db', 'c')    
    Movies_dict = db["movies"]
    movie_class = Movies_dict[movie_id]
    video_source = movie_class.get_trailer()
    print(video_source)
    return jsonify(video_source)