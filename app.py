from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import matplotlib.pyplot as plt
import folium
import geopandas as gpd


app = Flask(__name__)

# Charger modèle
model = tf.keras.models.load_model("model/recycling_model.h5")

# Classes
classes = [
    "cardboard",
    "ewaste",
    "glass",
    "metal",
    "organic",
    "paper",
    "plastic",
    "trash"
]

# Informations écologiques
waste_info = {

    "plastic": {
        "pollution": "400 millions de tonnes de plastique produites chaque année.",
        "recycle": "Bouteilles, vêtements, mobilier urbain.",
        "impact": "Très polluant pour les océans et les animaux.",
        "country": "Océan Pacifique"
    },

    "organic": {
        "pollution": "Déchets biodégradables issus de la nourriture.",
        "recycle": "Compost et fertilisants naturels.",
        "impact": "Faible impact si correctement recyclé.",
        "country": "Afrique"
    },

    "glass": {
        "pollution": "Le verre prend des milliers d'années à disparaître.",
        "recycle": "Nouvelles bouteilles et décoration.",
        "impact": "100% recyclable.",
        "country": "Europe"
    },

    "metal": {
        "pollution": "Extraction minière très polluante.",
        "recycle": "Canettes, outils, pièces industrielles.",
        "impact": "Très recyclable avec forte économie d'énergie.",
        "country": "Chine"
    },

    "paper": {
        "pollution": "Déforestation et forte consommation d'eau.",
        "recycle": "Papier recyclé et cartons.",
        "impact": "Recyclable plusieurs fois.",
        "country": "Brésil"
    },

    "ewaste": {
        "pollution": "Plus de 50 millions de tonnes de déchets électroniques par an.",
        "recycle": "Extraction des métaux rares et composants électroniques.",
        "impact": "Très toxique pour l'environnement.",
        "country": "Inde"
    },

    "trash": {
        "pollution": "Déchets non recyclables accumulés dans les décharges.",
        "recycle": "Traitement spécialisé ou incinération.",
        "impact": "Fort impact environnemental.",
        "country": "États-Unis"
    },

    "cardboard": {
        "pollution": "Production liée à la déforestation.",
        "recycle": "Cartons recyclés et emballages.",
        "impact": "Très recyclable.",
        "country": "Canada"
    }
}

# Coordonnées carte
map_locations = {
    "Océan Pacifique": [10, -140],
    "Afrique": [1, 20],
    "Europe": [48, 10],
    "Chine": [35, 103],
    "Brésil": [-14, -51],
    "Inde": [20, 78],
    "États-Unis": [37, -95],
    "Canada": [56, -106]
}

# Niveaux de pollution
pollution_levels = {

    "plastic": {
        "China": 95,
        "India": 90,
        "United States of America": 85,
        "Brazil": 70,
        "Germany": 30,
        "France": 35,
        "Canada": 25,
        "Australia": 20
    },

    "ewaste": {
        "China": 90,
        "India": 95,
        "United States of America": 80,
        "Germany": 50,
        "France": 45,
        "Canada": 35
    },

    "metal": {
        "China": 85,
        "Russia": 75,
        "India": 70,
        "Canada": 40
    },

    "glass": {
        "Germany": 25,
        "France": 30,
        "Italy": 35,
        "China": 60
    },

    "paper": {
        "Brazil": 80,
        "Canada": 40,
        "Sweden": 20,
        "Germany": 25
    },

    "organic": {
        "India": 50,
        "Brazil": 45,
        "France": 20,
        "Canada": 15
    },

    "cardboard": {
        "China": 65,
        "United States of America": 55,
        "Germany": 25
    },

    "trash": {
        "India": 95,
        "Indonesia": 90,
        "Brazil": 80,
        "United States of America": 70
    }
}

# Accueil
@app.route("/")
def home():
    return render_template("index.html")

# Prediction
@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    # Préparer image
    img = image.load_img(filepath, target_size=(224,224))

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(img_array, axis=0)

    img_array /= 255.0

    # Prediction
    prediction = model.predict(img_array)[0]

    predicted_index = np.argmax(prediction)

    predicted_class = classes[predicted_index]

    confidence = round(prediction[predicted_index] * 100, 2)

    # Top résultats
    top_indices = prediction.argsort()[-3:][::-1]

    top_predictions = []

    for i in top_indices:
        top_predictions.append({
            "class": classes[i],
            "score": round(prediction[i] * 100, 2)
        })

    # Infos
    info = waste_info[predicted_class]

    # Graphique
    labels = [p["class"] for p in top_predictions]
    values = [p["score"] for p in top_predictions]

    plt.figure(figsize=(6,4))
    plt.bar(labels, values)
    plt.xlabel("Catégories")
    plt.ylabel("Pourcentage")
    plt.title("Résultats IA")

    chart_path = "static/charts/prediction_chart.png"

    plt.savefig(chart_path)

    plt.close()

    # Charger carte du monde
    world = gpd.read_file("maps/ne_110m_admin_0_countries.shp")
    print(world.columns)

    # Valeur par défaut
    world['pollution'] = 10

    # Matériau détecté
    material_pollution = pollution_levels.get(predicted_class, {})

    # Affecter niveaux pollution
    for country, value in material_pollution.items():
        world.loc[world['NAME'] == country, 'pollution'] = value

    # Générer figure
    fig, ax = plt.subplots(1, 1, figsize=(15,8))

    world.plot(
        column='pollution',
        cmap='RdYlGn_r',
        linewidth=0.8,
        ax=ax,
        edgecolor='0.8',
        legend=True
    )

    ax.set_title(f'Carte mondiale de pollution : {predicted_class}', fontsize=18)

    map_path = 'static/maps/pollution_map.png'

    plt.savefig(map_path, bbox_inches='tight')

    plt.close()

    return render_template(
        "result.html",
        prediction=predicted_class,
        confidence=confidence,
        pollution=info["pollution"],
        recycle=info["recycle"],
        impact=info["impact"],
        image_path=filepath,
        chart_path=chart_path,
        map_path=map_path,
        top_predictions=top_predictions
    )

if __name__ == "__main__":
    app.run(debug=True)