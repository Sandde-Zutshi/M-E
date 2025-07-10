import streamlit as st
import psycopg2
import os
import json
from datetime import datetime
from psycopg2 import sql

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname="nutrition_db",
    user="sandeep",      # your Mac login username
    password="",         # leave empty if no password set
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Initialize session state for multi-step flow
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}

# Function to go to next step
def next_step():
    st.session_state.step += 1

# Function to go back a step
def prev_step():
    if st.session_state.step > 1:
        st.session_state.step -= 1

# Function to save uploaded file
def save_uploaded_file(uploaded_file, file_type):
    if uploaded_file is not None:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = uploaded_file.name.split('.')[-1]
        filename = f"{file_type}_{timestamp}.{file_extension}"
        
        # Save file
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return filename
    return None

# Function to save data to JSON
def save_data_to_file(data):
    os.makedirs("data", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nutrition_data_{timestamp}.json"
    filepath = os.path.join("data", filename)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)
    
    return filename

st.markdown('<h1 style="color: blue; font-size: 80%;">🧒 Child Nutrition Data Collection (MVP Demo)</h1>', unsafe_allow_html=True)

# Progress indicator
progress_value = (st.session_state.step - 1) / 5
st.progress(progress_value)
st.write(f"Step {st.session_state.step} of 6")

step = st.session_state.step

if step == 1:
    st.header("👤 Staff & Household Info")
    
    staff_id = st.text_input("Enter Field Staff ID", value=st.session_state.data.get('staff_id', ''))
    household_id = st.text_input("Enter Household ID", value=st.session_state.data.get('household_id', ''))
    language = st.selectbox("Select Language", ["English", "Hindi", "Telugu"], 
                           index=["English", "Hindi", "Telugu"].index(st.session_state.data.get('language', 'English')))

    # Validation
    can_proceed = staff_id.strip() != "" and household_id.strip() != ""
    
    if not can_proceed:
        st.warning("⚠️ Please fill in all required fields to continue.")

    if st.button("Next", disabled=not can_proceed):
        st.session_state.data['staff_id'] = staff_id
        st.session_state.data['household_id'] = household_id
        st.session_state.data['language'] = language
        st.session_state.data['timestamp'] = datetime.now().isoformat()
        next_step()
        st.rerun()

elif step == 2:
    st.header("🧒 Child Info")
    
    name = st.text_input("Child's Name", value=st.session_state.data.get('child_name', ''))
    age = st.number_input("Child's Age (in months)", min_value=0, max_value=120, 
                         value=st.session_state.data.get('child_age_months', 0))

    # Validation
    can_proceed = name.strip() != "" and age > 0
    
    if not can_proceed:
        st.warning("⚠️ Please provide valid child name and age to continue.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next", disabled=not can_proceed):
            st.session_state.data['child_name'] = name
            st.session_state.data['child_age_months'] = age
            next_step()
            st.rerun()

elif step == 3:
    st.header("📏 Measurements")
    
    height = st.number_input("Height (cm)", min_value=30.0, max_value=200.0, 
                            value=st.session_state.data.get('height_cm', 50.0))
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=100.0, 
                            value=st.session_state.data.get('weight_kg', 3.0))

    # Basic validation check - show warning but don't block progression
    if weight > 30 and st.session_state.data.get('child_age_months', 0) < 24:
        st.warning("⚠️ Unusual weight for a child under 2 years. Please double-check this measurement.")

    # Validation
    can_proceed = height > 0 and weight > 0
    
    if not can_proceed:
        st.warning("⚠️ Please provide valid measurements to continue.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next", disabled=not can_proceed):
            st.session_state.data['height_cm'] = height
            st.session_state.data['weight_kg'] = weight
            next_step()
            st.rerun()

elif step == 4:
    st.header("📸 Upload Child's Photo")
    st.write("Please upload a recent photo of the child for identification purposes.")
    
    photo = st.file_uploader("Upload a photo of the child", type=["jpg", "jpeg", "png"])

    # Show preview if photo is uploaded
    if photo is not None:
        st.image(photo, caption="Uploaded Photo", width=300)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Skip Photo"):
            st.session_state.data['photo'] = "skipped"
            next_step()
            st.rerun()
    with col3:
        if st.button("Next", disabled=photo is None):
            if photo is not None:
                filename = save_uploaded_file(photo, "photo")
                st.session_state.data['photo'] = filename
                next_step()
                st.rerun()

elif step == 5:
    st.header("🎙️ Mother's Audio Confirmation")
    st.write("Please record the mother's voice confirmation (e.g., 'Yes, this information is correct').")
    
    audio = st.file_uploader("Upload mother's voice confirmation", type=["mp3", "wav", "m4a"])

    # Show audio player if file is uploaded
    if audio is not None:
        st.audio(audio)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Skip Audio"):
            st.session_state.data['audio_confirmation'] = "skipped"
            next_step()
            st.rerun()
    with col3:
        if st.button("Next", disabled=audio is None):
            if audio is not None:
                filename = save_uploaded_file(audio, "audio")
                st.session_state.data['audio_confirmation'] = filename
                next_step()
                st.rerun()

elif step == 6:
    st.header("🧾 Review & Submit")
    st.write("Please review the collected information before submitting:")
    
    # Display data in a more organized way
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Staff & Household")
        st.write(f"**Staff ID**: {st.session_state.data.get('staff_id', 'N/A')}")
        st.write(f"**Household ID**: {st.session_state.data.get('household_id', 'N/A')}")
        st.write(f"**Language**: {st.session_state.data.get('language', 'N/A')}")
        
        st.subheader("Child Information")
        st.write(f"**Name**: {st.session_state.data.get('child_name', 'N/A')}")
        st.write(f"**Age**: {st.session_state.data.get('child_age_months', 'N/A')} months")
    
    with col2:
        st.subheader("Measurements")
        st.write(f"**Height**: {st.session_state.data.get('height_cm', 'N/A')} cm")
        st.write(f"**Weight**: {st.session_state.data.get('weight_kg', 'N/A')} kg")
        
        st.subheader("Files")
        st.write(f"**Photo**: {st.session_state.data.get('photo', 'Not uploaded')}")
        st.write(f"**Audio**: {st.session_state.data.get('audio_confirmation', 'Not uploaded')}")

    st.subheader("Timestamp")
    st.write(f"**Collected on**: {st.session_state.data.get('timestamp', 'N/A')}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Submit Data"):
            # Save data to file
            filename = save_data_to_file(st.session_state.data)
            st.success(f"✅ Data submitted successfully! Saved as {filename}")
            st.info("💡 You can now start a new data collection by clicking 'Start New Collection' below.")
            
            if st.button("Start New Collection"):
                st.session_state.step = 1
                st.session_state.data = {}
                st.rerun()

# Add sidebar with summary
with st.sidebar:
    st.header("📊 Collection Summary")
    st.write(f"Current Step: {step}/6")
    
    if st.session_state.data:
        st.subheader("Collected Data:")
        for key, value in st.session_state.data.items():
            if key not in ['timestamp']:
                display_key = key.replace('_', ' ').title()
                if isinstance(value, (int, float)):
                    st.write(f"• {display_key}: {value}")
                elif len(str(value)) > 20:
                    st.write(f"• {display_key}: {str(value)[:20]}...")
                else:
                    st.write(f"• {display_key}: {value}")
    
    st.markdown("---")
    st.write("**Instructions:**")
    st.write("1. Fill in staff and household info")
    st.write("2. Enter child details")
    st.write("3. Record measurements")
    st.write("4. Upload photo (optional)")
    st.write("5. Upload audio confirmation (optional)")
    st.write("6. Review and submit")
