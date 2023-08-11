import config
from users import get_all

app = config.connex_app
app.add_api(config.basedir / "swagger.yml")

@app.route("/")
def home():
    return get_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)