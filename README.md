# nnlogging

A powerful logging library for neural network and machine learning experiments
that combines [Rich](https://github.com/Textualize/rich) for beautiful terminal
output with [Aim](https://github.com/aimhubio/aim) for comprehensive experiment
tracking.

## ✨ Features

- 🎨 **Beautiful Console Output** - Rich-powered colorful logging with progress
  bars
- 📊 **Experiment Tracking** - Built-in Aim integration for metrics and
  hyperparameters
- 🔧 **Flexible Logging** - Multiple console handlers with customizable
  formatting
- 📈 **Progress Tracking** - Advanced progress bars for long-running training
  loops
- 🎯 **ML-Focused Design** - Purpose-built for machine learning workflows
- 🐍 **Modern Python** - Python 3.10+ with full type hints

## 🚀 Installation

```bash
pip install nnlogging
```

**Requirements:** Python 3.10-3.12

## ⚡ Quick Start

### Basic Logging

```python
from nnlogging import Shell
from nnlogging.utils import get_rich_console
import sys

# Initialize logger
shell = Shell(name="my_experiment")
shell.add_console({"main": get_rich_console(sys.stderr)})
shell.build_handler_from_console()

# Log messages
shell.info("Starting training...")
shell.warn("Learning rate is high")
shell.error("CUDA out of memory")
```

### Experiment Tracking

```python
# Initialize Aim tracking
shell.add_aimrun(experiment="resnet_training")

# Track metrics during training
for epoch in range(100):
    train_loss, train_acc = train_epoch()
    shell.track(train_loss, name="train_loss", epoch=epoch)
    shell.track(train_acc, name="train_accuracy", epoch=epoch)

    shell.info(f"Epoch {epoch}: Loss={train_loss:.4f}, Acc={train_acc:.3f}")

# Track hyperparameters
shell.update_aimrun_metadata("config", {
    "learning_rate": 0.001,
    "batch_size": 32,
    "model": "ResNet50"
})
```

### Progress Tracking

```python
# Setup progress bars
shell.build_progress_from_console("main")
shell.add_task("training", description="Training", total=1000)
shell.start_progress()

# Update during training loop
for step in range(1000):
    loss = train_step()
    shell.update_task("training", advance=1)

    if step % 100 == 0:
        shell.info(f"Step {step}: Loss={loss:.4f}")

shell.stop_progress()
```

### Complete Training Example

```python
from nnlogging import Shell
from nnlogging.utils import get_rich_console
import sys

# Setup logging with both console and experiment tracking
shell = Shell(name="training")
shell.add_console({"console": get_rich_console(sys.stdout)})
shell.build_handler_from_console()
shell.build_progress_from_console()

# Initialize experiment tracking
shell.add_aimrun(
    experiment="mnist_cnn",
    log_system_params=True,
    capture_terminal_logs=True
)

# Log hyperparameters
config = {"lr": 0.001, "batch_size": 64, "epochs": 10}
shell.update_aimrun_metadata("hparams", config)
shell.info(f"Starting training with config: {config}")

# Training loop with progress tracking
shell.add_task("epochs", description="Epochs", total=config["epochs"])
shell.start_progress()

for epoch in range(config["epochs"]):
    # Training phase
    train_loss, train_acc = train_model()
    shell.track(train_loss, name="train_loss", epoch=epoch)
    shell.track(train_acc, name="train_acc", epoch=epoch)

    # Validation phase
    val_loss, val_acc = validate_model()
    shell.track(val_loss, name="val_loss", epoch=epoch)
    shell.track(val_acc, name="val_acc", epoch=epoch)

    shell.update_task("epochs", advance=1)
    shell.info(f"Epoch {epoch}: Train Loss={train_loss:.3f}, Val Acc={val_acc:.3f}")

shell.stop_progress()
shell.info("Training completed! 🎉")
```

## 🔄 Workflow

![Workflow Overview](assets/workflow-overview.png)

1. **Initialize** - Create Shell instance for your experiment
2. **Configure** - Add consoles and progress tracking
3. **Track** - Connect to Aim for experiment tracking
4. **Train & Log** - Use throughout your ML pipeline
5. **Visualize** - View results in Aim's web interface with `aim up`

## 🌍 Environments

nnlogging works seamlessly across different environments:

- **Local Development** - Full Rich terminal output with colors and formatting
- **Jupyter Notebooks** - Integrated display with notebook-friendly rendering
- **Remote Servers** - Automatic fallback for limited terminal capabilities
- **CI/CD Pipelines** - Clean text output when Rich features aren't supported
- **Docker Containers** - Optimized for containerized ML workloads

## 🤝 Contributing

Contributions welcome! Please open an issue for major changes.

## 📄 License

MIT License
