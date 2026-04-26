"""
FitByte — Personalized AI Fitness Coach
========================================
Tech Stack : Groq API (LLaMA 3.3 70B) | Gradio | Hugging Face Spaces
Concepts   : System Prompt Engineering, Prompt Chaining, Dynamic Prompts,
             BMI Calculation, Input Validation, Secure API Key Handling
"""

import os
import gradio as gr
from groq import Groq

# ─────────────────────────────────────────────
# API SETUP  (Colab → HF Spaces compatible)
# ─────────────────────────────────────────────
def get_api_key() -> str:
    try:
        from google.colab import userdata
        return userdata.get("GROQ_API_KEY")
    except Exception:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            raise EnvironmentError("GROQ_API_KEY not found in environment.")
        return key

try:
    client = Groq(api_key=get_api_key())
    API_READY = True
except Exception as e:
    API_READY = False
    API_ERROR = str(e)


# ─────────────────────────────────────────────
# BMI CALCULATION
# ─────────────────────────────────────────────
def calculate_bmi(weight_kg: float, height_cm: float) -> tuple:
    if height_cm <= 0 or weight_kg <= 0:
        raise ValueError("Weight and height must be positive numbers.")
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal weight"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obese"
    return bmi, category


# ─────────────────────────────────────────────
# PROMPT ENGINEERING
# ─────────────────────────────────────────────
COACHING_MODES = {
    "Motivational Coach 🔥": (
        "You are an energetic, motivational fitness coach. "
        "Use powerful, encouraging language. Include motivational quotes. "
        "Make the user feel unstoppable. Use emojis sparingly but effectively."
    ),
    "Scientific Advisor 🔬": (
        "You are a sports scientist and certified nutritionist. "
        "Use precise, evidence-based language. Cite physiological principles "
        "(e.g., progressive overload, TDEE, macronutrient ratios). "
        "Be clinical but clear. No fluff."
    ),
    "Friendly Buddy 😊": (
        "You are the user's supportive gym buddy. "
        "Keep the tone casual, warm, and relatable. "
        "Use simple language. Make fitness feel approachable and fun."
    ),
    "Strict Drill Sergeant 💪": (
        "You are a no-nonsense military fitness trainer. "
        "Be direct, demanding, and results-focused. "
        "No excuses. Short, punchy sentences. Push the user hard."
    ),
}

def build_system_prompt(mode: str) -> str:
    base = COACHING_MODES.get(mode, COACHING_MODES["Motivational Coach 🔥"])
    return (
        f"{base}\n\n"
        "Always structure your response with these clearly labeled sections:\n"
        "1. **BMI Analysis** — Interpret their BMI and what it means for them.\n"
        "2. **Weekly Workout Plan** — Plan with specific exercises, sets, reps.\n"
        "3. **Daily Meal Plan** — Breakfast, Lunch, Dinner, Snacks with approximate calories.\n"
        "4. **Key Tips** — 3 personalized tips based on their goal and fitness level.\n"
        "5. **Motivational Closing** — End with an inspiring one-liner.\n\n"
        "Use markdown formatting with bold headers. Be specific, not generic.\n\n"
        "IMPORTANT: Build the meal plan strictly around the user's available foods and cuisine. "
        "Do NOT suggest foods they cannot access or afford. Use locally available, budget-friendly alternatives."
    )

def build_user_prompt(
    name, age, gender, body_condition,
    weight, height, bmi, bmi_cat,
    goal, fitness_level, dietary_pref,
    cuisine_pref, food_context,
    workout_days, workout_duration,
    health_conditions
) -> str:
    conditions_str = health_conditions.strip() if health_conditions else "None reported"
    food_str = food_context.strip() if food_context else "No specific constraints"
    return (
        f"Create a fully personalized fitness plan for the following individual:\n\n"
        f"**Personal Details:**\n"
        f"- Name: {name}\n"
        f"- Age: {age} years | Gender: {gender}\n"
        f"- Weight: {weight} kg | Height: {height} cm\n"
        f"- BMI: {bmi} ({bmi_cat}) | Body Condition: {body_condition}\n\n"
        f"**Goals & Preferences:**\n"
        f"- Primary Goal: {goal}\n"
        f"- Current Fitness Level: {fitness_level}\n"
        f"- Dietary Type: {dietary_pref}\n"
        f"- Cuisine / Food Region: {cuisine_pref}\n"
        f"- Food Availability & Budget: {food_str}\n"
        f"- Workout Days per Week: {workout_days}\n"
        f"- Workout Duration per Day: {workout_duration} minutes\n"
        f"- Health Conditions / Injuries: {conditions_str}\n\n"
        f"Generate a realistic, safe, and highly personalized plan. "
        f"Account for their BMI category, body condition, and health conditions "
        f"when recommending exercises and diet."
    )


# ─────────────────────────────────────────────
# GROQ API CALL
# ─────────────────────────────────────────────
def call_groq(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=2048
    )
    return response.choices[0].message.content


# ─────────────────────────────────────────────
# MAIN ORCHESTRATION
# ─────────────────────────────────────────────
def generate_fitness_plan(
    name, age, gender, body_condition,
    weight, height,
    goal, fitness_level, dietary_pref,
    cuisine_pref, food_context,
    workout_days, workout_duration,
    health_conditions, coaching_mode
):
    if not name.strip():
        return "❌ Error", "Please enter your name.", ""
    if not (10 <= int(age) <= 100):
        return "❌ Error", "Age must be between 10 and 100.", ""
    if weight <= 0 or height <= 0:
        return "❌ Error", "Weight and height must be positive values.", ""
    if not API_READY:
        return "❌ API Error", f"Groq API not configured: {API_ERROR}", ""

    try:
        bmi, bmi_cat = calculate_bmi(weight, height)
        bmi_display = f"**BMI: {bmi}** — {bmi_cat}"

        system_prompt = build_system_prompt(coaching_mode)
        user_prompt = build_user_prompt(
            name, age, gender, body_condition,
            weight, height, bmi, bmi_cat,
            goal, fitness_level, dietary_pref,
            cuisine_pref, food_context,
            int(workout_days), int(workout_duration),
            health_conditions
        )

        plan = call_groq(system_prompt, user_prompt)

        download_text = (
            f"FITBYTE — PERSONALIZED FITNESS PLAN\n"
            f"Name: {name}\n"
            f"{'='*50}\n\n"
            f"BMI: {bmi} ({bmi_cat})\n"
            f"Goal: {goal} | Level: {fitness_level} | Mode: {coaching_mode}\n"
            f"{'='*50}\n\n"
            + plan
        )

        return bmi_display, plan, download_text

    except ValueError as ve:
        return "❌ Input Error", str(ve), ""
    except Exception as e:
        return "❌ Error", f"Something went wrong: {str(e)}", ""


def save_plan(download_text: str):
    if not download_text:
        return None
    filepath = "/tmp/fitbyte_plan.txt"
    with open(filepath, "w") as f:
        f.write(download_text)
    return filepath


# ─────────────────────────────────────────────
# GRADIO UI
# ─────────────────────────────────────────────
CSS = """
footer { display: none !important; }
"""

with gr.Blocks(theme=gr.themes.Soft(primary_hue="emerald"), css=CSS, title="FitByte") as demo:

    gr.Markdown("""
    # 🏋️ FitByte — Personalized AI Fitness Coach
    > **Powered by Groq (LLaMA 3.3 70B)** | Built with Gradio | Deployed on Hugging Face Spaces
    """)

    with gr.Row():

        with gr.Column(scale=1):
            gr.Markdown("### 👤 Personal Info")
            name = gr.Textbox(label="Full Name", placeholder="e.g. Rohit Sharma")
            age = gr.Number(label="Age", value=21, minimum=10, maximum=100)
            gender = gr.Radio(["Male", "Female", "Other"], label="Gender", value="Male")
            body_condition = gr.Dropdown(
                ["Not Sure", "Skinny", "Skinny-Fat", "Average", "Overweight/Fat", "Muscular"],
                label="Current Body Condition", value="Average"
            )

            gr.Markdown("### 📏 Body Metrics")
            weight = gr.Number(label="Weight (kg)", value=70)
            height = gr.Number(label="Height (cm)", value=175)

            gr.Markdown("### 🎯 Fitness Profile")
            goal = gr.Dropdown(
                ["Weight Loss", "Muscle Gain", "Maintain Weight", "Improve Stamina", "Flexibility & Mobility"],
                label="Primary Goal", value="Muscle Gain"
            )
            fitness_level = gr.Dropdown(
                ["Beginner (0–6 months)", "Intermediate (6 months–2 years)", "Advanced (2+ years)"],
                label="Fitness Level", value="Beginner (0–6 months)"
            )
            dietary_pref = gr.Dropdown(
                ["No Preference", "Vegetarian", "Eggetarian", "Vegan", "Non-Vegetarian", "Keto", "High Protein"],
                label="Dietary Preference", value="No Preference"
            )
            workout_days = gr.Slider(minimum=2, maximum=7, step=1, value=4, label="Workout Days per Week")
            workout_duration = gr.Slider(minimum=20, maximum=120, step=10, value=45, label="Workout Duration per Day (minutes)")

            gr.Markdown("### 🍽️ Food & Cuisine")
            cuisine_pref = gr.Dropdown(
                ["No Preference", "Indian", "South Indian", "Middle Eastern", "East Asian", "Mediterranean", "Western"],
                label="Cuisine / Region", value="No Preference"
            )
            food_context = gr.Textbox(
                label="Food Availability & Budget (optional)",
                placeholder="e.g. I eat chapati, dal, sabzi daily. No bread or pasta. Tight budget.",
                lines=2
            )

            gr.Markdown("### ⚕️ Health")
            health_conditions = gr.Textbox(
                label="Health Conditions / Injuries (optional)",
                placeholder="e.g. Lower back pain, knee injury..."
            )

            gr.Markdown("### 🤖 Coaching Style")
            coaching_mode = gr.Radio(
                list(COACHING_MODES.keys()),
                label="Select Your Coach",
                value="Motivational Coach 🔥"
            )

            generate_btn = gr.Button("⚡ Generate My Plan", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.Markdown("### 📊 Your BMI")
            bmi_output = gr.Markdown(value="_Your BMI will appear here._")

            gr.Markdown("### 📋 Your Personalized Plan")
            plan_output = gr.Markdown(value="_Fill in your details and hit Generate._", height=600)

            with gr.Row():
                download_state = gr.State("")
                download_btn = gr.Button("💾 Download My Plan", variant="secondary")
                download_file = gr.File(label="Your Plan (TXT)", visible=False)

    gr.Markdown("""
    ---
    **📌 Disclaimer:** AI-generated for educational purposes. Consult a certified trainer and nutritionist before starting any fitness program.
    """)

    generate_btn.click(
        fn=generate_fitness_plan,
        inputs=[
            name, age, gender, body_condition,
            weight, height,
            goal, fitness_level, dietary_pref,
            cuisine_pref, food_context,
            workout_days, workout_duration,
            health_conditions, coaching_mode
        ],
        outputs=[bmi_output, plan_output, download_state]
    )

    download_btn.click(
        fn=save_plan,
        inputs=[download_state],
        outputs=[download_file]
    ).then(
        fn=lambda: gr.File(visible=True),
        outputs=[download_file]
    )


if __name__ == "__main__":
    demo.launch()
