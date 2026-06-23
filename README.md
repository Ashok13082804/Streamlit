# 🚀 Streamlit AI Applications Suite

A collection of interactive Streamlit web applications powered by Google Gemini AI. This suite includes tools for AI-based quizzes, meme generation, language tutoring and audio translation, mathematical problem solving, camera image processing, and YouTube channel insights.

---

## 📋 Table of Contents
1. [Module Analysis](#-module-analysis)
2. [Prerequisites & External Dependencies](#-prerequisites--external-dependencies)
3. [Environment Setup](#%EF%B8%8F-environment-setup)
   - [macOS / Linux](#macos--linux)
   - [Windows (Command Prompt / PowerShell)](#windows-command-prompt--powershell)
4. [Running the Applications Separately](#-running-the-applications-separately)
   - [1. AI Quiz Game (`Quiz.py`)](#1-ai-quiz-game-quizpy)
   - [2. Meme Generator (`img.py`)](#2-meme-generator-imgpy)
   - [3. Language Tutor & Translator (`lang.py`)](#3-language-tutor--translator-langpy)
   - [4. Math Solver (`new.py`)](#4-math-solver-newpy)
   - [5. Photo Filter App (`pic.py`)](#5-photo-filter-app-picpy)
   - [6. YouTube Analytics (`yt.py`)](#6-youtube-analytics-ytpy)
5. [API Key Configuration](#-api-key-configuration)

---

## 🔍 Module Analysis

Here is a breakdown of the Python modules included in this workspace:

| Module File | Name | Description | Key Libraries Used |
| :--- | :--- | :--- | :--- |
| [Quiz.py](file:///Users/ashokkumar/Downloads/streamlit/Quiz.py) | **AI Quiz Game** | Generates multiple-choice quizzes dynamically based on user-supplied topics and count of questions. Validates scores at the end. | `streamlit`, `google-generativeai` |
| [img.py](file:///Users/ashokkumar/Downloads/streamlit/img.py) | **Meme Generator** | Upload an image and generate creative/funny captions using Gemini. Draw top/bottom styled meme text onto the image. | `streamlit`, `Pillow`, `google-generativeai` |
| [lang.py](file:///Users/ashokkumar/Downloads/streamlit/lang.py) | **Language Tutor & Translator** | Translate written text or transcribed speech (from uploaded audio files) into target languages. Generates a mini comprehension quiz. | `streamlit`, `SpeechRecognition`, `pydub`, `google-generativeai` |
| [new.py](file:///Users/ashokkumar/Downloads/streamlit/new.py) | **Math Problem Solver** | Input math equations or word problems and get detailed, step-by-step educational solutions explained by Gemini AI. | `streamlit`, `google-generativeai` |
| [pic.py](file:///Users/ashokkumar/Downloads/streamlit/pic.py) | **Photo Filters App** | Take a photo via webcam or upload one. Features computer vision filter options (grayscale, sepia, blur, cartoon) and Gemini analysis. | `streamlit`, `opencv-python`, `numpy`, `Pillow`, `google-generativeai` |
| [yt.py](file:///Users/ashokkumar/Downloads/streamlit/yt.py) | **YouTube Analytics** | Analyze a YouTube channel URL to infer likely content topics, target demographics, posting frequency, and tips for engagement. | `streamlit`, `google-generativeai`, `re` |

---

## ⚙️ Prerequisites & External Dependencies

### 1. Python
Ensure you have **Python 3.9** or higher installed on your system.

### 2. Audio Processing (Required for `lang.py`)
`lang.py` utilizes the `pydub` library to process uploaded audio files. `pydub` requires **FFmpeg** to handle compressed audio formats (such as MP3, M4A, AAC, etc.).

* **macOS Installation (using Homebrew):**
  ```bash
  brew install ffmpeg
  ```
* **Windows Installation:**
  * **Option A (PowerShell - Winget):**
    ```powershell
    winget install Gypsey.FFmpeg
    ```
  * **Option B (Chocolatey):**
    ```cmd
    choco install ffmpeg
    ```
  * **Option C (Manual):** Download static binaries from [ffmpeg.org](https://ffmpeg.org/download.html), extract them, and add the `bin` folder path to your system environment variables (`PATH`).

---

## 🛠️ Environment Setup

Navigate to your project directory inside your terminal:
```bash
cd /Users/ashokkumar/Downloads/streamlit
```

### macOS / Linux
```bash
# 1. Create a virtual environment named 'venv'
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install all Python dependencies
pip install -r requirements.txt
```

### Windows (Command Prompt / PowerShell)

#### Using Command Prompt (cmd)
```cmd
:: 1. Create a virtual environment named 'venv'
python -m venv venv

:: 2. Activate the virtual environment
call venv\Scripts\activate.bat

:: 3. Upgrade pip
pip install --upgrade pip

:: 4. Install all Python dependencies
pip install -r requirements.txt
```

#### Using PowerShell
```powershell
# 1. Create a virtual environment named 'venv'
python -m venv venv

# 2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 3. Upgrade pip
pip install --upgrade pip

# 4. Install all Python dependencies
pip install -r requirements.txt
```

> [!NOTE]
> If you get an execution policy error on PowerShell while activating the environment, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

> [!TIP]
> **Streamlit Onboarding Prompt:** On your first run, Streamlit may ask for an email address (`Email:`). 
> * You can simply press **Enter** (leave it blank) to bypass it.
> * We have pre-configured `gatherUsageStats = false` inside [.streamlit/config.toml](file:///Users/ashokkumar/Downloads/streamlit/.streamlit/config.toml) to prevent usage statistics prompt.

---

## 🚀 Running the Applications Separately

Ensure your virtual environment is **activated** before running any of the commands below.

### 1. AI Quiz Game (`Quiz.py`)
Generates multiple-choice quizzes dynamically based on user topics.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run Quiz.py
  ```

### 2. Meme Generator (`img.py`)
Generates funny meme captions and adds custom text to uploaded images.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run img.py
  ```

### 3. Language Tutor & Translator (`lang.py`)
Performs speech recognition on audio files, translates languages, and hosts quizzes.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run lang.py
  ```

### 4. Math Solver (`new.py`)
Generates detailed step-by-step solutions to mathematical equations.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run new.py
  ```

### 5. Photo Filter App (`pic.py`)
Webcam and file upload photo booth with computer vision filters and Gemini analysis.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run pic.py
  ```

### 6. YouTube Analytics (`yt.py`)
Extracts channel tags and outputs audience reach suggestions.
* **macOS / Linux / Windows:**
  ```bash
  streamlit run yt.py
  ```

---

## 🔑 API Key Configuration

The applications support loading a custom Google Gemini API key through multiple methods (precedence from highest to lowest):

### 1. Directly in the App Sidebar (Recommended for local runs)
When you run any of the applications, a configuration section is displayed in the **sidebar**:
1. Go to the sidebar on the left side of the app.
2. Enter your custom Gemini API key into the password text input field.
3. The application will instantly switch to using your custom key. 
4. If you don't have a key, click the link in the sidebar to create a free one on [Google AI Studio](https://aistudio.google.com/).

### 2. Environment Variables
You can export the API key as an environment variable before running the applications:
* **macOS / Linux:**
  ```bash
  export GEMINI_API_KEY="your-actual-api-key"
  ```
* **Windows (Command Prompt):**
  ```cmd
  set GEMINI_API_KEY=your-actual-api-key
  ```
* **Windows (PowerShell):**
  ```powershell
  $env:GEMINI_API_KEY="your-actual-api-key"
  ```

### 3. Streamlit Secrets
For local development or deployment on Streamlit Cloud, you can use a secrets file:
1. Create a directory named `.streamlit` in the project root folder.
2. Create a file named `secrets.toml` inside `.streamlit/`.
3. Add the following entry:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"
   ```
