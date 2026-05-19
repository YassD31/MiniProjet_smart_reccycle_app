# Architecture

This document explains the technical architecture of the Smart Recycling App, including the web workflow, machine learning workflow, data flow, core systems, and deployment considerations.

## High-Level Architecture

Smart Recycling App is a local Flask web application connected to a TensorFlow/Keras image classification model.

```text
User Browser
    |
    | Upload image through HTML form
    v
Flask Web App (`app.py`)
    |
    | Save uploaded image to `uploads/`
    | Preprocess image to 224x224 RGB tensor
    v
TensorFlow/Keras Model (`model/recycling_model.h5`)
    |
    | Return class probabilities
    v
Prediction Enrichment
    |
    | Select top class and top-3 predictions
    | Attach environmental and recycling info
    | Generate chart and pollution map
    v
Jinja2 Result Page (`templates/result.html`)
```

### Application Workflow

1. Flask starts and loads the trained model from `model/recycling_model.h5`.
2. The user opens `/` and sees `templates/index.html`.
3. The user uploads a waste image with form field name `image`.
4. The `/predict` route receives the image through a POST request.
5. The image is saved in `uploads/`.
6. Keras preprocessing converts the file into a normalized input tensor.
7. The model predicts probabilities for the configured waste classes.
8. The app generates supporting visualizations and renders `templates/result.html`.

### ML Workflow

Training and inference are separated:

- `train_model.py` handles model training and saves the trained model.
- `app.py` loads the saved model and performs inference during web requests.

The active training approach uses MobileNetV2 transfer learning. `cnn model.py` is an experimental standalone CNN definition and is not used directly by `app.py`.

### Frontend/Backend Interaction

The project uses a server-rendered frontend:

- Frontend: static HTML/CSS inside Jinja2 templates
- Backend: Flask route handlers
- Communication: standard HTML form submission, not a separate JavaScript API

## Core Systems

### Dataset System

The dataset follows Keras' `flow_from_directory` convention:

```text
dataset/<class_name>/<image_files>
```

Detected classes:

- `cardboard`
- `ewaste`
- `glass`
- `metal`
- `organic`
- `paper`
- `plastic`
- `trash`

Class folder names must remain synchronized with the class order expected by the trained model and the `classes` list in `app.py`.

### Model Training System

Implemented in `train_model.py`.

Key responsibilities:

- Count dataset classes
- Load images from `dataset/`
- Split data into training and validation subsets
- Apply augmentation and normalization
- Build MobileNetV2 transfer learning model
- Fine-tune the last layers of the base model
- Train for 30 epochs
- Save output to `model/recycling_model.h5`

Training architecture:

```text
Input image 224x224x3
    -> MobileNetV2 base model, ImageNet weights, include_top=False
    -> GlobalAveragePooling2D
    -> Dense(128, relu)
    -> Dropout(0.5)
    -> Dense(8, softmax)
```

### Prediction System

Implemented in the `/predict` route in `app.py`.

Key responsibilities:

- Receive uploaded file from `request.files["image"]`
- Save the image to `uploads/`
- Load image at `224x224`
- Convert image to array
- Add batch dimension
- Normalize pixels using `/ 255.0`
- Run `model.predict(...)`
- Select the highest-probability class with `np.argmax`
- Build top-3 prediction list
- Render the final result page

### UI System

Implemented with Flask templates:

- `templates/index.html`: homepage and upload form
- `templates/result.html`: result page with prediction, image preview, top predictions, chart, environmental cards, and pollution map

Styling is currently embedded directly in the HTML templates for simplicity.

### File Handling

Runtime file locations:

- `uploads/`: stores user-uploaded images during local app execution
- `static/charts/prediction_chart.png`: generated prediction chart
- `static/maps/pollution_map.png`: generated pollution map image

Current file generation uses fixed output filenames for charts and maps. This is simple for local demos, but concurrent users may overwrite each other's outputs.

### Image Preprocessing

The preprocessing pipeline is intentionally aligned between training and inference:

```text
Load image
-> Resize to 224x224
-> Convert to array
-> Expand dimensions to create batch shape
-> Normalize pixel values to [0, 1]
-> Predict with TensorFlow/Keras model
```

### Environmental Information System

`app.py` contains dictionaries for:

- `waste_info`: pollution facts, recycling suggestions, and impact notes by class
- `pollution_levels`: country-level pollution intensity values by predicted material
- `map_locations`: marker-style coordinate data, currently not used in the active map rendering workflow

### Map Visualization System

The map system uses GeoPandas and Natural Earth shapefile assets in `maps/`.

Workflow:

1. Load world shapefile using `gpd.read_file(...)`.
2. Add a default pollution score to every country.
3. Override selected country scores based on the predicted class.
4. Plot a choropleth-style map with Matplotlib.
5. Save the output image to `static/maps/pollution_map.png`.

## Data Flow

### Training Data Flow

```text
dataset/ class folders
    -> ImageDataGenerator
    -> Training and validation batches
    -> MobileNetV2 transfer learning model
    -> model/recycling_model.h5
```

### Prediction Data Flow

```text
Browser image upload
    -> Flask `/predict`
    -> uploads/<filename>
    -> Keras image preprocessing
    -> TensorFlow model inference
    -> prediction probabilities
    -> top class + top-3 classes
    -> waste_info and pollution_levels lookup
    -> Matplotlib chart
    -> GeoPandas map
    -> result.html
```

## File Structure Breakdown

```text
app.py
```

Main web application. Defines Flask routes, loads the trained model, performs prediction, generates charts/maps, and renders templates.

```text
train_model.py
```

Training script for the MobileNetV2 transfer learning model.

```text
cnn model.py
```

Experimental simple CNN architecture. Useful for learning or comparison, but not integrated into the active web app.

```text
import_matplotlib.py / import matplotlib.py
```

Dataset distribution chart scripts. They currently contain duplicate logic.

```text
dataset/
```

Waste image dataset organized by class folder.

```text
model/
```

Contains the saved TensorFlow/Keras model expected by `app.py`.

```text
maps/
```

Contains Natural Earth shapefile components required for GeoPandas map rendering.

```text
templates/
```

Contains Jinja2 pages used by Flask.

```text
static/
```

Contains generated static outputs such as prediction charts and map images.

```text
uploads/
```

Runtime upload directory for user-submitted images.

## Design Patterns

Detected design and architectural patterns:

- **Model-View-Controller-like structure**: Flask route functions act as controllers, Jinja templates act as views, and the Keras model acts as the prediction model.
- **Transfer learning**: MobileNetV2 provides pretrained visual feature extraction.
- **Folder-per-class dataset convention**: standard Keras image classification structure.
- **Server-side rendering**: result pages are rendered on the backend with Jinja2.
- **Pipeline processing**: upload -> preprocess -> predict -> enrich -> visualize -> render.

## Deployment Notes

### Local Deployment

The current project is optimized for local execution:

```bash
python app.py
```

The app runs in Flask debug mode when executed directly. For production, use a WSGI server and disable debug mode.

### Docker

Docker is not currently configured. To add Docker support later, include:

- `Dockerfile`
- `.dockerignore`
- optional `docker-compose.yml`
- documented handling for the model, dataset, uploads, and generated static files

### Ollama

No Ollama integration is currently present. A future architecture could use Ollama for:

- conversational recycling assistant
- natural-language explanations of predictions
- location-specific disposal recommendations
- multilingual educational guidance

### Production Considerations

Before public deployment, consider adding:

- secure filename handling with `werkzeug.utils.secure_filename`
- file type and file size validation
- unique generated filenames per request
- disabled Flask debug mode
- dependency version pinning
- tests for prediction and routes
- model versioning
- structured logging