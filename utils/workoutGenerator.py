
import json
from typing import Optional

from groq import (
    Groq,
    APIConnectionError,
    APIStatusError,
    RateLimitError
)

from config import GROQ_API_KEY


def generate_workout_plan(
    fitness_goal: str,
    experience_level: str,
    days_per_week: int,
    equipment: str,
    injuries: Optional[str] = None
) -> dict[str, str]:
    """
    Generate a personalized workout plan using Groq API.

    Returns:
        A dictionary containing status, message and workout_plan.
    """

    # --------------------------------
    # 1. Validate API configuration
    # --------------------------------

    if not GROQ_API_KEY:
        return {
            "status": "error",
            "message": "Groq API key is missing. Please configure your .env file.",
            "workout_plan": ""
        }

    # --------------------------------
    # 2. Validate user inputs
    # --------------------------------

    valid_goals = [
        "Build muscle",
        "Lose fat",
        "General fitness",
        "Improve endurance"
    ]

    valid_levels = [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]

    valid_equipment = [
        "No equipment",
        "Home dumbbells",
        "Full gym"
    ]

    if fitness_goal not in valid_goals:
        return {
            "status": "invalid_input",
            "message": "Please select a valid fitness goal.",
            "workout_plan": ""
        }

    if experience_level not in valid_levels:
        return {
            "status": "invalid_input",
            "message": "Please select a valid experience level.",
            "workout_plan": ""
        }

    if type(days_per_week) is not int or not 1 <= days_per_week <= 7:
        return {
            "status": "invalid_input",
            "message": "Workout days must be between 1 and 7.",
            "workout_plan": ""
        }

    if equipment not in valid_equipment:
        return {
            "status": "invalid_input",
            "message": "Please select valid workout equipment.",
            "workout_plan": ""
        }

    # --------------------------------
    # 3. Prepare system prompt
    # --------------------------------

    system_prompt = """
    You are a professional fitness workout planning assistant.

    Your task is is to generate safe, practical and personalized
    workout plans based on user-provided fitness information.
    
    IMPORTANT: Before generating a workout plan, analyze the
    user's injuries, limitations and additional comments.

    LIMITATION VALIDATION RULES:

    1. If no limitations are provided, generate a normal
       workout plan suitable for the user's fitness level.

    2. If the user provides a relevant exercise restriction,
       such as bad knees, back pain or no overhead pressing,
       create a modified workout plan that respects the restriction.

    3. If the user provides unrelated information, such as
       travel plans, hobbies, random sentences or unrelated
       questions, DO NOT generate a workout plan.

       Return status "invalid_input" and politely ask the user
       to provide a fitness-related injury or limitation.

    4. If the limitation is unclear, return status "clarification"
       and ask the user for more information.

    5. If the user mentions a serious medical condition,
       recent surgery, severe injury, chest pain, fainting,
       or other concerning symptoms, return status "medical_review".
       Recommend appropriate medical assessment before exercise.
       Do not prescribe exercises for that condition.

    6. Never diagnose a medical condition.

    7. Never claim that an exercise is medically safe for an injury.

    8. Never recommend exercises that conflict with stated
       physical restrictions.

    9. Do not interpret unrelated information as a fitness
       limitation just to generate a workout.



    SAFETY RULES:
    - Never diagnose medical conditions.
    - Never recommend exercises that conflict with stated limitations.
    - If medical assessment is needed, do not generate a workout plan.
    - Ask for clarification if an injury or limitation is unclear.
    - If the user reports potentially urgent symptoms, advise appropriate urgent medical attention.

    OUTPUT RULES:
    You MUST return one valid JSON object.
    Do not include markdown code fences.
    Do not include explanations outside the JSON object.
    Use double quotes for all JSON keys and string values.
    Do not include trailing commas.

    The JSON must follow this exact structure:

    {
        "status": "success",
        "message": "Your workout plan is ready.",
        "workout_plan": "Your workout plan in Markdown format."
    }

    Allowed status values:
    - success
    - invalid_input
    - clarification
    - medical_review

    For any status other than success, workout_plan must be an empty string.

    Return ONLY valid JSON.
    """

    # --------------------------------
    # 4. Prepare user prompt
    # --------------------------------

    user_prompt = f"""
    Generate a personalized workout plan using the following details.

    FITNESS GOAL:
    {fitness_goal}

    EXPERIENCE LEVEL:
    {experience_level}

    WORKOUT DAYS PER WEEK:
    {days_per_week}

    AVAILABLE EQUIPMENT:
    {equipment}

    INJURIES OR PHYSICAL LIMITATIONS:
    {injuries.strip() if injuries and injuries.strip() else "None specified"}

    First validate the limitations according to your safety rules.

    If valid for planning, generate the workout schedule.

    The schedule must contain exactly {days_per_week} workout days.

    Include the following sections:

    1. User Profile
    2. Weekly Workout Schedule
    3. Daily Exercises with Sets and Repetitions
    4. Rest Intervals
    5. Warm-up and Cool-down
    6. Progression Recommendations
    7. Recovery and Safety Tips

    Return only valid JSON.
    """

    # --------------------------------
    # 5. Call Groq API
    # --------------------------------

    try:

        client = Groq(api_key=GROQ_API_KEY)

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "workout_plan",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": [
                                    "success",
                                    "invalid_input",
                                    "clarification",
                                    "medical_review"
                                ]
                            },
                            "message": {
                                "type": "string"
                            },
                            "workout_plan": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "status",
                            "message",
                            "workout_plan"
                        ],
                        "additionalProperties": False
                    }
                }
            },
            reasoning_effort="medium",
            temperature=0.3,
            max_completion_tokens=3500
        )

        # --------------------------------
        # 6. Extract AI response
        # --------------------------------

        raw_response = response.choices[0].message.content

        if not raw_response:
            return {
                "status": "error",
                "message": "The AI returned an empty response. Please try again.",
                "workout_plan": ""
            }

        result = json.loads(raw_response)

        # --------------------------------
        # 7. Validate AI response
        # --------------------------------

        allowed_statuses = [
            "success",
            "invalid_input",
            "clarification",
            "medical_review"
        ]

        status = result.get("status")
        message = result.get("message", "")
        workout_plan = result.get("workout_plan", "")

        if status not in allowed_statuses:
            raise ValueError("Invalid AI response status.")

        if not isinstance(message, str):
            raise ValueError("Invalid AI response message.")

        if not isinstance(workout_plan, str):
            raise ValueError("Invalid workout plan format.")

        if status == "success" and not workout_plan.strip():
            raise ValueError("Workout plan is empty.")

        if status != "success":
            workout_plan = ""

        return {
            "status": status,
            "message": message,
            "workout_plan": workout_plan
        }

    # --------------------------------
    # 8. Error handling
    # --------------------------------

    except RateLimitError:

        return {
            "status": "error",
            "message": "Groq API rate limit reached. Please wait and try again.",
            "workout_plan": ""
        }

    except APIStatusError as error:
         print("Groq status:", error.status_code)
         print("Groq error details:", error.response.text)
         
         return {
              "status": "error",
              "message": f"Groq API error ({error.status_code}): {error.response.text}",
              "workout_plan": ""
            }

    except APIConnectionError:

        return {
            "status": "error",
            "message": "Unable to connect to Groq. Check your internet connection.",
            "workout_plan": ""
        }

    except json.JSONDecodeError:

        return {
            "status": "error",
            "message": "Unable to process the AI response. Please try again.",
            "workout_plan": ""
        }

    except Exception:

        return {
            "status": "error",
            "message": "Something went wrong. Please try again.",
            "workout_plan": ""
        }
