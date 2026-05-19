import matplotlib.pyplot as plt

categories = [
    "Plastic",
    "Metal",
    "Glass",
    "Organic",
    "Paper",
    "Cardboard",
    "Trash",
    "E-Waste"
]

images_count = [400, 400, 400, 400, 400, 400, 397, 3985]

plt.figure(figsize=(10,5))
plt.bar(categories, images_count)

plt.xlabel("Catégories")
plt.ylabel("Nombre d'images")
plt.title("Distribution des classes du dataset")

plt.xticks(rotation=20)

plt.savefig("dataset_distribution.png")