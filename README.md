
# MecanoFlow

MecanoFlow is a typing application designed to improve typing speed and accuracy. The application offers different practice modes and provides detailed statistics about the user's performance.

## Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the dependencies using pip:

> [!TIP]
> It is recommended to use a virtual environment to install the dependencies.
> You can create a virtual environment with the following command:
> ```bash
> python -m venv venv
> ```

```bash
pip install -r requirements.txt
```

## Usage

To start the application, run the `main.py` file:

```bash
python main.py
```

## User Manual

### Main Interface

- **Application Bar**: Contains the logo, which changes color according to the theme.
- **Settings Bar**: Contains the menu for language selection and practice mode customization.
- **Typing Area**: This is where the practice text is displayed, and the user types.
- **Statistics**: Displays typing speed (WPM), accuracy, and errors.
- **Speed and Accuracy Chart**: A chart that appears after completing a practice session.

### Practice Modes

- **Timer Mode**: Practice for a fixed time (30, 60, 90, or 120 seconds).
- **Word Count Mode**: Practice by typing a fixed number of words (10, 20, 30, 40).

> [!IMPORTANT]
> There are many keyboard shortcuts you can use to enhance your user experience. You can view these shortcuts by hovering the cursor over the respective elements.
