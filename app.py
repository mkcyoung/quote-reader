# Flask component of Project
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session
from image2text import im2str
import cv2
import sys
import pytesseract

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure to use SQLite database
datab = sqlite3.connect('book_store.db',check_same_thread=False)
db = datab.cursor()

# home page containing upload of picture and input of book data (title)
@app.route('/')
def index():
    """Handle requests for / via GET (and POST)"""
    return render_template("index.html")

# Page containg lookup of stored book_store
@app.route('/lookup',methods =["GET","POST"])
def lookup():
    """Handle requests for /quotes via POST & GET"""
    # Getting titles from books
    db.execute("SELECT DISTINCT title FROM books")
    titles = db.fetchall()

    if request.method == "POST":
        # Port data to results template
        title = request.form.get("title")
        db.execute("SELECT * FROM books WHERE title = (?)",(title,))
        history = db.fetchall()

        return render_template("results.html",history=history, title=title)

    # Route via GET
    else:
        return render_template("lookup.html",titles=titles)

# Page containing all of quotes saved from that book
@app.route('/quotes',methods=["POST"])
def quotes():
    """Handle requests for /quotes via POST"""
    # Read files
    im = request.form.get("image")
    title = request.form.get("title")
    page = request.form.get("page")
    if not im or not title or not page:
        raise RuntimeError("missing strings")

    # determine if image is of acceptable format
    #if not im.lower().endswith(('.png', '.jpg', '.jpeg')):
    #    raise RuntimeError("unsupported image type")

    # Convert image to string
    new_string = im2str(im)

    # converts title to all lower case to homogenize things, could probably do
    # better here I know
    title2 = title.lower()

    # Store image and title in the database
    insert = db.execute("INSERT INTO books (title,quotes,page) VALUES (?, ?, ?)",
            (title2, new_string, page))
    datab.commit()
    # Show all quotes for that book
    db.execute("SELECT * FROM books WHERE title = ?", (title2,))
    history = db.fetchall()
    return render_template("quotes.html", history = history, title = title)


if __name__ == '__main__':
    app.run(debug=True)
