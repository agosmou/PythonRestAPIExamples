import config
from users import get_all

app = config.connex_app
app.add_api(config.basedir / "openapi.yml", strict_validation=True)

@app.route("/")
def home():
    return get_all()

@app.route("/notinapiyaml")
def implementation_first_pattern():
    '''
    This API endpoint is not registered in our swagger.yaml file, 
    but it works fine! Connexion does not strictly require every 
    endpoint to be registered in the yaml file. If you choose
    not to use the yaml registration, however, then you loose 
    access to the connexion OpenAPI features (like authentication)
    '''
    return get_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)