import os
from flask import Flask, redirect, abort, render_template, jsonify, request
from models import setup_db, Actor, Movie
from flask_cors import CORS
from auth import requires_auth, AuthError
import sys

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
AUTH0_CALLBACK_URL = os.environ.get('AUTH0_CALLBACK_URL')

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #-----------view

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project. <a href=\"https://huelt.us.auth0.com/login\">Login</a>"
        return greeting

    
    @app.route('/login')
    def get_login():
      try:      
        return redirect(
          f"https://{AUTH0_DOMAIN}/authorize?"
          f"audience={API_AUDIENCE}&"
          f"response_type=token&"
          f"client_id={AUTH0_CLIENT_ID}&"
          f"redirect_uri={AUTH0_CALLBACK_URL}"
        )
      except:
        abort(422)

    @app.route('/login-results')
    def get_loginResult():
      try:      
        return render_template("callback.html")
      except:
        abort(422)

    #--------------------------------------------------for actor

    @app.route('/actors')
    def get_actors():
      try:
        actors = Actor.query.order_by(Actor.id).all()
        return jsonify({
          'success': True,
          'actors': [actor.format() for actor in actors],
        })
      except:
        abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actor')
    def create_actor(_):
      body = request.get_json()

      new_name = body.get('name')
      new_age = body.get('age')
      new_gender = body.get('gender')

      if new_age and new_gender and new_name : 
          try:
            actor = Actor(new_name, new_age, new_gender)
            actor.insert()

            return jsonify({
              'success': True,
              'created': actor.id,
            }), 201
          except:
            abort(500)
      else:
        abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(_,actor_id):
      actor = Actor.query.filter(Actor.id==actor_id).one_or_none()
      if actor is None:
        abort(404)
      else:
        try:
          actor.delete()
          return jsonify({
              "success": True,
              "actor": actor.format()
          })
        except:
          print(sys.exc_info())
          abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(_,actor_id):
      try:
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      except:
        abort(500)

      if actor is None:
        abort(404)
      else:
        body = request.get_json()

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        if new_age: 
          actor.age = new_age
        
        if new_name:
          actor.name = new_name

        if new_gender:
          actor.gender = new_gender
        
        actor.update()

        return jsonify({
          'success': True,
          'updated': actor.format(),
        })
    
    #--------------------------------------------------for movie

    @app.route('/movies')
    def get_movies():
      try:
        movies = Movie.query.order_by(Movie.id).all()
        return jsonify({
          'success': True,
          'movies': [movie.format() for movie in movies],
        })
      except:
        abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movie')
    def create_movie(_):
      body = request.get_json()

      new_title = body.get('title')
      new_release_date = body.get('release_date')
      if new_title and new_release_date:
        try: 
          movie = Movie(new_title, new_release_date)
          movie.insert()

          return jsonify({
            'success': True,
            'created': movie.id,
          }), 201
        except:
          abort(500)
      else:
        abort(422)
  
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(_,movie_id):
      try:
        movie = Movie.query.filter(Movie.id==movie_id).one_or_none()
      except:
        abort(500)
      if movie is None:
        abort(404)
      else:
        movie.delete()
        return jsonify({
            "success": True,
            "movie": movie.format()
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(_,movie_id):
      try:
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      except:
        abort(422)
          
      if movie is None:
        abort(404)
      else:
        body = request.get_json()

        new_title = body.get('title')
        new_release_date = body.get('release_date')

        if new_title: 
          movie.title = new_title
        
        if new_release_date:
          movie.new_release_date = new_release_date

        movie.update()

        return jsonify({
          'success': True,
          'updated': movie.format(),
        })

    #--------------------------------------------------for error

    @app.errorhandler(422)
    def unprocessable(error):
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def notfound(error):
      return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not found"
        }), 404
    
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
      return jsonify({
          "success": False,
          "error": ex.status_code,
          "message": ex.error['description']
      }), ex.status_code
    
    @app.errorhandler(500)
    def serverError(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
      }), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
