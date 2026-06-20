# Contributing to Food Freshness Image Prediction System

First off, thank you for taking the time to contribute! Contributions are what make the open-source community such an amazing place to learn, inspire, and create.

All types of contributions are welcome, from reporting bugs to submitting feature requests or implementing code improvements.

---

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to **<jewimaluwi2019@gmail.com>**.

---

## How Can I Contribute?

### Reporting Bugs

Before submitting a bug report, please check the existing issues to see if it has already been reported. When creating a bug report, please use the **Bug Report Template** and include:

* A clear and descriptive title.
* Steps to reproduce the issue.
* Expected vs actual behavior.
* Relevant environment details (OS, Python version, library versions).
* Error logs and screenshots if applicable.

### Suggesting Enhancements

If you have an idea to improve the system, please open an issue using the **Feature Request Template**. Include:

* A clear description of the enhancement.
* The problem it solves.
* Any alternative solutions or workarounds considered.

### Submitting Pull Requests

1. **Fork the Repository** and clone it locally.
2. **Create a Branch** for your feature or fix: `git checkout -b feature/your-feature-name`.
3. **Set Up the Development Environment** (see below).
4. **Make Your Changes** and ensure the code follows style guidelines.
5. **Run Verification Checks** to verify that everything works correctly.
6. **Commit Your Changes** with clear commit messages.
7. **Push to Your Fork** and open a Pull Request against the `main` branch.

---

## Development Environment Setup

This project uses Python, FastAPI, Gradio, and MongoDB.

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nickymarzz/Food-Freshness-Image-Prediction-System.git
   cd Food-Freshness-Image-Prediction-System
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Copy `.env.example` to `.env` and fill in your MongoDB connection details:

   ```bash
   cp .env.example .env
   ```

5. **Run the Application Locally**:

   ```bash
   python -m src.app.app
   ```

---

## Style & Standards

* **Code Style**: Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
* **Docstrings**: Document classes, methods, and functions using clear docstrings.
* **Formatting**: Keep code clean, avoid trailing whitespace, and ensure correct import formatting.
* **No Mutating Inputs**: Avoid modifying input arguments in-place unless intended. Make sure functions return new copies if modifications are made (e.g. annotation pipelines).
