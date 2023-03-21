from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredient = db.Column(db.String(300), nullable=False)
    cooking = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Recipe %r>' % self.id

@app.route('/')
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/advices')
def advices():
    return render_template("advices.html")

@app.route('/recipes')
def recipes():
    recipes = Recipe.query.order_by(Recipe.date.desc()).all()
    return render_template("recipes.html", recipes=recipes)

@app.route('/recipes/<int:id>')
def recipes_detail(id):
    recipes = Recipe.query.get(id)
    return render_template("recipes_detail.html", recipes=recipes)

@app.route('/create_recipe', methods =['POST', 'GET'])
def create_recipe():
    if request.method == "POST":
        title = request.form['title']
        ingredient = request.form['ingredient']
        cooking = request.form['cooking']
        author = request.form['author']

        recipe = Recipe(title=title, ingredient=ingredient, cooking=cooking, author=author)
        try:
            db.session.add(recipe)
            db.session.commit()
            return redirect('/recipes')
        except:
            return "При добавлении рецепта возникла ошибка"
    else:
        return render_template("create_recipe.html")

if __name__=='__main__':
    app.run(debug=True)