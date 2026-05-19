# Development Guide

This guide explains how to set up, run, debug, and extend the Smart Recycling App project.

## Required Software

Install the following tools before starting:

- **Python 3.10+** recommended
- **Git** for version control
- **VS Code** or another code editor
- **pip** for installing Python packages

Optional tools:

- **Docker Desktop** if Docker support is added in the future
- **Ollama** if local LLM recycling assistance is added in the future

## Python Setup

Check that Python is installed:

```bash
python --version
```

If this command fails, install Python from the official website and make sure the `Add Python to PATH` option is enabled on Windows.

## Virtual Environment Setup

Create a virtual environment in the project root:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

When activated, your terminal prompt should show `(venv)`.

## Dependency Installation

Install project dependencies:

```bash
pip install -r requirements.txt
```

Main libraries used by the app:

- `Flask`
- `tensorflow`
- `numpy`
- `matplotlib`
- `geopandas`
- `folium`
- `Pillow`
- `h5py`

### GeoPandas note

GeoPandas depends on geospatial libraries. If installation fails, update pip first:

```bash
python -m pip install --upgrade pip
```

Then retry:

```bash
pip install -r requirements.txt
```

If the issue continues, install GeoPandas using the official instructions for your operating system.

## Running Locally

Start the Flask application:

```bash
python app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

Then:

1. Click the file input.
2. Select a waste image.
3. Click **Analyser le déchet**.
4. Review the predicted class, confidence, chart, and pollution map.

## Running with Docker

Docker is not currently configured for this project. There is no `Dockerfile` or `docker-compose.yml` yet.

If Docker support is added later, the expected workflow will be similar to:

```bash
docker build -t smart-recycling-app .
docker run -p 5000:5000 smart-recycling-app
```

Before adding Docker, document how the container handles:

- `model/recycling_model.h5`
- `dataset/`
- `uploads/`
- generated files in `static/charts/` and `static/maps/`
- GeoPandas system dependencies

## Ollama / Local LLM Development

Ollama is not currently integrated.

Possible future use cases:

- chatbot-style recycling assistant
- personalized recycling instructions
- natural-language explanations of model predictions
- multilingual environmental education

If Ollama is added later, document:

- required model name
- installation steps
- fallback behavior when Ollama is unavailable
- privacy and offline usage assumptions

## Debugging Tips

### App does not start

Check that the virtual environment is activated and dependencies are installed:

```bash
pip install -r requirements.txt
```

### Model file not found

The app expects:

```text
model/recycling_model.h5
```

If it is missing, retrain the model or restore the model artifact.

### Map generation fails

Verify that the shapefile components exist in `maps/`:

```text
ne_110m_admin_0_countries.shp
ne_110m_admin_0_countries.shx
ne_110m_admin_0_countries.dbf
ne_110m_admin_0_countries.prj
```

All shapefile components should stay together.

### Uploaded image does not display

Check that the image was saved under `uploads/` and that Flask can serve the path used by the template.

### Prediction results look wrong

Verify that these three class definitions are aligned:

1. `dataset/` folder order used during training
2. the trained model output order
3. the `classes` list in `app.py`

Changing class order without retraining or validating the mapping can produce incorrect labels.

## How to Retrain the ML Model

Before training, verify the dataset structure:

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

Run training:

```bash
python train_model.py
```

The script will:

1. Load images from `dataset/`
2. Apply preprocessing and augmentation
3. Train a MobileNetV2 transfer learning model
4. Save the model to `model/recycling_model.h5`

Training can take time depending on hardware. Do not run long training jobs unless you intentionally want to update the model.

## How to Test Predictions

### Manual browser test

1. Start the app:

   ```bash
   python app.py
   ```

2. Open:

   ```text
   http://127.0.0.1:5000
   ```

3. Upload a sample image from one of the dataset folders.
4. Confirm that the result page shows:
   - predicted class
   - confidence score
   - top-3 predictions
   - environmental information
   - chart image
   - pollution map image

### Lightweight route check

You can verify that the Flask app imports successfully:

```bash
python -m py_compile app.py train_model.py import_matplotlib.py
```

This does not test model accuracy, but it catches Python syntax errors.

## Development Best Practices

- Keep changes small and easy to review.
- Avoid committing local uploads, generated charts, generated maps, or `venv/`.
- Keep `224x224` image size consistent between training and prediction.
- Do not rename dataset class folders without updating labels and retraining/validating the model.
- Add new documentation when changing setup, dependencies, architecture, or model behavior.
- Use clear commit messages, for example:

```bash
git commit -m "Improve prediction documentation"
```

## Recommended Next Improvements

- Add automated tests for Flask routes and preprocessing.
- Add secure filename handling for uploads.
- Add file extension and file size validation.
- Add unique output filenames for generated charts/maps.
- Pin dependency versions after confirming a working environment.
- Add model evaluation metrics after training.