
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# On définit le CSS directement dans une variable
style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');

    body {
        font-family: 'Poppins', sans-serif;
        background-color: #f0f2f5;
        color: #1c1e21;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        margin: 0;
    }

    h1 {
        color: #1877f2;
        font-weight: 500;
    }

    p {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    a {
        text-decoration: none;
        color: white;
        background-color: 424270;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: bold;
        margin: 10px;
        transition: transform 0.2s, background-color 0.2s;
    }

    a:hover {
        background-color: 424270;
        transform: scale(1.05);
    }
</style>
"""

@app.route('/')
def home():
    return style + """
    <h1>Bienvenue sur ma page d'accueil !</h1>
    <div style="display: flex; flex-direction: column;">
        <a href="/about">Aller vers la page À propos</a>
        <a href="/project">Aller vers la page Projet</a>
        <a href="/map">Aller vers la carte</a>
        <a href="/photo">Voir mes photos</a>
    </div>
    """

@app.route('/about')
def about():
    return style + """
    <h1>À propos</h1>
    <p>Je suis en train d'apprendre à développer des applications web avec Flask !</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/project')
def project():
    return style + """
    <h1>Page Projet</h1>
    <p>Bienvenue sur ma page projet !</p>
    <a href="/">Retour à l'accueil</a>
    """

@app.route('/map')
def map():
    return render_template("map.html")



@app.route('/photo')
def photo():
    # On se contente d'afficher la page photo.html
    return render_template("photo.html")





if __name__ == '__main__':
    app.run(debug=True, port=5001)

