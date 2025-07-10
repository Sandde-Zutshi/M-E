import streamlit as st
import os
import json
from datetime import datetime
import math

# Custom CSS for better styling including dashboard cards
st.markdown("""
<style>
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .data-entry-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .confirmation-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: white;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }
    
    .field-confirmed {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #2d3748;
        border-left: 4px solid #4CAF50;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: #744210;
        box-shadow: 0 4px 15px rgba(252, 182, 159, 0.3);
    }
    
    /* Dashboard Cards Styling */
    .dashboard-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
    }
    
    .stats-card {
        border-radius: 20px;
        padding: 25px;
        margin: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        min-height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .stats-card:hover {
        transform: translateY(-5px);
    }
    
    .card-heart {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    }
    
    .card-sleep {
        background: linear-gradient(135deg, #a55eea 0%, #26de81 100%);
    }
    
    .card-weight {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%);
    }
    
    .card-height {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
    }
    
    .card-age {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
    }
    
    .card-info {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        color: #2d3748;
    }
    
    .card-value {
        font-size: 2.5em;
        font-weight: bold;
        margin: 10px 0;
    }
    
    .card-label {
        font-size: 1em;
        opacity: 0.9;
        margin-bottom: 5px;
    }
    
    .card-unit {
        font-size: 0.9em;
        opacity: 0.8;
    }
    
    .success-check {
        color: #4CAF50;
        font-size: 20px;
    }
    
    .expandable-section {
        background: white;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        cursor: pointer;
        font-size: 1.2em;
        font-weight: bold;
    }
    
    .section-content {
        padding: 25px;
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
if 'expanded_sections' not in st.session_state:
    st.session_state.expanded_sections = {}
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# Function to toggle section expansion
def toggle_section(section_key):
    if section_key not in st.session_state.expanded_sections:
        st.session_state.expanded_sections[section_key] = False
    st.session_state.expanded_sections[section_key] = not st.session_state.expanded_sections[section_key]

# Function to show expandable data entry section
def show_expandable_section(title, icon, section_key, content_func):
    is_expanded = st.session_state.expanded_sections.get(section_key, False)
    
    st.markdown(f"""
    <div class="expandable-section">
        <div class="section-header">
            {icon} {title} {'▼' if is_expanded else '▶'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"{'Collapse' if is_expanded else 'Expand'} {title}", key=f"toggle_{section_key}"):
        toggle_section(section_key)
        st.rerun()
    
    if is_expanded:
        with st.container():
            st.markdown('<div class="section-content">', unsafe_allow_html=True)
            content_func()
            st.markdown('</div>', unsafe_allow_html=True)

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

# Function to calculate BMI
def calculate_bmi(weight_kg, height_cm):
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

# Function to get BMI category for children
def get_child_bmi_category(bmi):
    if bmi < 15:
        return "Underweight"
    elif bmi < 18:
        return "Normal"
    elif bmi < 25:
        return "Overweight"
    else:
        return "Obese"

# Function to show dashboard
def show_dashboard():
    st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
    
    st.markdown("# 📊 Child Health Dashboard")
    st.markdown(f"### {st.session_state.data.get('child_name', 'Child')}'s Health Statistics")
    
    # Calculate BMI if we have height and weight
    height = st.session_state.data.get('height_cm', 0)
    weight = st.session_state.data.get('weight_kg', 0)
    bmi = calculate_bmi(weight, height) if height > 0 and weight > 0 else 0
    bmi_category = get_child_bmi_category(bmi) if bmi > 0 else "N/A"
    
    # Create dashboard cards
    col1, col2 = st.columns(2)
    
    with col1:
        # Age Card
        st.markdown(f"""
        <div class="stats-card card-age">
            <div class="card-label">👶 Age</div>
            <div class="card-value">{st.session_state.data.get('child_age_months', 0)}</div>
            <div class="card-unit">months old</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Weight Card
        st.markdown(f"""
        <div class="stats-card card-weight">
            <div class="card-label">⚖️ Weight</div>
            <div class="card-value">{st.session_state.data.get('weight_kg', 0)}</div>
            <div class="card-unit">kg</div>
        </div>
        """, unsafe_allow_html=True)
        
        # BMI Card
        st.markdown(f"""
        <div class="stats-card card-heart">
            <div class="card-label">📈 BMI</div>
            <div class="card-value">{bmi:.1f if bmi > 0 else 'N/A'}</div>
            <div class="card-unit">{bmi_category}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Height Card
        st.markdown(f"""
        <div class="stats-card card-height">
            <div class="card-label">📏 Height</div>
            <div class="card-value">{st.session_state.data.get('height_cm', 0)}</div>
            <div class="card-unit">cm</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Staff Info Card
        st.markdown(f"""
        <div class="stats-card card-info">
            <div class="card-label">👥 Staff ID</div>
            <div class="card-value" style="font-size: 1.8em;">{st.session_state.data.get('staff_id', 'N/A')}</div>
            <div class="card-unit">Field Worker</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Household Info Card
        st.markdown(f"""
        <div class="stats-card card-sleep">
            <div class="card-label">🏠 Household</div>
            <div class="card-value" style="font-size: 1.8em;">{st.session_state.data.get('household_id', 'N/A')}</div>
            <div class="card-unit">ID Number</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Information
    st.markdown("### 📋 Additional Information")
    col3, col4 = st.columns(2)
    
    with col3:
        st.info(f"**Language**: {st.session_state.data.get('language', 'N/A')}")
        st.info(f"**Photo**: {'✅ Uploaded' if st.session_state.data.get('photo', '') not in ['', 'skipped'] else '❌ Not uploaded'}")
    
    with col4:
        st.info(f"**Audio**: {'✅ Uploaded' if st.session_state.data.get('audio_confirmation', '') not in ['', 'skipped'] else '❌ Not uploaded'}")
        st.info(f"**Recorded**: {datetime.fromisoformat(st.session_state.data.get('timestamp', '')).strftime('%Y-%m-%d %H:%M') if st.session_state.data.get('timestamp') else 'N/A'}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📤 Export Data", use_container_width=True):
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(st.session_state.data, indent=2),
                file_name=f"child_data_{st.session_state.data.get('child_name', 'unknown')}.json",
                mime="application/json"
            )
    with col2:
        if st.button("🔄 New Collection", use_container_width=True):
            st.session_state.step = 1
            st.session_state.data = {}
            st.session_state.field_confirmations = {}
            st.session_state.expanded_sections = {}
            st.session_state.show_dashboard = False
            st.rerun()
    with col3:
        if st.button("📊 View Raw Data", use_container_width=True):
            st.json(st.session_state.data)

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

# Main app logic
if st.session_state.show_dashboard:
    show_dashboard()
else:
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.title("🧒 Child Nutrition Data Collection")
    st.markdown("### Enhanced Interactive Data Entry System")
    st.markdown("---")

    # Progress indicator
    progress_value = (st.session_state.step - 1) / 5
    st.progress(progress_value)
    st.write(f"Step {st.session_state.step} of 6")

    step = st.session_state.step

    if step == 1:
        st.header("👤 Staff & Household Information")
        
        def staff_content():
            staff_id = st.text_input("Enter Field Staff ID", value=st.session_state.data.get('staff_id', ''))
            staff_confirmed = False
            if staff_id.strip():
                staff_confirmed = show_field_confirmation("Staff ID", staff_id, "staff_id")
            return staff_id, staff_confirmed
        
        def household_content():
            household_id = st.text_input("Enter Household ID", value=st.session_state.data.get('household_id', ''))
            household_confirmed = False
            if household_id.strip():
                household_confirmed = show_field_confirmation("Household ID", household_id, "household_id")
            return household_id, household_confirmed
        
        def language_content():
            language = st.selectbox("Select Language", ["English", "Hindi", "Telugu"], 
                                   index=["English", "Hindi", "Telugu"].index(st.session_state.data.get('language', 'English')))
            language_confirmed = False
            if language:
                language_confirmed = show_field_confirmation("Language", language, "language")
            return language, language_confirmed
        
        # Show expandable sections
        show_expandable_section("Staff ID Entry", "👨‍💼", "staff_section", lambda: staff_content())
        show_expandable_section("Household ID Entry", "🏠", "household_section", lambda: household_content())
        show_expandable_section("Language Selection", "🌐", "language_section", lambda: language_content())
        
        # Get current values for validation
        staff_id = st.session_state.data.get('staff_id', '')
        household_id = st.session_state.data.get('household_id', '')
        language = st.session_state.data.get('language', 'English')
        
        # Check confirmations
        staff_confirmed = st.session_state.field_confirmations.get('staff_id', False)
        household_confirmed = st.session_state.field_confirmations.get('household_id', False)
        language_confirmed = st.session_state.field_confirmations.get('language', False)
        
        can_proceed = staff_confirmed and household_confirmed and language_confirmed
        
        if not can_proceed:
            st.warning("⚠️ Please expand each section, enter the required information, and confirm all fields to continue.")

        st.markdown("---")
        if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
            st.session_state.data['staff_id'] = staff_id
            st.session_state.data['household_id'] = household_id
            st.session_state.data['language'] = language
            st.session_state.data['timestamp'] = datetime.now().isoformat()
            next_step()
            st.rerun()

    elif step == 2:
        st.header("🧒 Child Information")
        
        def name_content():
            name = st.text_input("Child's Name", value=st.session_state.data.get('child_name', ''))
            name_confirmed = False
            if name.strip():
                name_confirmed = show_field_confirmation("Child's Name", name, "child_name")
            return name, name_confirmed
        
        def age_content():
            age = st.number_input("Child's Age (in months)", min_value=0, max_value=120, 
                                 value=st.session_state.data.get('child_age_months', 0))
            age_confirmed = False
            if age > 0:
                age_confirmed = show_field_confirmation("Child's Age", f"{age} months", "child_age")
            return age, age_confirmed
        
        show_expandable_section("Child's Name", "👶", "name_section", lambda: name_content())
        show_expandable_section("Child's Age", "📅", "age_section", lambda: age_content())
        
        # Check confirmations
        name_confirmed = st.session_state.field_confirmations.get('child_name', False)
        age_confirmed = st.session_state.field_confirmations.get('child_age', False)
        
        can_proceed = name_confirmed and age_confirmed
        
        if not can_proceed:
            st.warning("⚠️ Please expand each section, enter the required information, and confirm all fields to continue.")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back", use_container_width=True):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
                next_step()
                st.rerun()

    elif step == 3:
        st.header("📏 Physical Measurements")
        
        def height_content():
            height = st.number_input("Height (cm)", min_value=30.0, max_value=200.0, 
                                    value=st.session_state.data.get('height_cm', 50.0))
            height_confirmed = False
            if height > 0:
                height_confirmed = show_field_confirmation("Height", f"{height} cm", "height")
            return height, height_confirmed
        
        def weight_content():
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=100.0, 
                                    value=st.session_state.data.get('weight_kg', 3.0))
            weight_confirmed = False
            if weight > 0:
                weight_confirmed = show_field_confirmation("Weight", f"{weight} kg", "weight")
                
                # Show BMI calculation if both height and weight are available
                height = st.session_state.data.get('height_cm', 0)
                if height > 0:
                    bmi = calculate_bmi(weight, height)
                    bmi_category = get_child_bmi_category(bmi)
                    st.info(f"📊 Calculated BMI: {bmi:.1f} ({bmi_category})")
            
            return weight, weight_confirmed
        
        show_expandable_section("Height Measurement", "📏", "height_section", lambda: height_content())
        show_expandable_section("Weight Measurement", "⚖️", "weight_section", lambda: weight_content())
        
        # Check confirmations
        height_confirmed = st.session_state.field_confirmations.get('height', False)
        weight_confirmed = st.session_state.field_confirmations.get('weight', False)
        
        can_proceed = height_confirmed and weight_confirmed
        
        if not can_proceed:
            st.warning("⚠️ Please expand each section, enter the measurements, and confirm all fields to continue.")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Back", use_container_width=True):
                prev_step()
                st.rerun()
        with col2:
            if st.button("Next ➡️", disabled=not can_proceed, use_container_width=True):
                next_step()
                st.rerun()

    elif step == 4:
        st.header("📸 Photo Upload")
        
        def photo_content():
            st.write("Please upload a recent photo of the child for identification purposes.")
            photo = st.file_uploader("Upload a photo of the child", type=["jpg", "jpeg", "png"])
            photo_confirmed = False

            if photo is not None:
                st.image(photo, caption="Uploaded Photo", width=300)
                photo_confirmed = show_field_confirmation("Child's Photo", f"File: {photo.name}", "photo")
            
            return photo, photo_confirmed
        
        show_expandable_section("Photo Upload", "📸", "photo_section", lambda: photo_content())
        
        photo_confirmed = st.session_state.field_confirmations.get('photo', False)

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
                # Save the photo
                if 'photo' in st.session_state:
                    filename = save_uploaded_file(st.session_state.photo, "photo")
                    st.session_state.data['photo'] = filename
                next_step()
                st.rerun()

    elif step == 5:
        st.header("🎙️ Audio Confirmation")
        
        def audio_content():
            st.write("Please record the mother's voice confirmation (e.g., 'Yes, this information is correct').")
            audio = st.file_uploader("Upload mother's voice confirmation", type=["mp3", "wav", "m4a"])
            audio_confirmed = False

            if audio is not None:
                st.audio(audio)
                audio_confirmed = show_field_confirmation("Audio Confirmation", f"File: {audio.name}", "audio")
            
            return audio, audio_confirmed
        
        show_expandable_section("Audio Upload", "🎙️", "audio_section", lambda: audio_content())
        
        audio_confirmed = st.session_state.field_confirmations.get('audio', False)

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
                # Save the audio
                if 'audio' in st.session_state:
                    filename = save_uploaded_file(st.session_state.audio, "audio")
                    st.session_state.data['audio_confirmation'] = filename
                next_step()
                st.rerun()

    elif step == 6:
        st.header("🧾 Final Review & Submission")
        st.write("Please carefully review all the collected information before final submission:")
        
        # Enhanced review display
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">
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
            
            # Show calculated BMI
            height = st.session_state.data.get('height_cm', 0)
            weight = st.session_state.data.get('weight_kg', 0)
            if height > 0 and weight > 0:
                bmi = calculate_bmi(weight, height)
                bmi_category = get_child_bmi_category(bmi)
                st.info(f"**BMI**: {bmi:.1f} ({bmi_category})")
            
            st.markdown("### 📁 Files")
            photo_status = st.session_state.data.get('photo', 'Not uploaded')
            audio_status = st.session_state.data.get('audio_confirmation', 'Not uploaded')
            st.info(f"**Photo**: {photo_status}")
            st.info(f"**Audio**: {audio_status}")

        # Final confirmation
        st.markdown("---")
        st.markdown("""
        <div class="warning-box">
            <h4>⚠️ FINAL CONFIRMATION REQUIRED</h4>
            <p>This is your last chance to review the data. Once submitted, the data will be permanently saved and the dashboard will be displayed.</p>
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
                # Save data to file
                filename = save_data_to_file(st.session_state.data)
                
                st.balloons()  # Celebration animation
                st.success(f"🎉 Data submitted successfully! Saved as {filename}")
                
                # Automatically show dashboard after submission
                st.session_state.show_dashboard = True
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced sidebar
with st.sidebar:
    st.header("📊 Collection Summary")
    st.write(f"Current Step: {st.session_state.step}/6")
    
    # Progress visualization
    progress_steps = ["Staff Info", "Child Info", "Measurements", "Photo", "Audio", "Review"]
    for i, step_name in enumerate(progress_steps, 1):
        if i < st.session_state.step:
            st.write(f"✅ {i}. {step_name}")
        elif i == st.session_state.step:
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
    1. **Expand & Fill** each data section
    2. **Confirm** every entered field  
    3. **Navigate** using Back/Next buttons
    4. **Review** all data before submission
    5. **View Dashboard** after successful submission
    """)
    
    if st.session_state.show_dashboard:
        st.markdown("---")
        if st.button("🔙 Back to Form", use_container_width=True):
            st.session_state.show_dashboard = False
            st.rerun()