
import streamlit as st
from utils.workoutGenerator import generate_workout_plan


st.set_page_config(
    page_title="Workout Plan Generator",
    layout="centered"
)


st.title("Workout Plan Generator")
st.write("Create your personalized workout plan with the help of AI.")
st.divider()

# Fitness Goal
fitnessGoal = st.selectbox(
    "Fitness Goal",
    (
        "Build muscle","Lose fat","General fitness","Improve endurance"
    ),
    index=None,
    placeholder="Select your fitness goal..."
)


# Experience level
experienceLevel = st.selectbox(
    "Experience Level",
    (
        "Beginner", "Intermediate", "Advanced"
    ),
    index=None,
    placeholder="Select your experience level..."
)

# Workout days
daysPerWeek = st.slider(
    "How many days can you work out per week?",
    min_value=1,
    max_value=7,
    value=3
)

# Equipment access
equipment = st.selectbox(
    "Equipment Access",
    (
        "No equipment", "Home dumbbells", "Full gym"
    ),
    index=None,
    placeholder="Select your available equipment..."
)

# Injuries and limitations
injuries = st.text_area(
    "Injuries or Physical Limitations (Optional)",
    placeholder=("Example: Bad knees, back pain, no overhead pressing..."),
    help=("Mention injuries, medical conditions, or exercises you need to avoid.")
)

st.divider()


# Generate workout plan
if st.button(
    "Generate Plan",
    type="primary",
    use_container_width=True
):

    # Validate required fields
    if not fitnessGoal:
        st.warning("Please select your fitness goal.")

    elif not experienceLevel:
        st.warning("Please select your experience level.")

    elif not equipment:
        st.warning("Please select your available equipment.")

    elif not 1 <= daysPerWeek <= 7:
        st.warning("Please select between 1 and 7 workout days.")

    else:
        # Call Groq API
        with st.spinner(
            "AI is analyzing your fitness information..."
        ):

            result = generate_workout_plan(
                fitness_goal=fitnessGoal,
                experience_level=experienceLevel,
                days_per_week=daysPerWeek,
                equipment=equipment,
                injuries=injuries
            )

        # Display results based on status
        status = result["status"]
        message = result["message"]

        if status == "success":
            st.success("Your workout plan is ready!")
            st.divider()
            st.subheader("🏋️ Your Personalized Workout Plan")
            st.markdown(result["workout_plan"])

            # Download workout plan
            st.download_button(
                label="Download Workout Plan",
                data=result["workout_plan"],
                file_name="my_workout_plan.md",
                mime="text/markdown",
                use_container_width=True
            )
            st.divider()

            st.caption(
                "Disclaimer: This is general fitness guidance, "
                "not medical advice. Consult a qualified healthcare "
                "professional if you have injuries or medical concerns."
            )

        elif status == "invalid_input":
            st.warning(message)

        elif status == "clarification":
            st.info(message)

        elif status == "medical_review":
            st.error(message)

        else:
            st.error(message)
