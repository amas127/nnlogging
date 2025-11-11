# nnlogging

![PyPI - Version](https://img.shields.io/pypi/v/nnlogging)
![PyPI - Downloads](https://img.shields.io/pypi/dm/nnlogging)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/nnlogging)
![GitHub License](https://img.shields.io/github/license/amas127/nnlogging)

[nnlogging](https://codeberg.org/nnaf/nnlogging) is a powerful, modern logging
library for neural network and machine learning experiments, combining
[Rich](https://github.com/Textualize/rich) for beautiful terminal output with
[Aim](https://github.com/aimhubio/aim) for comprehensive experiment tracking.

## ✨ Features

- 🎨 **Beautiful Console Output** - Rich-powered colorful logging with
  integrated progress bars.
- 📊 **Effortless Experiment Tracking** - Seamless Aim integration for metrics,
  parameters, and system monitoring.
- 🔧 **Simplified API** - Get started in one line of code with the global
  functions.
- 📈 **Advanced Progress Tracking** - Manage multiple progress bars for
  training, validation, and other tasks.
- 🎯 **ML-Focused Design** - Purpose-built for the machine learning workflow.
- 🐍 **Modern Python** - Fully typed, Python 3.10+ codebase.

## 🚀 Installation

```bash
pip install nnlogging
```

**Requirements:** Python 3.10-3.12

## ⚡ Quick Start

The new `nnlogging` API is designed for simplicity. You can get a
pre-configured, global logger instance and start logging right away.

### Basic Logging

Get the global shell or customize your shell from scratch to use logging methods
and trackings.

```python
import nnlogging

# Log messages!
nnlogging.info("Starting training...")
nnlogging.warn("Learning rate seems high.")
nnlogging.debug("This is a detailed debug message.")
nnlogging.error("CUDA out of memory.", extra={"show_locals": True})
```

### Experiment Tracking with Aim

Configure the Aim run to track metrics, hyperparameters, and more.

```python
import random
import nnlogging

# 1. Configure the experiment tracker
nnlogging.run_configure(
    experiment="resnet_training",
    log_system_params=True,      # Track CPU/GPU usage
    capture_terminal_logs=True   # Save console output in Aim
)

# 2. Log hyperparameters
config = {"lr": 0.001, "batch_size": 32, "model": "ResNet50"}
nnlogging.update_metadata("hparams", config)
nnlogging.info(f"Using config: {config}")

# 3. Track metrics in your training loop
for epoch in range(10):
    train_loss = 1.0 / (epoch + 1) + random.random() * 0.1
    nnlogging.track(train_loss, name="train_loss", epoch=epoch)
    nnlogging.info(f"Epoch {epoch}: Loss={train_loss:.4f}")

nnlogging.info("Experiment finished!")
```

To view the results, run `aim up` in your terminal.

### Progress Tracking

Add tasks to the logger to display and update rich progress bars.

```python
import time
import nnlogging

# 1. Add a task to the progress display
nnlogging.task_add("training", desc="Training", total=500)

# 2. Update the task during your training loop
for step in range(500):
    # training_step()
    time.sleep(0.01)
    nnlogging.advance("training", 1)

    if step % 100 == 0:
        nnlogging.info(f"Completed step {step}")

# 3. Remove the task when finished
nnlogging.task_remove("training")
nnlogging.info("Training complete!")
```

## 🔄 Workflow

1. **Import `nnlogging`** - Import the `nnlogging` library at the start of your
   script.
2. **`run_configure()`** - (Optional) Configure Aim for experiment tracking.
3. **Log & Track** - Use `nnlogging.info()`, `nnlogging.track()`, and
   `nnlogging.advance()` throughout your code.
4. **Visualize** - Run `aim up` to launch the Aim UI and analyze your results.

## 🤝 Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull
request.

## 📄 License

This project is licensed under the MIT License.
