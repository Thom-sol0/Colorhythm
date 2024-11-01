# INF573 Project - Colorythm

Objective: Generate scores/melody from an image of colorful paper sliders.

## Installation

1. Clone the repo:
   ```bash
   git clone https://gitlab.binets.fr/thomas.pouponneau/colorhythm.git
   # or git clone git@gitlab.binets.fr:thomas.pouponneau/colorhythm.git for development
   cd path/to/colorythm
   ```

2. Install the virtual environment and its dependencies:
   ```bash
   pip install poetry # if not already installed
   poetry install
   poetry shell # connect to the venv
   # poetry add dependency_name # to install dependencies
   ```

## Get started

   To check if your video source works, run the following and find the right source number by testing among the available sources. (exit with q)
   ```bash
   python tests/video_test.py
   ```
   
