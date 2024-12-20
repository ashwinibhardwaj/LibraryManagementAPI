from flask import Flask
from routes import library_blueprint

app = Flask(__name__)

key = "c3be84bfc50917b4da096a1913530cc3ed13b1f39e5292c8"
# Configuration
app.config["SECRET_KEY"] = key

# Register blueprints
app.register_blueprint(library_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
