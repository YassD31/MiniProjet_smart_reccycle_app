from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.layers import Flatten, Dense, Dropout

# Création du modèle CNN

model = Sequential()

# Première couche convolutionnelle
model.add(Conv2D(
    32,
    (3,3),
    activation='relu',
    input_shape=(224,224,3)
))

model.add(MaxPooling2D(pool_size=(2,2)))

# Deuxième couche convolutionnelle
model.add(Conv2D(
    64,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D(pool_size=(2,2)))

# Troisième couche convolutionnelle
model.add(Conv2D(
    128,
    (3,3),
    activation='relu'
))

model.add(MaxPooling2D(pool_size=(2,2)))

# Flatten
model.add(Flatten())

# Couche Dense
model.add(Dense(
    128,
    activation='relu'
))

# Dropout pour réduire l'overfitting
model.add(Dropout(0.5))

# Couche finale
model.add(Dense(
    8,
    activation='softmax'
))

# Compilation du modèle
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Affichage de l'architecture
model.summary()