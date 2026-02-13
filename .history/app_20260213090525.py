# import os
# import numpy as np
# from flask import Flask, render_template, request, send_from_directory
# from sklearn.cluster import KMeans
# from PIL import Image
# import io


# app = Flask(__name__)

# # Style CSS pour l'interface
# style = """
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500&display=swap');
#     body { font-family: 'Poppins', sans-serif; background-color: #f0f2f5; color: #1c1e21; display: flex; flex-direction: column; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }
#     h1 { color: #1877f2; font-weight: 500; }
#     p { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
#     .container { display: flex; flex-direction: column; gap: 10px; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
#     a, button { text-decoration: none; color: white; background-color: #424270; padding: 10px 20px; border: none; border-radius: 6px; font-weight: bold; cursor: pointer; transition: transform 0.2s, background-color 0.2s; }
#     a:hover, button:hover { background-color: #313156; transform: scale(1.05); }
#     input[type="number"] { padding: 8px; border-radius: 4px; border: 1px solid #ddd; width: 60px; }
#     img { margin-top: 20px; border-radius: 8px; max-width: 100%; height: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
# </style>
# """

# @app.route('/')
# def home():
#     return style + """
#     <h1>Bienvenue sur ma page d'accueil !</h1>
#     <div class="container">
#         <a href="/about">Aller vers la page À propos</a>
#         <a href="/project">Aller vers la page Projet</a>
#         <a href="/map">Aller vers la carte</a>
#         <a href="/photo">Voir mes photos</a>
#     </div>
#     """

# @app.route('/about')
# def about():
#     return style + """<h1>À propos</h1><p>Apprentissage de Flask et K-Means !</p><a href="/">Retour</a>"""

# @app.route('/project')
# def project():
#     return style + """<h1>Projet</h1><p>Segmentation d'images par IA.</p><a href="/">Retour</a>"""

# @app.route('/map')
# def map():
#     return render_template("map.html")





# @app.route('/photo', methods=['GET', 'POST'])
# def photo():
#     images = []
#     dossier_choisi = request.form.get('chemin_dossier', '')
#     photo_selectionnee = request.form.get('menu_photos', '')

#     if dossier_choisi and os.path.exists(dossier_choisi):
#         images = [f for f in os.listdir(dossier_choisi) 
#                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     return render_template("photo.html", 
#                            images=images, 
#                            dossier=dossier_choisi, 
#                            photo_finale=photo_selectionnee)





# @app.route('/process_kmeans', methods=['POST'])
# def process_kmeans():
#     dossier = request.form.get('dossier')
#     photo = request.form.get('photo')
#     k = int(request.form.get('k', 5))

#     if not dossier or not photo:
#         return "Erreur : chemin invalide", 400

#     path_input = os.path.join(dossier, photo)
    
#     # --- Algorithme K-Means ---
#     img = Image.open(path_input).convert('RGB')
    
#     # Redimensionner pour le calcul (évite que le PC rame) 
#     img_small = img.copy()
#     img_small.thumbnail((400, 400)) 
    
#     img_np = np.array(img_small)
#     original_shape = img_np.shape
#     pixels = img_np.reshape(-1, 3)

#     # Entraînement de l'IA L'algorithme calcule la couleur moyenne de chaque groupe de pixels
#     kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
#     labels = kmeans.fit_predict(pixels)
#     colors = kmeans.cluster_centers_.astype('uint8')  

#     # Reconstruction : On remplace chaque pixel d'origine par la couleur moyenne du group
#     new_pixels = colors[labels]
#     new_img_np = new_pixels.reshape(original_shape)
    
#     # Sauvegarde du résultat
#     result_name = f"kmeans_{k}_{photo}"
#     result_path = os.path.join(dossier, result_name)
#     Image.fromarray(new_img_np).save(result_path)

#     # Récupérer la liste des images pour ne pas casser l'affichage
#     images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#     return render_template("photo.html", 
#                            images=images, 
#                            dossier=dossier, 
#                            photo_finale=result_name)

# @app.route('/image_externe/<path:filename>')
# def image_externe(filename):
#     directory = request.args.get('dir')
#     return send_from_directory(directory, filename)

# if __name__ == '__main__':
#     app.run(debug=True, port=5001)


import os
import numpy as np
from flask import Flask, render_template, request, send_from_directory
from sklearn.cluster import KMeans, AgglomerativeClustering
from PIL import Image
import io

app = Flask(__name__)

# Style CSS réutilisé pour la cohérence
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

@app.route('/')
def home():
    return style + """
    <h1>Ma Plateforme IA</h1>
    <div class="container">
        <a href="/photo">Segmentation K-Means</a>
        <a href="/hierarchical">Segmentation Hiérarchique</a>
        <a href="/map">Mon Parcours Scolaire</a>
        <a href="/about">À propos</a>
    </div>
    """

@app.route('/about')
def about():
    return style + """<h1>À propos</h1><p>Comparaison entre K-Means et Clustering Hiérarchique.</p><a href="/">Retour</a>"""

@app.route('/map')
def map():
    return render_template("map.html")

# --- Routes Communes pour les Photos ---

@app.route('/photo', methods=['GET', 'POST'])
def photo():
    return handle_gallery("photo.html")

@app.route('/hierarchical', methods=['GET', 'POST'])
def hierarchical():
    return handle_gallery("hierarchical.html")

def handle_gallery(template_name):
    images = []
    dossier_choisi = request.form.get('chemin_dossier', '')
    photo_selectionnee = request.form.get('menu_photos', '')
    if dossier_choisi and os.path.exists(dossier_choisi):
        images = [f for f in os.listdir(dossier_choisi) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return render_template(template_name, images=images, dossier=dossier_choisi, photo_finale=photo_selectionnee)

# --- Algorithmes ---

@app.route('/process_kmeans', methods=['POST'])
def process_kmeans():
    return run_clustering("kmeans")

@app.route('/process_hc', methods=['POST'])
def process_hc():
    return run_clustering("hc")

def run_clustering(method):
    dossier = request.form.get('dossier')
    photo = request.form.get('photo')
    k = int(request.form.get('k', 5))
    
    path_input = os.path.join(dossier, photo)
    img = Image.open(path_input).convert('RGB')
    
    # Redimensionnement crucial pour le CHA
    limit = 100 if method == "hc" else 400
    img_small = img.copy()
    img_small.thumbnail((limit, limit))
    
    img_np = np.array(img_small)
    pixels = img_np.reshape(-1, 3)

    if method == "kmeans":
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        labels = model.fit_predict(pixels)
        colors = model.cluster_centers_.astype('uint8')
    else:
        model = AgglomerativeClustering(n_clusters=k, linkage='ward')
        labels = model.fit_predict(pixels)
        # Calcul manuel des couleurs moyennes pour le CHA
        colors = np.array([pixels[labels == i].mean(axis=0) for i in range(k)]).astype('uint8')

    new_pixels = colors[labels]
    new_img_np = new_pixels.reshape(img_np.shape)
    
    result_name = f"{method}_{k}_{photo}"
    Image.fromarray(new_img_np).save(os.path.join(dossier, result_name))
    
    images = [f for f in os.listdir(dossier) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    template = "photo.html" if method == "kmeans" else "hierarchical.html"
    return render_template(template, images=images, dossier=dossier, photo_finale=result_name)

@app.route('/image_externe/<path:filename>')
def image_externe(filename):
    directory = request.args.get('dir')
    return send_from_directory(directory, filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)