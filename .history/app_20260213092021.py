
import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from sklearn.cluster import KMeans, AgglomerativeClustering
from PIL import Image
import io

# Initialisation de l'application Flask
app = Flask(__name__)

# Style CSS pour rendre l'interface plus jolie (police, couleurs, boutons)
style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');
    body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; color: #1c1e21; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    h1 { color: #1877f2; font-weight: 500; }
    .container { display: flex; flex-direction: column; gap: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
    a, button { text-decoration: none; color: white; background-color: #424270; padding: 10px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: transform 0.2s; text-align: center;}
    a:hover, button:hover { background-color: #313156; transform: scale(1.05); }
</style>
"""

# Route pour la page d'accueil avec les liens vers les différentes fonctionnalités
@app.route('/')
def home():
    return style + """
    <h1>Ma Plateforme IA</h1>
    <div class="container">
        <a href="/photo">Segmentation K-Means</a>
        <a href="/hierarchical">Segmentation Hiérarchique</a>
        <a href="/map">Aller vers la carte</a>
        <a href="/about">À propos</a>
    </div>
    """

@app.route('/about')
def about():
    return style + """<h1>À propos</h1><p>Comparaison entre K-Means et Clustering Hiérarchique.</p><a href="/">Retour</a>"""

# Affiche la carte interactive Leaflet
@app.route('/map')
def map():
    return render_template("map.html")

# --- Gestion de l'affichage des galeries ---

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return handle_gallery("photo.html")

@app.route('/hierarchical', methods=['GET', 'POST'])
def hierarchical():
    return handle_gallery("hierarchical.html")

# Fonction générique pour lister les images d'un dossier sélectionné
def handle_gallery(template_name):
    images = []
    dossier_choisi = request.form.get('chemin_dossier', '')
    photo_selectionnee = request.form.get('menu_photos', '')
    
    # Si le dossier existe, on récupère tous les fichiers .png, .jpg, .jpeg
    if dossier_choisi and os.path.exists(dossier_choisi):
        images = [f for f in os.listdir(dossier_choisi) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    return render_template(template_name, images=images, dossier=dossier_choisi, photo_finale=photo_selectionnee)

# --- Algorithmes de Clustering ---

@app.route('/process_kmeans', methods=['POST'])
def process_kmeans():
    return run_clustering("kmeans")

@app.route('/process_hc', methods=['POST'])
def process_hc():
    return run_clustering("hc")

# Le cœur de l'application : lance l'IA choisie sur l'image
def run_clustering(method):
    dossier = request.form.get('dossier')
    photo = request.form.get('photo')
    k = int(request.form.get('k', 5)) # Nombre de couleurs souhaitées
    
    # Chargement de l'image
    path_input = os.path.join(dossier, photo)
    img = Image.open(path_input).convert('RGB')
    
    # Réduction de la taille de l'image pour accélérer les calculs
    # Le Clustering Hiérarchique (hc) est très lent, donc on réduit beaucoup (100px)
    limit = 100 if method == "hc" else 400
    img_small = img.copy()
    img_small.thumbnail((limit, limit))
    
    # Conversion de l'image en une liste de pixels (Tableau NumPy)
    img_np = np.array(img_small)
    pixels = img_np.reshape(-1, 3) # On transforme la grille en une longue liste de couleurs RGB

    if method == "kmeans":
        # Méthode K-Means : cherche les 'k' couleurs centrales les plus représentatives
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = model.fit_predict(pixels) # Assigne chaque pixel à un groupe
        colors = model.cluster_centers_.astype('uint8') # Récupère les couleurs moyennes
    else:
        # Méthode Hiérarchique : fusionne les pixels les plus proches étape par étape
        model = AgglomerativeClustering(n_clusters=k, linkage='ward')
        labels = model.fit_predict(pixels)
        # Pour le CHA, on doit calculer nous-mêmes la couleur moyenne de chaque groupe créé
        colors = np.array([pixels[labels == i].mean(axis=0) for i in range(k)]).astype('uint8')

    # Création de la nouvelle image : on remplace chaque pixel par la couleur de son groupe
    new_pixels = colors[labels]
    new_img_np = new_pixels.reshape(img_np.shape) # On remet les pixels sous forme de grille image
    
    # Sauvegarde du résultat dans le dossier d'origine
    result_name = f"{method}_{k}_{photo}"
    Image.fromarray(new_img_np).save(os.path.join(dossier, result_name))
    
    # On renvoie l'utilisateur sur la page avec l'image traitée affichée
    images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    template = "photo.html" if method == "kmeans" else "hierarchical.html"
    return render_template(template, images=images, dossier=dossier, photo_finale=result_name)

# Route spéciale pour pouvoir lire des images situées n'importe où sur l'ordinateur
@app.route('/image_externe/<path:filename>')
def image_externe(filename):
    directory = request.args.get('dir')
    return send_from_directory(directory, filename)

# Lancement du serveur sur le port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)
