import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
import os

# Taille images
IMG_SIZE = 224

# Batch
BATCH_SIZE = 32

# Nombre catégories
num_classes = len(os.listdir("dataset"))

print("Nombre de catégories :", num_classes)

# Data augmentation
train_datagen = ImageDataGenerator(

    rescale=1./255,

    validation_split=0.2,

    rotation_range=20,

    zoom_range=0.2,

    horizontal_flip=True
)

# Training
train_generator = train_datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="training"
)

# Validation
validation_generator = train_datagen.flow_from_directory(

    "dataset",

    target_size=(IMG_SIZE, IMG_SIZE),

    batch_size=BATCH_SIZE,

    class_mode="categorical",

    subset="validation"
)

# Modèle pré-entraîné
base_model = MobileNetV2(

    weights='imagenet',

    include_top=False,

    input_shape=(224,224,3)
)

# Geler couches pré-entraînées
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

# Nouveau modèle
model = Sequential([

    base_model,

    GlobalAveragePooling2D(),

    Dense(128, activation='relu'),

    Dropout(0.5),

    Dense(num_classes, activation='softmax')
])

# Compilation
model.compile(

    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),

    loss='categorical_crossentropy',

    metrics=['accuracy']
)

# Résumé
model.summary()

# Entraînement
history = model.fit(

    train_generator,

    validation_data=validation_generator,

    epochs=30
)

# Sauvegarde
model.save("model/recycling_model.h5")

print("Modèle MobileNetV2 sauvegardé avec succès.")