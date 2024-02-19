import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
# Cluster representation of the DB.
client = MongoClient(os.getenv("MONGO_URI"))
app.db = client.microblog  # Here we need to connect to the db created on Mongo Compass.
entries = []


def create_app():
    @app.route('/', methods=['POST', 'GET'])
    def home():
        # In this method, we need to interact with a dictionary.
        # print([e for e in app.db.entries.find({})])

        if request.method == 'POST':
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            entries.append((entry_content, formatted_date))

            # Here we have to insert a Dictionary, so we need a key value. I think this is deprecated.
            app.db.entries.insert({"content": entry_content, "date": formatted_date})

        entries_with_date = [
            (
                entry[0],
                entry[1],
                datetime.datetime.strptime(entry[1], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in entries
        ]
        return render_template("home.html", entries=entries_with_date)

    return app
