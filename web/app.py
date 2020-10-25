"""
Service API
------------

* Registration of a user 0 tokens.
* Each user gets 10 tokens.
* Store a sentence on our database for 1 token.
* Retrieve his stored sentence on out database for 1 token.

@author Hamza Arain
@version 0.0.1v
@date 25 October 2020

"""

# import flask
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

import bcrypt


# ###########################################################
# #######################  Tool Classe ######################
# ###########################################################    

class Tool():
    def JSONOutputMessage(statusCode, output=""):
        """Return status code 200 & output"""
        retMap = {
            'Message': output,
            'Status Code': statusCode
        }
        return jsonify(retMap)

    def verifyPw(username, password):
        hashed_pw = users.find({
            "Username":username
        })[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        else:
            return False

    def countTokens(username):
        tokens = users.find({
            "Username":username
        })[0]["Tokens"]
        return tokens

# ###########################################################
# #######################  API Classes ######################
# ###########################################################    

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"

        # password > hash + salt 
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens":6
        })

        return Tool.JSONOutputMessage(statusCode=200, output="You successfully signed up for the API")



class Store(Resource):
    def post(self):
        #Step 1 get the posted data
        postedData = request.get_json()

        #Step 2 is to read the data
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        #Step 3 verify the username pw match
        correct_pw = Tool.verifyPw(username, password)

        if not correct_pw:
            return Tool.JSONOutputMessage(statusCode=302)
        #Step 4 Verify user has enough tokens
        num_tokens = Tool.countTokens(username)
        if num_tokens <= 0:
            return Tool.JSONOutputMessage(statusCode=301)
        #Step 5 store the sentence, take one token away  and return 200OK
        users.update({
            "Username":username
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
        })

        return Tool.JSONOutputMessage(statusCode=200, output="Sentence saved successfully")

        


class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        #Step 3 verify the username pw match
        correct_pw = Tool.verifyPw(username, password)
        if not correct_pw:
            return Tool.JSONOutputMessage(statusCode=302)

        num_tokens = Tool.countTokens(username)
        if num_tokens <= 0:
            return Tool.JSONOutputMessage(statusCode=301)

        #MAKE THE USER PAY!
        users.update({
            "Username":username
        }, {
            "$set":{
                "Tokens":num_tokens-1
                }
        })

        sentence = users.find({
            "Username": username
        })[0]["Sentence"]

        return Tool.JSONOutputMessage(statusCode=200, output=str(sentence))



# ###########################################################
# ##################### Run Application #####################
# ###########################################################


# Database connection
# # "db" is same as written in web Dockerfile
# # "27017" is default port for MongoDB 
client = MongoClient("mongodb://db:27017")  
db = client.SentencesDatabase      # Create database
users = db["Users"]                # Create collection

# App & API creation
app = Flask(__name__)
api = Api(app)

# API paths
api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')


if __name__=="__main__":
    app.run(host='0.0.0.0')