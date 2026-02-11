# from flask import Flask, render_template

# app = Flask(__name__)
# style = '<link rel="stylesheet" href="/static/style.css">'

# @app.route('/')
# def home():
#     return """
#     <h1>Bienvenue sur ma page d'accueil !</h1>
#     <a href="/about">Aller vers la page À propos</a><br>
#     <a href="/project">Aller vers la page Projet</a> <br>
#     <a href="/map">Aller vers la carte</a>
#     """

# @app.route('/about')
# def about():
#     return """
#     <h1>À propos</h1>
#     <p>Je suis en train d'apprendre à développer des applications web avec Flask !</p>
#     <a href="/">Retour à l'accueil</a>
#     """

# @app.route('/project')
# def project():
#     return """
#     <h1>Page Projet</h1>
#     <p>Bienvenue sur ma page projet !</p>
#     <a href="/">Retour à l'accueil</a>
#     """


# @app.route('/map')
# def map():
#     return render_template("map.html")



# if __name__ == '__main__':
#     app.run(debug=True, port=5001)*


from flask import Flask, render_template

app = Flask(__name__)

# Lien vers ton CSS
style = '<link rel="stylesheet" href="/static/style.css">'

# Petite fonction pour éviter de répéter le HTML partout
def render_page(title, content):
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        {style}
    </head>
    <body>
        <div class="card">
            {content}
        </div>
    </body>
    </html>
    """

# Page Accueil
@app.route('/')
def home():
    content = """
        <h1>Bienvenue 👋</h1>
        <p>Mon premier site web avec Flask</p>

        <a href="/about">À propos</a><br>
        <a href="/project">Mes projets</a><br>
        <a href="/map">Voir la carte</a>
    """
    return render_page("Accueil", content)

# Page À propos
@app.route('/about')
def about():
    content = """
        <h1>À propos</h1>
        <p>Je suis en train d'apprendre à développer des applications web avec Flask 🚀</p>
        <a href="/">Retour accueil</a>
    """
    return render_page("À propos", content)

# Page Projet
@app.route('/project')
def project():
    content = """
        <h1>Mes projets</h1>
        <p>Bienvenue sur ma page projet !</p>
        <a href="/">Retour accueil</a>
    """
    return render_page("Projet", content)

# Page Carte (template HTML existant)
@app.route('/map')
def map():
    return f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Carte</title>
        {style}
    </head>
    <body>
        <div class="card">
            <h1>Carte 🗺️</h1>
            <p>Ma carte interactive est ci-dessous :</p>
            <iframe src="/static/map.html" width="100%" height="400px"></iframe>
            <br><br>
            <a href="/">Retour accueil</a>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5001)

