#!/usr/bin/env python3
import flask, data
from flask import render_template, request, redirect, url_for

# app står för att vi vill ladda sidan med namnet "Portfolio".
app = flask.Flask("Portfolio")
# Flask här kopplar ihåp "route" med funktion som kommer under. 
@app.route("/")
def index():
    """Function for controlling data to and from the home page (index.html). Loads database and return the 5 projects that were last to be created"""
    db = data.load("data.json")
    # Sökning på de senaste 5 projekt som finns. 
    result = data.search(db, sort_by="start_date", sort_order="desc")
    result = result[5:]
    # render_template står för att ladda sidan.
    return render_template("index.html", projects=result)
# De godkända metoder är båda två men vi använd bara POST.
@app.route("/list", methods=["GET", "POST"])
def list():
    """Function for controlling data to and from the list page (list.html). Loads the database and returns all projects default sorted by start date."""
    db = data.load("data.json")
    checked = {}
    search_for = request.form.get("search", "")
    result = data.search(db)
    include_fields = request.form.getlist("searchfields")
    include_techniques = request.form.getlist("techniques")
    select_sortby = request.form.get("sortby", "start_date")
    select_sortorder = request.form.get("sortorder","desc")

    # if no fields are selected we convert to None as data.search does not return any projects when fed an empty list.
    if include_fields == []:
        include_fields = None
    else:
        # If user has selected short_description then we also include long_description.
        if "short_description" in include_fields:
            include_fields.append("long_description")
        # Add all fields that user checked to checked so that we send them back as checked.
        for field in include_fields:
            checked[field] = "checked"

    # Add all techniques that user checked to checked so that we send them back as checked.
    for tech in include_techniques:
        checked[tech] = "checked"

    used_tech = data.get_techniques(db)

    #Here we search for the correct projects to return based on user input.
    result = data.search(db, sort_by=select_sortby, sort_order=select_sortorder, search=search_for, search_fields=include_fields, techniques=include_techniques)

    return render_template("list.html", search=search_for, projects=result, checked=checked, techniques=used_tech, sortorder=select_sortorder)

@app.route("/techniques", methods=["GET", "POST"])
def techniques():
    """Function for controlling data to and from the techniques page (techniques.html). Loads the database and returns all projects default sorted by start date."""
    db = data.load("data.json")
    checked = {}
    include_techniques = request.form.getlist("techniques")
    
    # Add all techniques that user checked to checked so that we send them back as checked.
    for tech in include_techniques:
        checked[tech] = "checked"

    used_tech = data.get_techniques(db)
    
    #Return results based on user input.
    result = data.search(db, techniques=include_techniques) 

    return render_template("techniques.html", projects=result, checked=checked, techniques=used_tech)

@app.route("/project/<p_id>")
def project(p_id):
    """Function for controlling the data to a single project page. Sends back data corresponding with the project number from database."""
    db=data.load("data.json")
    cur_proj = data.get_project(db, p_id)
    if cur_proj == None:
        return page_not_found(404)
    
    return render_template("project.html", project=cur_proj)


@app.errorhandler(404)
def page_not_found(error):
    """In case of a 404 error we return a custom html page"""
    return render_template('404.html', title = '404'), 404

@app.errorhandler(500)
def internal_error(error):
    """If we get an internal server error we return a message"""
    return "Oops.. something went wrong! Please send this error to me: " + str(error)

