from flask import Flask, render_template, request
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import requests
from datetime import datetime
import os
from auth import auth_blueprint
from models import models_blueprint, db, UserData
app = Flask(__name__)
app.secret_key = "super secret key"
login_manager = LoginManager(app)
login_manager.init_app(app)
csrf = CSRFProtect()
csrf.init_app(app)
# Register the auth Blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(models_blueprint, url_prefix='/models')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

# Initialize the database
db.init_app(app)

newsapi = os.getenv("news_api_key")


@login_manager.user_loader
def load_user(id):
    return UserData.query.get(int(id))
# Custom Jinja filter to convert datetime string to formatted string


@app.template_filter('format_datetime')
def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').strftime(format)


@app.route("/", endpoint='homepage')
def home():
    url = f"https://newsapi.org/v2/everything?q=india&apiKey={newsapi}"
    # url=f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={newsapi}"
    res = requests.get(url)
    if res.status_code == 200:
        response = res.json()["articles"]
        # for res in response:
        #     print(res['content'])
        country_code = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu',
                        'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr']

        return render_template("body.html", response={"response": response, "countries": country_code})
    return render_template("index.html")


@app.route("/list_of_suggestions", methods=['GET', 'POST'], endpoint='list_of_suggestions')
def SuggestionList():
    if request.method == 'POST':
        print("request.form--SuggestionList------", request.form)
    return {"suggestions": ["bitcoin", "india", "economics"]}


@app.route("/search", methods=['GET', 'POST'], endpoint='search_keywords')
def search_keywords():
    if request.method == 'POST':
        print("request.form-----search_keywords---", request.form)
        search_keyword = request.form.get("keyword")
        url = f"https://newsapi.org/v2/everything?q={search_keyword}&apiKey={newsapi}"
        # url=f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={newsapi}"
        res = requests.get(url)
        if res.status_code == 200:
            response = res.json()["articles"]
            # for res in response:
            #     print(res['content'])
            return render_template("body.html", response={"response": response, "countries": []})
        return render_template("index.html")


@app.route("/get-category-news/<search_for>", methods=['GET', 'POST'], endpoint='category_search')
def GetCategoryNews(search_for):
    print("request.form-----GetCategoryNews---", search_for)
    url = f"https://newsapi.org/v2/top-headlines?country=in&category={search_for}&apiKey={newsapi}"
    res = requests.get(url)
    if res.status_code == 200:
        response = res.json()["articles"]
        # for res in response:
        #     print(res['content'])
        return render_template("body.html", response={"response": response, "countries": []})


@app.route("/country-code", methods=['GET', 'POST'], endpoint='country_code')
def CountryCode():
    if request.method == 'POST':
        print("request.form-----search_keywords---", request.form)
        search_keyword = request.form.get("keyword")
        url = f"https://newsapi.org/v2/everything?q={search_keyword}&apiKey={newsapi}"
        # url=f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey={newsapi}"
        res = requests.get(url)
        if res.status_code == 200:
            response = res.json()["articles"]
            # for res in response:
            #     print(res['content'])
            return render_template("body.html", response=response)
        return render_template("index.html")
    else:
        country_code = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu',
                        'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr']
        return country_code


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
