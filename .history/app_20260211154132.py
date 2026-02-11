from flask import Flask, render_template

app = Flask(__name__)
style = '<link rel="stylesheet" href="/static/style.css">'

@app.route('/')
def home():
    return """
    <h1>Bienvenue sur ma page d'accueil !</h1>
    <a href="/about">Aller vers la page À propos</a><br>
    <a href="/project">Aller vers la page Projet</a> <br>
    <a href="/map">Aller vers la carte</a>
    """

@app.route('/about')
def about():
    return """
    <h1>À propos</h1>
    <p>Je suis en train d'apprendre à développer des applications web avec Flask !</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/project')
def project():
    return """
    <h1>Page Projet</h1>
    <p>Bienvenue sur ma page projet !</p>
    <a href="/">Retour à l'accueil</a>
    """


@app.route('/map')
def map():
    return render_template("map.html")





if __name__ == '__main__':
    app.run(debug=True, port=5001)




