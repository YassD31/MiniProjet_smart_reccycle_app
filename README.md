# Smart Recycling App

Smart Recycling App is a Flask-based machine learning web application that classifies waste images and provides recycling guidance. The project combines image classification, environmental information, visual analytics, and map-based pollution context to help users understand how different waste categories should be handled.

The app is designed as a mini AI/ML project suitable for academic demos, internships, portfolio presentations, and future smart recycling assistance features.

## Features

- Waste image classification from uploaded images
- Smart recycling assistance with environmental impact information
- AI/ML prediction system powered by TensorFlow/Keras
- Dataset integration with 8 waste categories
- Transfer learning training workflow using MobileNetV2
- Web user interface built with Flask and HTML templates
- Top-3 prediction confidence display
- Matplotlib prediction chart generation
- GeoPandas-based pollution map visualization

## Tech Stack

### Application

- **Python** — main programming language
- **Flask** — web application framework
- **HTML/CSS** — user interface templates
- **Jinja2** — Flask template rendering

### Machine Learning and Image Processing

- **TensorFlow / Keras** — model training and inference
- **MobileNetV2** — transfer learning backbone used in `train_model.py`
- **Keras ImageDataGenerator** — image loading, preprocessing, augmentation, and train/validation split
- **NumPy** — prediction array processing
- **Pillow** — image loading backend used by Keras utilities

### Visualization and Mapping

- **Matplotlib** — prediction charts and generated map images
- **GeoPandas** — shapefile loading and geospatial plotting
- **Natural Earth shapefile data** — world map boundaries in `maps/`
- **Folium** — imported in the app; currently not used in the active PNG map workflow

### DevOps / Integrations

- **Git** — repository version control
- **Docker** — not currently configured
- **Ollama / local LLMs** — not currently configured

## Machine Learning Pipeline

### Dataset

The dataset is stored in `dataset/` using a folder-per-class image classification structure:

```text
dataset/
├── cardboard/
├── ewaste/
├── glass/
├── metal/
├── organic/
├── paper/
├── plastic/
└── trash/
```

Detected dataset distribution:

| Class | Images |
| --- | ---: |
| cardboard | 400 |
| ewaste | 3,985 |
| glass | 400 |
| metal | 400 |
| organic | 400 |
| paper | 400 |
| plastic | 400 |
| trash | 397 |

The dataset contains JPG/JPEG image files. `dataset_distribution.png` visualizes the class distribution.

### Preprocessing

Training and prediction both resize images to **224x224** pixels. Pixel values are normalized to the range `[0, 1]` by dividing by `255.0`.

During training, `ImageDataGenerator` applies:

- Rescaling
- 80/20 training-validation split
- Rotation augmentation
- Zoom augmentation
- Horizontal flip augmentation

### Training

`train_model.py` trains a transfer learning classifier:

1. Loads images from `dataset/`
2. Splits data into training and validation subsets
3. Loads **MobileNetV2** pretrained on ImageNet without the top classification layer
4. Freezes most base layers while fine-tuning the last 20 layers
5. Adds a custom classification head:
   - `GlobalAveragePooling2D`
   - `Dense(128, activation="relu")`
   - `Dropout(0.5)`
   - `Dense(num_classes, activation="softmax")`
6. Trains for 30 epochs
7. Saves the model to `model/recycling_model.h5`

`cnn model.py` contains an alternative simple CNN architecture for experimentation, but the active training workflow uses MobileNetV2.

### Prediction Workflow

The Flask app loads `model/recycling_model.h5` at startup. When a user uploads an image:

1. The image is saved to `uploads/`
2. It is resized to `224x224`
3. It is converted to a NumPy array
4. A batch dimension is added
5. Pixel values are normalized
6. The trained model predicts probabilities for all 8 classes
7. The highest-probability class is selected
8. The app displays:
   - Predicted waste type
   - Confidence score
   - Top-3 predictions
   - Recycling and environmental information
   - Prediction chart
   - Pollution map visualization

## Application Workflow

1. User opens the homepage at `/`
2. User uploads a waste image through the web form
3. Flask receives the POST request at `/predict`
4. TensorFlow/Keras performs image classification
5. The app enriches the prediction with recycling guidance
6. Matplotlib generates a top-prediction chart
7. GeoPandas generates a pollution map from the shapefile data
8. The result page displays the prediction and visual outputs

## Installation Guide

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd SmartRecycelingApp
```

### 2. Create a Python virtual environment

On Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

On macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If `requirements.txt` is available:

```bash
pip install -r requirements.txt
```

Or install the main dependencies manually:

```bash
pip install flask tensorflow numpy matplotlib geopandas folium pillow h5py
```

> Note: GeoPandas may require geospatial dependencies depending on your operating system. If installation fails, check the official GeoPandas installation guide for platform-specific instructions.

### 4. Verify required local assets

Make sure these paths exist:

```text
dataset/
model/recycling_model.h5
maps/ne_110m_admin_0_countries.shp
templates/
static/
uploads/
```

### Docker setup

Docker is not currently configured in this repository. If Docker support is added later, include a `Dockerfile` and optional `docker-compose.yml`.

### Ollama setup

Ollama or local LLM integration is not currently implemented. Future versions could use Ollama to generate richer recycling recommendations or conversational assistance.

## Usage

### Run the web application

```bash
python app.py
```

Open the app in your browser:

```text
http://127.0.0.1:5000
```

Upload a waste image and view the classification result.

### Retrain the model

```bash
python train_model.py
```

The trained model will be saved to:

```text
model/recycling_model.h5
```

### Generate dataset distribution chart

```bash
python import_matplotlib.py
```

This creates or updates:

```text
dataset_distribution.png
```

## Project Structure

```text
SmartRecycelingApp/
├── app.py                         # Flask app and prediction route
├── train_model.py                 # MobileNetV2 training pipeline
├── cnn model.py                   # Experimental simple CNN architecture
├── import_matplotlib.py           # Dataset distribution chart script
├── import matplotlib.py           # Duplicate chart script with a spaced filename
├── dataset_distribution.png       # Dataset class distribution visualization
├── dataset/                       # Waste image dataset organized by class
├── maps/                          # Natural Earth shapefile assets for maps
├── model/
│   └── recycling_model.h5         # Saved TensorFlow/Keras model
├── static/
│   ├── charts/                    # Generated prediction charts
│   └── maps/                      # Generated pollution map outputs
├── templates/
│   ├── index.html                 # Upload page
│   └── result.html                # Prediction result page
├── uploads/                       # Runtime image uploads
├── .gitignore                     # Git ignore rules
└── SmartRecycelingApp.code-workspace
```

## Screenshots

Screenshots can be added here after running the application:

- Homepage upload screen
- Prediction result screen
- Top-3 prediction chart
- Pollution map visualization

```text
docs/screenshots/homepage.png
docs/screenshots/result.png
```

## Future Improvements

- Pin dependency versions after validating a stable local environment
- Improve upload security with filename sanitization and file type validation
- Add prediction API endpoint returning JSON
- Store generated charts/maps with unique filenames per request
- Add model evaluation metrics and confusion matrix
- Balance the dataset, especially the larger `ewaste` class
- Add Docker support for reproducible deployment
- Add Ollama-powered recycling chatbot or recommendation assistant
- Add tests for preprocessing, prediction, and Flask routes
- Improve UI with responsive CSS or a frontend framework

## Authors

- Smart Recycling App project contributors

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.