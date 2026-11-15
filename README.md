# Workout-Plan-Generator
An LLM-powered Workout Plan Generator built with Streamlit and the Groq API that creates personalized workout plans based on individual fitness goals, experience levels, available equipment, workout preferences, and physical limitations.


## 🚀 Features

- **Personalized Workout Plans:** Generate workout routines based on individual fitness goals.
- **LLM-Powered:** Uses Large Language Models (LLMs) through Groq API.
- **Structured JSON Output:** Generates workout plans using JSON Schema for consistent responses.
- **Daily Workout Cards:** Displays exercises organized by workout days.
- **Input Validation:** Handles invalid inputs and clarification requests.
- **Fitness Goal Support:** Helps users plan workouts for muscle building, weight loss, strength, and general fitness.

## 🛠️ Tech Stack

- **Python** – Backend development
- **Streamlit** – User interface
- **Groq API** – LLM inference
- **JSON Schema** – Structured output validation

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-workout-planner.git
```

### 2. Navigate to the project directory

```bash
cd ai-workout-planner
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key
```

Get your API key from [Groq Console](https://console.groq.com/).

### 6. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 🧠 How It Works

1. User enters fitness information and workout preferences.
2. The application sends the input to the Groq LLM API.
3. The LLM generates a personalized workout plan.
4. JSON Schema ensures a structured response.
5. Streamlit displays the generated workout plan in individual daily cards.

## 📌 Example Output

```json
{
  "status": "success",
  "message": "Workout plan generated successfully",
  "workout_plan": [
    {
      "day": "Monday",
      "focus": "Chest and Triceps",
      "exercises": [
        {
          "name": "Bench Press",
          "sets": "3",
          "reps": "12"
        },
        {
          "name": "Push-ups",
          "sets": "3",
          "reps": "15"
        }
      ]
    }
  ]
}
```
