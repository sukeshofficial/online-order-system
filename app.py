from flask import Flask
from models import DBModels
from routes import routes

app = Flask(__name__)
app.secret_key = "super-secret-key"

app.register_blueprint(routes)

DBModels.create_tables()

if __name__ == "__main__":
    app.run(debug=True)
