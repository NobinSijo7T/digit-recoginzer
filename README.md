
# Digit Recognition Web App

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE) [![TensorFlow.js](https://img.shields.io/badge/TensorFlow.js-2.0-orange.svg)](https://www.tensorflow.org/js) [![Built with Keras](https://img.shields.io/badge/Keras-%E2%9A%A1-orange.svg)](https://keras.io)

A small client-side demo that recognizes handwritten digits (0–9) using a CNN trained on the MNIST dataset and exported to TensorFlow.js format for in-browser inference.

---

## Demo
Open the demo (after serving this folder) and draw a digit in the canvas, then press Predict.

## Tech stack

| Technology | Purpose | Logo |
|---|---:|:---:|
| TensorFlow / Keras | Model training and evaluation (Python) | ![Keras logo](https://img.shields.io/badge/Keras-%E2%9A%A1-orange.svg) |
| TensorFlow.js | Model inference in the browser | ![TF.js](https://img.shields.io/badge/TensorFlow.js-2.0-orange.svg) |
| HTML / CSS / JavaScript | Web UI and glue code | ![JS](https://img.shields.io/badge/HTML%2FCSS%2FJS-lightgrey.svg) |
| Bootstrap | Layout & responsive utilities | ![Bootstrap](https://img.shields.io/badge/Bootstrap-4.3-blue.svg) |

---

## Train the model (overview)
This project uses a simple CNN trained on MNIST using Keras. Below are condensed, reproducible steps to train the model locally.

Requirements
- Python 3.8+
- pip
- virtualenv (optional but recommended)

Create environment and install:

```bash
python -m venv venv
venv\Scripts\activate    # Windows
# or: source venv/bin/activate  # macOS / Linux
pip install --upgrade pip
pip install tensorflow keras numpy matplotlib
```

Training script (example)

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# load MNIST
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
x_train = x_train[..., None] / 255.0
x_test = x_test[..., None] / 255.0

# simple CNN
model = keras.Sequential([
  layers.Conv2D(32, 3, activation='relu', input_shape=(28,28,1)),
  layers.BatchNormalization(),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, activation='relu'),
  layers.BatchNormalization(),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dropout(0.4),
  layers.Dense(128, activation='relu'),
  layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=128, epochs=12, validation_split=0.1)

# evaluate
print(model.evaluate(x_test, y_test))

# save Keras model
model.save('models/keras_model.h5')
```

Model tips & notes
- Use Data Augmentation or adjust dropout if you overfit.
- Training longer (more epochs) and increasing model capacity can improve accuracy beyond ~99% depending on setup.

---

## Convert to TensorFlow.js format
Install the converter and convert the .h5 model to TF.js Layers format used by the web app:

```bash
pip install tensorflowjs
mkdir -p models
tensorflowjs_converter --input_format=keras models/keras_model.h5 models/tfjs_model
```

This will produce a `model.json` plus weight shard files you can serve with the web app.

---

## Run locally (simple static server)
From the repository root:

```bash
# Python 3
python -m http.server 8000
# open http://localhost:8000 in your browser
```

---

## Project structure
```
index.html
css/
  styles.css
js/
  main.js
models/
  model.json (tfjs)
  group1-shard1of1.bin
  models.h5 (keras)
```

---

## Useful repository widgets (suggestions)
- Add GitHub Actions workflow for CI to run linting and tests.
- Add a small badge for demo status or latest commit.
- Consider publishing the model artifacts as releases or store them in GitHub Pages/Cloud Storage for production usage.

---

## License
MIT — see `LICENSE`.

If you'd like, I can add GitHub-flavored badges (build, coverage, license), plus a small GitHub Actions workflow to run a test script automatically on push.

