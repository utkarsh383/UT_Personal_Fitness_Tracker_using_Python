import streamlit as st
import pandas as pd
import datetime
import random
from user_auth import register_user, check_user
import pickle
import numpy as np
import base64


def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


# Load the trained model
with open("fitness_model.pkl", "rb") as f:
    model, scaler, label_encoders = pickle.load(f)

# Custom CSS
st.markdown(
    """
    <style>
        .card {
            background-color: #ffffff; /* White background */
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 16px;
            margin: 10px;
            text-align: center;
            box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
        }
        .card h3 {
            color: #333333; /* Dark text for visibility */
        }
        .card p {
            color: #555555; /* Slightly lighter text */
        }
        .exercise-icon, .yoga-icon {
            width: 80px;
            height: 80px;
            object-fit: cover;
            border-radius: 50%;
            margin-bottom: 10px;
            display: block;
            margin-left: auto;
            margin-right: auto;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("Go to", ["🏠 Home", "📋 Register", "🧘 Yoga Tips"])

# Exercise Database for Personalized Plans 
EXERCISES = {
    "Beginner": [
        {"icon": "jumping-jacks.png", "name": "Jumping Jacks", "duration": "5 minutes",
         "description": "Boosts heart rate and warms up your body.", "kcal": 50},
        {"icon": "bodyweight-squats.png", "name": "Bodyweight Squats", "duration": "10 minutes",
         "description": "Strengthens your legs and glutes.", "kcal": 40},
        {"icon": "plank.png", "name": "Plank", "duration": "5 minutes",
         "description": "Improves core stability.", "kcal": 20},
        {"icon": "brisk-walking.png", "name": "Brisk Walking", "duration": "10 minutes",
         "description": "Great for beginners and cardio.", "kcal": 60},
        {"icon": "dumbbell-press.png", "name": "Light Dumbbell Press", "duration": "8 minutes",
         "description": "Improves upper body strength.", "kcal": 30},
        {"icon": "step-ups.png", "name": "Step-Ups", "duration": "7 minutes",
         "description": "Enhances leg strength and balance.", "kcal": 35}
    ],
    "Intermediate": [
        {"icon": "push-ups.png", "name": "Push-ups", "duration": "10 minutes",
         "description": "Builds upper body strength.", "kcal": 60},
        {"icon": "running-in-place.png", "name": "Running in Place", "duration": "8 minutes",
         "description": "Improves endurance.", "kcal": 70},
        {"icon": "cycling.png", "name": "Cycling", "duration": "15 minutes",
         "description": "Great for cardio and leg strength.", "kcal": 100},
        {"icon": "dumbbell-rows.png", "name": "Dumbbell Rows", "duration": "10 minutes",
         "description": "Strengthens back muscles.", "kcal": 50},
        {"icon": "medicine-ball-slams.png", "name": "Medicine Ball Slams", "duration": "7 minutes",
         "description": "Boosts explosive power.", "kcal": 55},
        {"icon": "high-knees.png", "name": "High Knees", "duration": "5 minutes",
         "description": "Elevates heart rate quickly.", "kcal": 45}
    ],
    "Advanced": [
        {"icon": "deadlifts.png", "name": "Deadlifts", "duration": "15 minutes",
         "description": "Full-body strength training.", "kcal": 120},
        {"icon": "sprints.png", "name": "Sprints", "duration": "10 minutes",
         "description": "High-intensity cardio workout.", "kcal": 80},
        {"icon": "lunges.png", "name": "Lunges", "duration": "10 minutes",
         "description": "Strengthens lower body muscles.", "kcal": 70},
        {"icon": "burpees.png", "name": "Burpees", "duration": "8 minutes",
         "description": "Intense full-body exercise.", "kcal": 65},
        {"icon": "mountain-climbers.png", "name": "Mountain Climbers", "duration": "7 minutes",
         "description": "Improves agility and core strength.", "kcal": 60},
        {"icon": "kettlebell-swings.png", "name": "Kettlebell Swings", "duration": "10 minutes",
         "description": "Boosts endurance and power.", "kcal": 75}
    ]
}

#  Home Page 
if page == "🏠 Home":
    st.title("🏋️ Personal Fitness Tracker")
    st.write("Welcome! Please log in or register to calculate your BMI, view your fitness summary, and generate a personalized exercise plan.")

    # Simple Login System in Home Page
    if "logged_in_user" not in st.session_state:
        st.subheader("Login")
        login_name = st.text_input("Enter your name to log in:")
        if st.button("Login"):
            user = check_user(login_name)
            if user:
                st.session_state.logged_in_user = user
                st.success(f"Welcome back, {login_name}!")
            else:
                st.error("User not found. Please register first.")
    else:
        user = st.session_state.logged_in_user
        st.success(f"Welcome back, {user[1]}!")  


    st.header("Your Personal Details")
    col1, col2 = st.columns(2)
    with col1:
        if "logged_in_user" in st.session_state:
            name = user[1]
            age = user[2]  
            gender = user[5]  
            st.text_input("Name", value=name, key="name_filled")
            st.number_input("Age", min_value=1, max_value=100, value=age, key="age_filled")
            st.selectbox("Gender", ["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(gender), key="gender_filled")
        else:
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=1, max_value=100, step=1)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with col2:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, step=0.1)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)

    # BMI Calculation
    bmi = None
    if weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2)
    if st.button("💪 Calculate BMI"):
        if name and bmi:
            st.success(f"Hello {name}, your BMI is **{bmi:.2f}**")
        else:
            st.error("Please fill in all the required details.")

    # Activity and Motivation Section
    st.header("Activity Level & Motivation")
    activity_option = st.radio("Select your activity level:",
                               ("Fully Active", "Moderately Active", "Not Active", "Manual Input"))
    exercise_duration = None
    if activity_option == "Manual Input":
        exercise_duration = st.number_input("Enter exercise duration (minutes)", min_value=0, step=1)
    motivation = st.text_input("What motivates you to exercise?")

    # summary table with all details
    st.header("Your Fitness Summary")
    data = {
        "Name": [name],
        "Age": [age],
        "Gender": [gender],
        "Weight (kg)": [weight],
        "Height (cm)": [height],
        "BMI": [f"{bmi:.2f}" if bmi else ""],
        "Activity Level": [activity_option],
        "Motivation": [motivation]
    }
    df = pd.DataFrame(data)
    st.table(df)

    # fitness-level comment based on BMI
    if bmi:
        if bmi < 18.5:
            comment = "Underweight: Consider a balanced diet."
        elif bmi < 24.9:
            comment = "Healthy weight: Great job!"
        elif bmi < 29.9:
            comment = "Overweight: Time to get more active!"
        else:
            comment = "Obese: Please consult a healthcare provider."
        st.write("**Fitness Level Comment:**", comment)

    # Personalized Exercise Plan Section
    st.header("Create Your Personalized Exercise Plan")
    workout_days = st.number_input("How many days per week can you workout?", min_value=1, max_value=7, step=1)
    if st.button("Generate Exercise Plan"):
        st.subheader("Your Exercise Plan:")

        if bmi is None:
            st.error("Please calculate your BMI first!")
        else:
           
            gender_encoded = label_encoders["Gender"].transform([gender])[0]
            activity_encoded = label_encoders["Activity_Level"].transform([activity_option])[0]

            user_data = np.array([[age, weight, height, activity_encoded]])
            user_data_scaled = scaler.transform(user_data)

            # Predict exercise type using the model
            predicted_category = model.predict(user_data_scaled)[0]
            predicted_exercise = label_encoders["Exercise_Type"].inverse_transform([predicted_category])[0]

            # Map the predicted exercise to a difficulty level
            mapping = {
                "Jumping Jacks": "Beginner",
                "Bodyweight Squats": "Beginner",
                "Plank": "Beginner",
                "Brisk Walking": "Beginner",
                "Light Dumbbell Press": "Beginner",
                "Step-Ups": "Beginner",
                "Push-ups": "Intermediate",
                "Running in Place": "Intermediate",
                "Cycling": "Intermediate",
                "Dumbbell Rows": "Intermediate",
                "Medicine Ball Slams": "Intermediate",
                "High Knees": "Intermediate",
                "Deadlifts": "Advanced",
                "Sprints": "Advanced",
                "Lunges": "Advanced",
                "Burpees": "Advanced",
                "Mountain Climbers": "Advanced",
                "Kettlebell Swings": "Advanced"
            }
            level = mapping.get(predicted_exercise, "Beginner")
            st.write(f"Based on your BMI, we've selected a **{level}** plan for you.")
            
            available = EXERCISES[level]
            random.shuffle(available)

            # Display each exercise
            for exercise in available:
                html = f"""
                <div class="card" style="text-align: center;">
                    <img src="data:image/png;base64,{get_base64_image('images/' + exercise['icon'])}" alt="{exercise['name']}" class="exercise-icon">
                    <h3>{exercise['name']}</h3>
                    <p><strong>Duration:</strong> {exercise['duration']}</p>
                    <p>{exercise['description']}</p>
                    <p><strong>Calories Burned:</strong> {exercise['kcal']} kcal</p>
                </div>
                """
                st.markdown(html, unsafe_allow_html=True)

# Registration Page
elif page == "📋 Register":
    st.title("📝 User Registration")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=10, max_value=100, step=1)
    height = st.number_input("Height (in cm)")
    weight = st.number_input("Weight (in kg)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

    if st.button("Register"):
        if name and age and height and weight and gender:
            if check_user(name):
                st.warning("⚠️ User already exists! Try a different name.")
            else:
                register_user(name, age, height, weight, gender)
                st.success(f"✅ Registration Successful for {name}!")
        else:
            st.error("⚠️ Please fill in all fields.")

#  Yoga Tips Page 
elif page == "🧘 Yoga Tips":
    st.title("🧘 Yoga Tips and Poses")
    st.write("Explore these yoga poses to relax, improve flexibility, and boost your overall wellness.")

    # Define a list of yoga pose cards with images
    yoga_poses = [
        {"image": "mountain-pose.png", "name": "Mountain Pose (Tadasana)",
         "instructions": "Stand tall with feet together, arms at your side.",
         "benefits": "Improves posture and balance."},
        {"image": "downward-dog.png", "name": "Downward Dog (Adho Mukha Svanasana)",
         "instructions": "Start on all fours, lift hips to form an inverted V.",
         "benefits": "Stretches the back and legs."},
        {"image": "warrior-ii.png", "name": "Warrior II (Virabhadrasana II)",
         "instructions": "Stand with feet wide, turn one foot out, bend that knee.",
         "benefits": "Strengthens legs and opens hips."},
        {"image": "tree-pose.png", "name": "Tree Pose (Vrikshasana)",
         "instructions": "Balance on one leg; place the other foot on your inner thigh.",
         "benefits": "Enhances balance and concentration."},
        {"image": "childs-pose.png", "name": "Child's Pose (Balasana)",
         "instructions": "Kneel and lower your torso forward with arms extended.",
         "benefits": "Relieves stress and tension."},
        {"image": "cobra-pose.png", "name": "Cobra Pose (Bhujangasana)",
         "instructions": "Lie on your stomach and lift your chest using your arms.",
         "benefits": "Strengthens the spine and opens the chest."},
        {"image": "bridge-pose.png", "name": "Bridge Pose (Setu Bandhasana)",
         "instructions": "Lie on your back, bend your knees, and lift your hips.",
         "benefits": "Stretches the chest, neck, and spine."},
        {"image": "seated-forward-bend.png", "name": "Seated Forward Bend (Paschimottanasana)",
         "instructions": "Sit with legs extended and lean forward gently.",
         "benefits": "Calms the mind and stretches the back."},
        {"image": "corpse-pose.png", "name": "Corpse Pose (Savasana)",
         "instructions": "Lie on your back with arms relaxed at your sides.",
         "benefits": "Promotes deep relaxation and stress relief."},
        {"image": "cat-cow.png", "name": "Cat-Cow Pose (Marjaryasana-Bitilasana)",
         "instructions": "Alternate arching and rounding your back on all fours.",
         "benefits": "Improves flexibility and relieves tension."}
    ]

    # Display yoga poses
        for pose in yoga_poses:
        html = f"""
        <div class="card" style="text-align: center;">
            <img src="data:image/png;base64,{get_base64_image('images/' + pose['image'])}" alt="{pose['name']}" class="yoga-icon" style="width: 240px; height: 240px;">
            <h3>{pose['name']}</h3>
            <p><strong>How to do it:</strong> {pose['instructions']}</p>
            <p><strong>Benefits:</strong> {pose['benefits']}</p>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
