from flask import Flask

from handlers.recipes import recipes

app = Flask(__name__)
app.register_blueprint(recipes)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
