# import os
# import numpy as np
# from flask import Flask, render_template, request, send_from_directory
# from sklearn.cluster import KMeans, AgglomerativeClustering
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
#     """Page d'accueil avec navigation vers les deux types de segmentation."""
#     return style + """
#     <h1>Ma Plateforme IA</h1>
#     <div class="container">
#         <a href="/photo">Segmentation K-Means (Rapide)</a>
#         <a href="/hierarchical">Segmentation Hiérarchique (Précis)</a>
#         <a href="/map">Mon Parcours (Carte)</a>
#         <a href="/about">À propos</a>
#     </div>
#     """

# @app.route('/about')
# def about():
#     return style + '<h1>À propos</h1><p>Comparaison entre K-Means et Clustering Hiérarchique.</p><a href="/">Retour</a>'

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

# def run_clustering(method):
#     """Exécute l'algorithme choisi sur l'image d'origine."""
#     dossier = request.form.get('dossier')
#     photo = request.form.get('photo')
#     k = int(request.form.get('k', 5))
    
#     # 1. Chargement de l'image
#     path_input = os.path.join(dossier, photo)
#     img = Image.open(path_input).convert('RGB')
    
#     # 2. Redimensionnement (Très important pour le CHA qui est très lent)
#     limit = 100 if method == "hc" else 400
#     img_small = img.copy()
#     img_small.thumbnail((limit, limit))
    
#     # 3. Préparation des données (pixels en liste de couleurs)
#     img_np = np.array(img_small)
#     pixels = img_np.reshape(-1, 3)

#     # 4. Application de l'IA
#     if method == "kmeans":
#         # K-Means : cherche les 'k' centres de couleurs
#         model = KMeans(n_clusters=k, n_init=10, random_state=42)
#         labels = model.fit_predict(pixels)
#         colors = model.cluster_centers_.astype('uint8')
#     else:
#         # Hiérarchique : fusionne les pixels de proche en proche
#         model = AgglomerativeClustering(n_clusters=k, linkage='ward')
#         labels = model.fit_predict(pixels)
#         # Calcul manuel de la couleur moyenne de chaque groupe
#         colors = np.array([pixels[labels == i].mean(axis=0) for i in range(k)]).astype('uint8')

#     # 5. Reconstruction et sauvegarde
#     new_pixels = colors[labels]
#     new_img_np = new_pixels.reshape(img_np.shape)
    
#     result_name = f"{method}_{k}_{photo}"
#     Image.fromarray(new_img_np).save(os.path.join(dossier, result_name))
    
#     # 6. Retour vers la page correspondante avec le résultat
#     images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
#     template = "photo.html" if method == "kmeans" else "hierarchical.html"
#     return render_template(template, images=images, dossier=dossier, photo_finale=result_name)

# @app.route('/image_externe/<path:filename>')
# def image_externe(filename):
#     directory = request.args.get('dir')
#     return send_from_directory(directory, filename)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)

