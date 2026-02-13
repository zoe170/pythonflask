

# import os
# import numpy as np
# from flask import Flask, render_template, request, send_from_directory
# from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
# from PIL import Image

# app = Flask(__name__)

# # Style CSS centralisé pour l'interface
# style = """
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');
#     body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; color: #1c1e21; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
#     h1 { color: #1877f2; font-weight: 500; }
#     .container { display: flex; flex-direction: column; gap: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); width: 350px; }
#     a, button { text-decoration: none; color: white; background-color: #424270; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; text-align: center; }
#     a:hover, button:hover { background-color: #313156; transform: scale(1.02); }
# </style>
# """

# @app.route('/')
# def home():
#     """Page d'accueil avec navigation vers les trois types de segmentation."""
#     return style + """
#     <h1>Ma Plateforme IA</h1>
#     <div class="container">
#         <a href="/photo">Segmentation K-Means (Rapide)</a>
#         <a href="/hierarchical">Segmentation Hiérarchique (Précis)</a>
#         <a href="/dbscan">Segmentation par Densité (DBSCAN)</a>
#         <a href="/map">Mon Parcours (Carte)</a>
#         <a href="/about">À propos</a>
#     </div>
#     """

# @app.route('/about')
# def about():
#     return style + '<h1>À propos</h1><p>Comparaison entre K-Means, Clustering Hiérarchique et DBSCAN.</p><a href="/">Retour</a>'

# @app.route('/map')
# def map():
#     return render_template("map.html")

# # --- Gestion des Galeries ---

# @app.route('/photo', methods=['GET', 'POST'])
# def photo():
#     return handle_gallery("photo.html")

# @app.route('/hierarchical', methods=['GET', 'POST'])
# def hierarchical():
#     return handle_gallery("hierarchical.html")

# @app.route('/dbscan', methods=['GET', 'POST'])
# def dbscan():
#     return handle_gallery("dbscan.html")

# def handle_gallery(template_name):
#     """Gère l'affichage du dossier et de la photo sélectionnée."""
#     images = []
#     dossier_choisi = request.form.get('chemin_dossier', '')
#     photo_selectionnee = request.form.get('menu_photos', '')
#     if dossier_choisi and os.path.exists(dossier_choisi):
#         images = [f for f in os.listdir(dossier_choisi) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#     return render_template(template_name, images=images, dossier=dossier_choisi, photo_finale=photo_selectionnee)

# # --- Algorithmes de Clustering ---

# @app.route('/process_kmeans', methods=['POST'])
# def process_kmeans():
#     return run_clustering("kmeans")

# @app.route('/process_hc', methods=['POST'])
# def process_hc():
#     return run_clustering("hc")

# @app.route('/process_dbscan', methods=['POST'])
# def process_dbscan():
#     return run_clustering("dbscan")

# def run_clustering(method):
#     """Exécute l'algorithme choisi sur l'image d'origine."""
#     dossier = request.form.get('dossier')
#     photo = request.form.get('photo')
#     stats = None
    
#     # 1. Chargement de l'image originale
#     path_input = os.path.join(dossier, photo)
#     img = Image.open(path_input).convert('RGB')
    
#     # 2. Paramètres et Redimensionnement
#     if method == "kmeans":
#         k = int(request.form.get('k', 5))
#         limit = 400
#     elif method == "hc":
#         k = int(request.form.get('k', 5))
#         limit = 100
#     else: # dbscan
#         eps = float(request.form.get('eps', 5))
#         min_samples = int(request.form.get('min_samples', 10))
#         limit = 150 # Réduction pour performance

#     img_small = img.copy()
#     img_small.thumbnail((limit, limit))
#     img_np = np.array(img_small)
#     pixels = img_np.reshape(-1, 3)

#     # 3. Application de l'IA
#     if method == "kmeans":
#         model = KMeans(n_clusters=k, n_init=10, random_state=42)
#         labels = model.fit_predict(pixels)
#         colors = model.cluster_centers_.astype('uint8')
#         new_pixels = colors[labels]
#         suffix = f"kmeans_{k}"

#     elif method == "hc":
#         model = AgglomerativeClustering(n_clusters=k, linkage='ward')
#         labels = model.fit_predict(pixels)
#         colors = np.array([pixels[labels == i].mean(axis=0) for i in range(k)]).astype('uint8')
#         new_pixels = colors[labels]
#         suffix = f"hc_{k}"

#     elif method == "dbscan":
#         model = DBSCAN(eps=eps, min_samples=min_samples)
#         labels = model.fit_predict(pixels)
        
#         unique_labels = set(labels)
#         n_clusters = len([l for l in unique_labels if l != -1])
#         n_noise = list(labels).count(-1)
#         pct_noise = round((n_noise / len(labels)) * 100, 1)
#         stats = {"clusters": n_clusters, "noise": pct_noise}

#         new_pixels = np.zeros_like(pixels)
#         for label in unique_labels:
#             if label == -1:
#                 new_pixels[labels == label] = [0, 0, 0] # Bruit en noir
#             else:
#                 mean_col = pixels[labels == label].mean(axis=0)
#                 new_pixels[labels == label] = mean_col.astype('uint8')
#         suffix = f"dbscan_{eps}"

#     # 4. Reconstruction
#     new_img_np = new_pixels.reshape(img_np.shape)
#     result_img = Image.fromarray(new_img_np)
#     result_img = result_img.resize(img.size, Image.NEAREST)
    
#     result_name = f"{suffix}_{photo}"
#     result_img.save(os.path.join(dossier, result_name))
    
#     # 5. Retour
#     images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#     templates = {"kmeans": "photo.html", "hc": "hierarchical.html", "dbscan": "dbscan.html"}
#     return render_template(templates[method], images=images, dossier=dossier, photo_finale=result_name, stats=stats)

# @app.route('/image_externe/<path:filename>')
# def image_externe(filename):
#     directory = request.args.get('dir')
#     return send_from_directory(directory, filename)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from PIL import Image

app = Flask(__name__)

# Style CSS centralisé pour l'interface
style = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');
    body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; color: #1c1e21; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
    h1 { color: #1877f2; font-weight: 500; }
    .container { display: flex; flex-direction: column; gap: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); width: 350px; }
    a, button { text-decoration: none; color: white; background-color: #424270; padding: 12px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; text-align: center; }
    a:hover, button:hover { background-color: #313156; transform: scale(1.02); }
</style>
"""

@app.route('/')
def home():
    """Page d'accueil avec navigation vers les trois types de segmentation."""
    return style + """
    <h1>Ma Plateforme IA</h1>
    <div class="container">
        <a href="/photo">Segmentation K-Means (Rapide)</a>
        <a href="/hierarchical">Segmentation Hiérarchique (Précis)</a>
        <a href="/dbscan">Segmentation par Densité (DBSCAN)</a>
        <a href="/map">Mon Parcours (Carte)</a>
        <a href="/about">À propos</a>
    </div>
    """

@app.route('/about')
def about():
    return style + '<h1>À propos</h1><p>Comparaison entre K-Means, Clustering Hiérarchique et DBSCAN.</p><a href="/">Retour</a>'

@app.route('/map')
def map():
    return render_template("map.html")

# --- Gestion des Galeries ---

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return handle_gallery("photo.html")

@app.route('/hierarchical', methods=['GET', 'POST'])
def hierarchical():
    return handle_gallery("hierarchical.html")

@app.route('/dbscan', methods=['GET', 'POST'])
def dbscan():
    return handle_gallery("dbscan.html")

def handle_gallery(template_name):
    """Gère l'affichage du dossier et de la photo sélectionnée."""
    images = []
    dossier_choisi = request.form.get('chemin_dossier', '')
    photo_selectionnee = request.form.get('menu_photos', '')
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

@app.route('/process_dbscan', methods=['POST'])
def process_dbscan():
    return run_clustering("dbscan")

def run_clustering(method):
    """Exécute l'algorithme choisi sur l'image d'origine."""
    dossier = request.form.get('dossier')
    photo = request.form.get('photo')
    stats = None
    
    # 1. Chargement de l'image originale
    path_input = os.path.join(dossier, photo)
    img = Image.open(path_input).convert('RGB')
    
    # 2. Paramètres et Redimensionnement
    if method == "kmeans":
        k = int(request.form.get('k', 5))
        limit = 400
    elif method == "hc":
        k = int(request.form.get('k', 5))
        limit = 100
    else: # dbscan
        eps = float(request.form.get('eps', 5))
        min_samples = int(request.form.get('min_samples', 10))
        limit = 150 # Limite basse car DBSCAN est gourmand

    img_small = img.copy()
    img_small.thumbnail((limit, limit))
    img_np = np.array(img_small)
    pixels = img_np.reshape(-1, 3)

    # 3. Application de l'IA
    if method == "kmeans":
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = model.fit_predict(pixels)
        colors = model.cluster_centers_.astype('uint8')
        new_pixels = colors[labels]
        suffix = f"kmeans_{k}"

    elif method == "hc":
        model = AgglomerativeClustering(n_clusters=k, linkage='ward')
        labels = model.fit_predict(pixels)
        colors = np.array([pixels[labels == i].mean(axis=0) for i in range(k)]).astype('uint8')
        new_pixels = colors[labels]
        suffix = f"hc_{k}"

    elif method == "dbscan":
        model = DBSCAN(eps=eps, min_samples=min_samples)
        labels = model.fit_predict(pixels)
        
        unique_labels = set(labels)
        n_clusters = len([l for l in unique_labels if l != -1])
        n_noise = list(labels).count(-1)
        pct_noise = round((n_noise / len(labels)) * 100, 1)
        
        # Préparation des statistiques pour l'affichage
        stats = {
            "clusters": n_clusters, 
            "noise": pct_noise,
            "used_eps": eps,
            "used_min": min_samples
        }

        new_pixels = np.zeros_like(pixels)
        for label in unique_labels:
            if label == -1:
                new_pixels[labels == label] = [0, 0, 0] # Bruit en noir
            else:
                mean_col = pixels[labels == label].mean(axis=0)
                new_pixels[labels == label] = mean_col.astype('uint8')
        suffix = f"dbscan_{eps}"

    # 4. Reconstruction
    new_img_np = new_pixels.reshape(img_np.shape)
    result_img = Image.fromarray(new_img_np)
    result_img = result_img.resize(img.size, Image.NEAREST)
    
    result_name = f"{suffix}_{photo}"
    result_img.save(os.path.join(dossier, result_name))
    
    # 5. Retour vers le template correspondant
    templates = {"kmeans": "photo.html", "hc": "hierarchical.html", "dbscan": "dbscan.html"}
    images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template(templates[method], images=images, dossier=dossier, photo_finale=result_name, stats=stats)

@app.route('/image_externe/<path:filename>')
def image_externe(filename):
    directory = request.args.get('dir')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)