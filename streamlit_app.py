import streamlit as st
import os
import json
from datetime import datetime

# Custom CSS for better styling
st.markdown("""
<style>
    .confirmation-box {
        background-color: #e8f5e8;
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .field-confirmed {
        background-color: #f0f8f0;
        border-left: 4px solid #4CAF50;
        padding: 10px;
        margin: 5px 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 2px solid #ffc107;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    .success-check {
        color: #4CAF50;
        font-size: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for multi-step flow
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'data' not in st.session_state:
    st.session_state.data = {}
if 'field_confirmations' not in st.session_state:
    st.session_state.field_confirmations = {}

# Function to show field confirmation
def show_field_confirmation(field_name, field_value, field_key):
    if field_key not in st.session_state.field_confirmations:
        st.session_state.field_confirmations[field_key] = False
    
    if field_value and str(field_value).strip():
        st.markdown(f"""
        <div class="confirmation-box">
            <strong>📝 Please confirm:</strong><br>
            <strong>{field_name}:</strong> {field_value}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"✅ Confirm {field_name.split()[-1]}", key=f"confirm_{field_key}"):
                st.session_state.field_confirmations[field_key] = True
                st.success(f"✅ {field_name} confirmed!")
                st.rerun()
        with col2:
            if st.button(f"✏️ Edit {field_name.split()[-1]}", key=f"edit_{field_key}"):
                st.session_state.field_confirmations[field_key] = False
                st.info(f"Please re-enter {field_name}")
                st.rerun()
        
        if st.session_state.field_confirmations[field_key]:
            st.markdown(f"""
            <div class="field-confirmed">
                <span class="success-check">✅</span> <strong>{field_name}:</strong> {field_value} <em>(Confirmed)</em>
            </div>
            """, unsafe_allow_html=True)
            return True
    return False

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

st.title("🧒 Child Nutrition Data Collection (Enhanced MVP Demo)")
st.markdown("---")

# Progress indicator
progress_value = (st.session_state.step - 1) / 5
st.progress(progress_value)
st.write(f"Step {st.session_state.step} of 6")

step = st.session_state.step

if step == 1:
    st.header("👤 Staff & Household Info")
    
    staff_id = st.text_input("Enter Field Staff ID", value=st.session_state.data.get('staff_id', ''))
    staff_confirmed = False
    if staff_id.strip():
        staff_confirmed = show_field_confirmation("Staff ID", staff_id, "staff_id")
    
    household_id = st.text_input("Enter Household ID", value=st.session_state.data.get('household_id', ''))
    household_confirmed = False
    if household_id.strip():
        household_confirmed = show_field_confirmation("Household ID", household_id, "household_id")
    
    language = st.selectbox("Select Language", ["English", "Hindi", "Telugu"], 
                           index=["English", "Hindi", "Telugu"].index(st.session_state.data.get('language', 'English')))
    language_confirmed = False
    if language:
        language_confirmed = show_field_confirmation("Language", language, "language")

    # Validation - all fields must be confirmed
    can_proceed = staff_confirmed and household_confirmed and language_confirmed
    
    if not can_proceed:
        if not staff_id.strip() or not household_id.strip():
            st.warning("⚠️ Please fill in all required fields.")
        else:
            st.warning("⚠️ Please confirm all entered information to continue.")

    st.markdown("---")
    if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
        st.session_state.data['staff_id'] = staff_id
        st.session_state.data['household_id'] = household_id
        st.session_state.data['language'] = language
        st.session_state.data['timestamp'] = datetime.now().isoformat()
        next_step()
        st.rerun()

elif step == 2:
    st.header("🧒 Child Info")
    
    name = st.text_input("Child's Name", value=st.session_state.data.get('child_name', ''))
    name_confirmed = False
    if name.strip():
        name_confirmed = show_field_confirmation("Child's Name", name, "child_name")
    
    age = st.number_input("Child's Age (in months)", min_value=0, max_value=120, 
                         value=st.session_state.data.get('child_age_months', 0))
    age_confirmed = False
    if age > 0:
        age_confirmed = show_field_confirmation("Child's Age", f"{age} months", "child_age")

    # Validation - all fields must be confirmed
    can_proceed = name_confirmed and age_confirmed
    
    if not can_proceed:
        if not name.strip() or age <= 0:
            st.warning("⚠️ Please provide valid child name and age.")
        else:
            st.warning("⚠️ Please confirm all entered information to continue.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
            st.session_state.data['child_name'] = name
            st.session_state.data['child_age_months'] = age
            next_step()
            st.rerun()

elif step == 3:
    st.header("📏 Measurements")
    
    height = st.number_input("Height (cm)", min_value=30.0, max_value=200.0, 
                            value=st.session_state.data.get('height_cm', 50.0))
    height_confirmed = False
    if height > 0:
        height_confirmed = show_field_confirmation("Height", f"{height} cm", "height")
    
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=100.0, 
                            value=st.session_state.data.get('weight_kg', 3.0))
    weight_confirmed = False
    if weight > 0:
        weight_confirmed = show_field_confirmation("Weight", f"{weight} kg", "weight")

    # Basic validation check - show warning but don't block progression
    if weight > 30 and st.session_state.data.get('child_age_months', 0) < 24:
        st.markdown("""
        <div class="warning-box">
            <strong>⚠️ Important:</strong> Unusual weight for a child under 2 years. Please double-check this measurement.
        </div>
        """, unsafe_allow_html=True)

    # Validation - all fields must be confirmed
    can_proceed = height_confirmed and weight_confirmed
    
    if not can_proceed:
        if height <= 0 or weight <= 0:
            st.warning("⚠️ Please provide valid measurements.")
        else:
            st.warning("⚠️ Please confirm all entered measurements to continue.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
            st.session_state.data['height_cm'] = height
            st.session_state.data['weight_kg'] = weight
            next_step()
            st.rerun()

elif step == 4:
    st.header("📸 Upload Child's Photo")
    st.write("Please upload a recent photo of the child for identification purposes.")
    
    photo = st.file_uploader("Upload a photo of the child", type=["jpg", "jpeg", "png"])
    photo_confirmed = False

    # Show preview if photo is uploaded
    if photo is not None:
        st.image(photo, caption="Uploaded Photo", width=300)
        photo_confirmed = show_field_confirmation("Child's Photo", f"File: {photo.name}", "photo")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("⏭️ Skip Photo", use_container_width=True):
            st.session_state.data['photo'] = "skipped"
            next_step()
            st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=not photo_confirmed, use_container_width=True):
            if photo is not None:
                filename = save_uploaded_file(photo, "photo")
                st.session_state.data['photo'] = filename
                next_step()
                st.rerun()

elif step == 5:
    st.header("🎙️ Mother's Audio Confirmation")
    st.write("Please record the mother's voice confirmation (e.g., 'Yes, this information is correct').")
    
    audio = st.file_uploader("Upload mother's voice confirmation", type=["mp3", "wav", "m4a"])
    audio_confirmed = False

    # Show audio player if file is uploaded
    if audio is not None:
        st.audio(audio)
        audio_confirmed = show_field_confirmation("Audio Confirmation", f"File: {audio.name}", "audio")

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⬅️ Back", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("⏭️ Skip Audio", use_container_width=True):
            st.session_state.data['audio_confirmation'] = "skipped"
            next_step()
            st.rerun()
    with col3:
        if st.button("Next ➡️", disabled=not audio_confirmed, use_container_width=True):
            if audio is not None:
                filename = save_uploaded_file(audio, "audio")
                st.session_state.data['audio_confirmation'] = filename
                next_step()
                st.rerun()

elif step == 6:
    st.header("🧾 Review & Submit")
    st.write("Please carefully review all the collected information before final submission:")
    
    # Display data in a more organized way with enhanced styling
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3>📋 Complete Data Summary</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Staff & Household")
        st.info(f"**Staff ID**: {st.session_state.data.get('staff_id', 'N/A')}")
        st.info(f"**Household ID**: {st.session_state.data.get('household_id', 'N/A')}")
        st.info(f"**Language**: {st.session_state.data.get('language', 'N/A')}")
        
        st.markdown("### 🧒 Child Information")
        st.info(f"**Name**: {st.session_state.data.get('child_name', 'N/A')}")
        st.info(f"**Age**: {st.session_state.data.get('child_age_months', 'N/A')} months")
    
    with col2:
        st.markdown("### 📏 Measurements")
        st.info(f"**Height**: {st.session_state.data.get('height_cm', 'N/A')} cm")
        st.info(f"**Weight**: {st.session_state.data.get('weight_kg', 'N/A')} kg")
        
        st.markdown("### 📁 Files")
        photo_status = st.session_state.data.get('photo', 'Not uploaded')
        audio_status = st.session_state.data.get('audio_confirmation', 'Not uploaded')
        st.info(f"**Photo**: {photo_status}")
        st.info(f"**Audio**: {audio_status}")

    st.markdown("### 🕐 Timestamp")
    st.info(f"**Collected on**: {st.session_state.data.get('timestamp', 'N/A')}")

    # Final confirmation before submission
    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ FINAL CONFIRMATION REQUIRED</h4>
        <p>This is your last chance to review the data. Once submitted, the data will be permanently saved.</p>
        <p><strong>Please confirm that ALL the information above is correct and complete.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    final_confirmation = st.checkbox("✅ I confirm that all the information above is correct and complete", key="final_confirm")
    
    if not final_confirmation:
        st.warning("⚠️ Please check the confirmation box to proceed with submission.")

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back to Review", use_container_width=True):
            prev_step()
            st.rerun()
    with col2:
        if st.button("🚀 SUBMIT DATA", disabled=not final_confirmation, use_container_width=True):
            # Additional confirmation dialog
            if st.button("🔒 CONFIRM FINAL SUBMISSION", key="final_submit", use_container_width=True):
                # Save data to file
                filename = save_data_to_file(st.session_state.data)
                
                st.balloons()  # Celebration animation
                st.success(f"🎉 Data submitted successfully! Saved as {filename}")
                st.markdown("""
                <div class="confirmation-box">
                    <h4>✅ Submission Complete!</h4>
                    <p>Your data has been successfully saved and processed.</p>
                    <p><strong>Thank you for your contribution to child nutrition research!</strong></p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("💡 You can now start a new data collection by clicking 'Start New Collection' below.")
                
                if st.button("🔄 Start New Collection", use_container_width=True):
                    st.session_state.step = 1
                    st.session_state.data = {}
                    st.session_state.field_confirmations = {}
                    st.rerun()

# Enhanced sidebar with summary
with st.sidebar:
    st.header("📊 Collection Summary")
    st.write(f"Current Step: {step}/6")
    
    # Progress visualization
    progress_steps = ["Staff Info", "Child Info", "Measurements", "Photo", "Audio", "Review"]
    for i, step_name in enumerate(progress_steps, 1):
        if i < step:
            st.write(f"✅ {i}. {step_name}")
        elif i == step:
            st.write(f"🔄 {i}. {step_name} (Current)")
        else:
            st.write(f"⏳ {i}. {step_name}")
    
    if st.session_state.data:
        st.markdown("---")
        st.subheader("📝 Collected Data:")
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
    st.markdown("### 📋 Instructions:")
    st.markdown("""
    1. **Fill & Confirm** staff and household info
    2. **Enter & Verify** child details  
    3. **Record & Confirm** measurements
    4. **Upload & Verify** photo (optional)
    5. **Upload & Confirm** audio (optional)
    6. **Review & Submit** all data
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Tips:")
    st.markdown("""
    - ✅ Confirm each field after entry
    - 📝 Double-check measurements
    - 🔄 Use 'Back' to make changes
    - 💾 Data is saved after final submission
    """)