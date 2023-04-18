from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe_model import Recipe

@app.route( "/recipes", methods=["GET"] )
def get_recipes():
    if "user_id" not in session:
        return redirect( "/")
    all_recipes = Recipe.get_all_with_users()
    return render_template( "recipes.html", all_recipes = all_recipes )

@app.route( "/recipe/form", methods=["GET"] )
def display_recipe_form():
    if "user_id" not in session:
        return redirect( "/")
    return render_template( "recipe_form.html" )

@app.route( "/recipe/new", methods=["POST"] )
def add_recipe():
    data = {
        **request.form,
        "user_id" : session["user_id"]
    }
    if Recipe.validate_recipe( data ) == False:
        return redirect( "/recipe/form" )
    Recipe.create_one( data )
    return redirect( "/recipes" )

@app.route( "/recipe/<int:id>", methods = ['GET'])
def show_recipe(id):
    if "user_id" not in session:
        return redirect( "/" )
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_recipe_with_user( data )
    return render_template( "show.html", current_recipe = current_recipe )

@app.route( "/recipe/remove/<int:id>", methods=["POST"] )
def delete_recipe( id ):
    data = {
        "id" : id
    }
    Recipe.delete_one( data )
    return redirect( "/recipes" )

@app.route( "/recipe/<int:id>/edit", methods=["GET"] )
def display_update_book_form( id ):
    if "user_id" not in session:
        return redirect( "/" )
    data = {
        "id" : id
    }
    current_recipe = Recipe.get_one( data )
    return render_template( "update_recipe.html", current_recipe = current_recipe )


@app.route( "/recipe/update/<int:id>", methods=["POST"] )
def update_book( id ):
    if Recipe.validate_recipe( request.form ) == False:
        return redirect( f"/recipe/{id}/edit" )
    data = {
        "id" : id,
        **request.form,
        "user_id" : session["user_id"]
    }
    Recipe.update_one( data )
    return redirect( f"/recipe/{id}" )

@app.route( "/logout", methods=["POST"] )
def process_logout():
    session.clear()
    return redirect( "/" )

