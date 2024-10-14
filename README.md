Here is the content for your `README.md` file:

# PLoM-GUI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Graphical User Interface (GUI) for the Probability Learning on Manifolds (PLoM) framework.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Install Dependencies](#install-dependencies)
  - [Install Package](#install-package)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

PLoM-GUI is a user-friendly interface for the PLoM framework, designed to simplify the process of probability learning on manifolds. It provides an interactive environment for data analysis, visualization, and model building without the need for extensive coding.

## Features

- Intuitive graphical interface for PLoM functionalities
- Data import and preprocessing tools
- Visualization of datasets and manifold structures
- Data sampling on manifold
- Interactive parameter tuning and real-time feedback
- Feature importance ranking
- Automation of forward model(s) consturction

## Installation

### Prerequisites

- Python 3.6 or higher
- Required Python packages (listed in `requirements.txt`)

### Clone the Repository

```bash
git clone https://github.com/philippehawi/PLoM-GUI.git
cd PLoM-GUI
```

### Install Dependencies

This GUI package requires, among others, the [PLoM Python package](https://github.com/philippehawi/PLoM). To install this dependency, run the following command from the root of `PLoM-GUI`.
```bash
pip install -r requirements.txt
```

### Install Package

After downloading the repository, run the following command from the root of `PLoM-GUI`.
```bash
pip3 install .
```
If the above command hangs on Windows WSL2, you may need to clear the DISPLAY environment variable first:
```bash
export DISPLAY=
```

## Usage

To launch the PLoM-GUI application, run the following command from the terminal:

```bash
plom-gui
```

NOTE: You might need to add the directory where Python places the installed scripts to your system’s PATH environment variable. During the installation of this package, a warning is usually displayed if this scripts directory is not in PATH, and the full path is printed. An example of the scripts path: 

```bash
C:\Users\<YourUser>\AppData\Roaming\Python\PythonXX\Scripts\
```

Follow the on-screen instructions to load your dataset, configure parameters, and start the analysis.

## Examples

Explore the [examples](examples/) directory for sample datasets and projects to help you get started with PLoM-GUI.

## Contributing

Contributions are welcome! Please read our [contribution guidelines](CONTRIBUTING.md) before submitting a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact:

- Philippe Hawi - [philippehawi@gmail.com](mailto:philippehawi@gmail.com)