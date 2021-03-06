import os
from app import app
from flask import render_template, request, redirect

events = [
        {"event":"First Day of Classes", "date":"2019-08-21"},
        {"event":"Winter Break", "date":"2019-12-20"},
        {"event":"Finals Begin", "date":"2019-12-01"}
    ]


from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'database-name'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://admin:TRq3ABvirj4uQc3M@cluster0-acen4.mongodb.net/test?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    #connect to the Mongo DB
    collection = mongo.db.events
    #find all of the events in that database using a query , store it as events
    #{} will return everything in the database
    #list constructor will turn the results into a list (of dictionaries/objects)
    events = list(collection.find({}))
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    collection = mongo.db.events
    # insert new data
    collection.insert({"event_name": "test", "event_date": "today"})
    # return a message to the user
    return "you added an event to the database! go check it!!!!"

# need a get and a post method
@app.route('/results', methods = ["get", "post"])
def results():
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)
    #store the event_name
    event_name = user_info["event_name"]
    print("the event name is ", event_name)
    #store the event_date
    event_date = user_info["event_date"]
    print("the event date is ", event_date)
    #connect to Mongo DB
    category = user_info["category"]
    print("the category is ", category)
    collection = mongo.db.events
    email = user_info["email"]
    print("the email is ", email)
    #insert the user's input event_name and event_date to MONGO
    collection.insert({"event_name": event_name, "event_date": event_date, "category": category, "email": email})
    #(so that it will continue to exist after this program stops)
    #redirect back to the index page
    return redirect('/index')

@app.route('/delete_all')
def delete_all():
    #connect to the MongoDB
    collection = mongo.db.events
    #delete everything
    #google search terms pymongo delete many objects from database
    #the parenthesis invoke the method delete_many ()
    #the curly brackets {} query (find) all objects in the database to delete
    collection.delete_many({})
    #redirect back to the index page
    return redirect('/index')

@app.route('/EventFilter', methods = ["get", "post"])
def School():
    #connect to MONGO_DB
    collection = mongo.db.events
    user_input = dict(request.form)
    x = user_input["category"]
    #Query through all the events in '/School' category
    Dwight = list(collection.find({"category": x}))
    return render_template('EventFilter.html', events = Dwight) #pass jinja variable in
    ##Create a different html like index html
