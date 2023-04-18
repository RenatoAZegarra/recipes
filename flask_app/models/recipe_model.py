from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models import user_model

class Recipe:
    def __init__( self, data ):
        self.id = data["id"]
        self.name_of_recipe = data["name_of_recipe"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.under_30_min = data["under_30_min"]
        self.made_on = data["made_on"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None
    
    @classmethod
    def create_one( cls, data ):
        query  = "INSERT INTO recipes( name_of_recipe, description, instruction, under_30_min, made_on, user_id ) "
        query += "VALUES( %(name_of_recipe)s, %(description)s, %(instruction)s, %(under_30_min)s, %(made_on)s, %(user_id)s );"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return result
    
    @classmethod
    def get_all_with_users( cls ):
        query  = "SELECT * "
        query += "FROM recipes r JOIN users u "
        query += "ON r.user_id = u.id;"

        results = connectToMySQL( DATABASE ).query_db( query )
        list_of_recipes = []
        for row in results:
            current_recipe = cls( row )
            recipe_user = {
                "created_at" : row["u.created_at"],
                "updated_at" : row["u.updated_at"],
                "id" : row["u.id"],
                **row
            }
            current_recipe.user = user_model.User( recipe_user )
            list_of_recipes.append( current_recipe )
        return list_of_recipes
    @classmethod
    def get_recipe_with_user( cls, data):
        query  = "SELECT * "
        query += "FROM recipes r JOIN users u "
        query += "ON r.user_id = u.id "
        query += "WHERE r.id = %(id)s; "

        result = connectToMySQL( DATABASE ).query_db( query, data)
        row = result[0]
        current_recipe= cls(row)
        recipe_user = {
            **row,
            "created_at" : row["u.created_at"],
            "updated_at" : row["u.updated_at"],
            "id" : row["u.id"]
        }
        current_recipe.user = user_model.User(recipe_user)
        return current_recipe

    @classmethod
    def delete_one( cls, data ):
        query  = "DELETE FROM recipes "
        query += "WHERE id = %(id)s;"
        return connectToMySQL( DATABASE ).query_db( query, data )
    
    @classmethod
    def get_one( cls, data ):
        query  = "SELECT * "
        query += "FROM recipes "
        query += "WHERE id = %(id)s;"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        return cls( result[0] )
    
    @classmethod
    def update_one( cls, data ):
        query  = "UPDATE recipes "
        query += "SET name_of_recipe = %(name_of_recipe)s, description = %(description)s, instruction = %(instruction)s, under_30_min = %(under_30_min)s, made_on = %(made_on)s, user_id = %(user_id)s "
        query += "WHERE id = %(id)s;"
        return connectToMySQL( DATABASE ).query_db( query, data )

    @staticmethod
    def validate_recipe( data ):
        is_valid = True
        if len( data["name_of_recipe"] ) == 0:
            flash( "You must provide a Recipe!.", "error_recipe" )
            is_valid = False
        if len( data["description"] ) == 0:
            flash( "You must provide a Description!.", "error_description" )
            is_valid = False
        if len( data["instruction"] ) == 0:
            flash( "You must provide your Instructions!.", "error_instruction" )
            is_valid = False
        return is_valid
    
