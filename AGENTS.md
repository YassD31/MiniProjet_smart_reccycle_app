# AGENTS.md

Guidance for AI coding agents and automated assistants working on the Smart Recycling App repository.

## Project Overview

Smart Recycling App is a Python/Flask machine learning web application for classifying waste images into recycling categories. It uses a TensorFlow/Keras model trained with MobileNetV2, serves a browser-based upload workflow, and generates environmental information, prediction charts, and pollution map visualizations.

## Repository Structure

```text
app.py                    # Flask app, routes, prediction pipeline, chart/map generation
train_model.py            # MobileNetV2 training workflow
cnn model.py              # Experimental simple CNN architecture
import_matplotlib.py      # Dataset distribution chart script
dataset/                  # Image dataset organized by class folders
model/                    # Saved Keras model used by the Flask app
maps/                     # Shapefile assets for GeoPandas map generation
templates/                # Jinja2 HTML pages
static/charts/            # Runtime-generated prediction charts
static/maps/              # Runtime-generated map outputs
uploads/                  # Runtime image uploads
```

## Coding Conventions

- Use clear, beginner-friendly Python code.
- Keep Flask route logic readable and avoid unnecessary abstraction unless the app grows.
- Use `snake_case` for Python variables, functions, and filenames when possible.
- Keep ML class labels synchronized between:
  - `dataset/` folder names
  - `classes` in `app.py`
  - the trained model output order
- Prefer small, focused changes over large rewrites.
- Document non-obvious ML, preprocessing, or geospatial logic.

## Folder Responsibilities

- `dataset/`: training and validation images. Do not rename class folders without updating model training and inference labels.
- `model/`: trained model artifacts. `app.py` currently expects `model/recycling_model.h5`.
- `uploads/`: local runtime uploads. Do not commit user-uploaded files.
- `static/charts/` and `static/maps/`: generated outputs. Keep directories, but avoid committing generated runtime images.
- `maps/`: required shapefile components. Keep `.shp`, `.shx`, `.dbf`, `.prj`, and related metadata together.
- `templates/`: user-facing HTML pages. Keep form field names aligned with Flask request handling.

## Safe Modification Rules

Do:

- Read existing files before editing.
- Preserve the current `/` and `/predict` user workflow unless explicitly asked to change it.
- Validate changes with lightweight commands where possible.
- Keep generated files and local environments ignored through `.gitignore`.
- Add tests or small helper functions when changing preprocessing or prediction logic.

Don't:

- Delete or rename `dataset/`, `model/recycling_model.h5`, or `maps/` without user confirmation.
- Commit `venv/`, runtime uploads, generated charts, or generated maps.
- Change model input size from `224x224` without updating training and inference together.
- Reorder class labels in `app.py` unless the model is retrained or label mapping is verified.
- Add Docker, Ollama, or external service dependencies without documenting setup and fallback behavior.

## Naming Conventions

- Python files: prefer `snake_case.py`.
- Model files: use descriptive names such as `recycling_model.h5` or `recycling_model.keras`.
- Dataset classes: lowercase folder names such as `plastic`, `metal`, `ewaste`.
- Generated assets: use unique request-safe filenames if multiple users or concurrent requests are supported.

## AI Agent Do / Don't Guidelines

### Do

- Explain major actions briefly before making changes.
- Keep changes compatible with the current beginner-friendly project style.
- Update documentation when behavior, dependencies, setup, or architecture changes.
- Check `git status` before commits or major file operations.
- Stop and ask if a change could delete large assets or alter trained-model behavior.

### Don't

- Run long training jobs unless explicitly requested.
- Install heavy packages unnecessarily.
- Retry failing commands repeatedly; after two failures, explain the issue and ask for guidance.
- Push to GitHub without confirming the remote repository URL.
- Store secrets, API keys, or local machine paths in committed files.

## Git Workflow Recommendations

1. Check the current state:

   ```bash
   git status
   ```

2. Make focused edits.
3. Review changed files:

   ```bash
   git diff
   ```

4. Stage and commit with a clear message:

   ```bash
   git add .
   git commit -m "Describe the change"
   ```

5. Before adding a remote or pushing, confirm the intended GitHub repository URL with the user.