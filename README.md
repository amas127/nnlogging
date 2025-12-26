# nnlogging

[![status-badge](https://ci.codeberg.org/api/badges/15742/status.svg)](https://ci.codeberg.org/repos/15742)
[![PyPI - Version](https://img.shields.io/pypi/v/nnlogging)](https://pypi.org/project/nnlogging/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nnlogging)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nnlogging)
![PyPI - License](https://img.shields.io/pypi/l/nnlogging)

[nnlogging](https://codeberg.org/amas127/nnlogging.git) is a logging extension
designed for machine learning experiments and competitions.

[nnlogging](https://codeberg.org/amas127/nnlogging.git) is mostly built on
[Rich](https://github.com/Textualize/rich.git), [DuckDB](https://duckdb.org) and
[DVC](https://dvc.org/).

## Features

- **Modern Logging Record:** With pre-configured but customizable `rich`
  settings, `nnlogging` handles logs as modern and structured records.

- **Extendable Tracking History:** `nnlogging` leverages `duckdb` to store
  experiment metadata and data (tags, artifacts, ...).

- **Run Commit Solution:** `nnlogging` treats every run of any experiments as a
  git commit point.

## Installation

```sh
pip install nnlogging  # Python >= 3.10
```

## Quick Start

The new `nnlogging` API is designed for simplicity. You can get a
pre-configured, global logger instance and start logging right away.

### Basic Logging

Add a branch to the root logger and start logging messages.

```python
import nnlogging

# 0. Configure logger levels
nnlogging.configure_logger([None], level="DEBUG")

# 1. Add a console branch to root logger
nnlogging.add_branch(("console", "stdout"))

# 2. Log messages!
nnlogging.info(__name__, "Starting training...")
nnlogging.warning(__name__, "Learning rate seems high.")
nnlogging.debug(__name__, "This is a detailed debug message.")
nnlogging.error(__name__, "CUDA out of memory.")
```

### Experiment Tracking

Configure experiment tracking to store metrics, hyperparameters, and more in
DuckDB tables.

```python
import uuid
import nnlogging

# 1. Configure the experiment run
nnlogging.configure_run(experiment="resnet_training", uuid=uuid.uuid4(), run="run_1")

# 2. Log hyperparameters
nnlogging.add_hparams({"lr": 0.001, "batch_size": 32, "model": "ResNet50"})

# 3. Track metrics in your training loop
for epoch in range(10):
    train_loss = 1.0 / (epoch + 1)
    nnlogging.track(step=epoch, metrics={"train_loss": train_loss})
    nnlogging.info(None, f"Epoch {epoch}: Loss={train_loss:.4f}")

# 4. Close run to tell when the run is finished
nnlogging.close_run()
```

### Progress Tracking

Add tasks to display and update rich progress bars.

```python
import time
import nnlogging

# 0. Add at least 1 branch to show progress
nnlogging.add_branch(("stderr", "stderr"))

# 1. Add a task to the progress display
nnlogging.add_task("training", total=100)

# 2. Update the task during your training loop
for step in range(100):
    time.sleep(0.01)
    nnlogging.advance("training", 1)

# Tasks will be recycled when finished
```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull
request.

## License

This project is licensed under the MIT License.
