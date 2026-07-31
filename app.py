from flask import Flask
from controllers.search_controller import search

app = Flask(__name__)

app.register_blueprint(search)

if __name__ == "__main__":
    app.run(debug=True)