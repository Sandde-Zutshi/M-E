# Child Nutrition Data Collection App

A Streamlit-based application for collecting child nutrition data in field studies. This MVP demo provides a step-by-step interface for field staff to collect comprehensive nutrition information about children.

## 🌟 Features

- **Multi-step data collection flow** with progress tracking
- **Field staff and household information** capture
- **Child demographic data** collection
- **Physical measurements** (height and weight) with validation
- **Photo upload** for child identification (optional)
- **Audio confirmation** from mothers (optional)
- **Data validation** and quality checks
- **File storage** for uploaded media
- **JSON export** of collected data
- **Multi-language support** (English, Hindi, Telugu)

## 📋 Data Collection Steps

1. **Staff & Household Info** - Field staff ID, household ID, language selection
2. **Child Information** - Name and age (in months)
3. **Measurements** - Height (cm) and weight (kg) with validation warnings
4. **Photo Upload** - Optional child photo for identification
5. **Audio Confirmation** - Optional mother's voice confirmation
6. **Review & Submit** - Data verification and final submission

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd M-E
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run streamlit_app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8501
```

3. Follow the on-screen instructions to collect nutrition data

## 📁 Data Storage

- **Uploaded files** are saved in the `uploads/` directory
- **Collected data** is exported as JSON files in the `data/` directory
- **File naming convention**: includes timestamps for unique identification

## 🔧 Features & Improvements

### Bug Fixes Applied:
- ✅ Fixed validation logic in measurements step
- ✅ Added proper form validation with disabled buttons
- ✅ Fixed file upload requirements (now optional with skip options)
- ✅ Added actual file storage functionality

### Enhancements Added:
- ✅ Progress indicator showing current step
- ✅ Sidebar with collection summary and instructions
- ✅ Data persistence when navigating between steps
- ✅ Photo preview and audio playback
- ✅ Better organized review screen
- ✅ Improved user experience with clear validation messages
- ✅ JSON data export for permanent storage

## 🎯 Use Cases

- **Field nutrition surveys** in rural or remote areas
- **Community health monitoring** programs
- **Research data collection** for nutrition studies
- **Government health department** data gathering
- **NGO nutrition programs** monitoring

## 📊 Data Format

The app exports data in JSON format with the following structure:
```json
{
  "staff_id": "STAFF001",
  "household_id": "HH001",
  "language": "English",
  "child_name": "Child Name",
  "child_age_months": 24,
  "height_cm": 85.5,
  "weight_kg": 12.3,
  "photo": "photo_20231215_143022.jpg",
  "audio_confirmation": "audio_20231215_143025.wav",
  "timestamp": "2023-12-15T14:30:22.123456"
}
```

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.7+
- **Data Storage**: Local file system (JSON + uploaded files)
- **Session Management**: Streamlit session state
- **File Types Supported**: 
  - Images: JPG, JPEG, PNG
  - Audio: MP3, WAV, M4A

## 🚀 Deployment

This app can be deployed on:
- **Streamlit Cloud** (recommended for demos)
- **Heroku**
- **AWS/GCP/Azure** with container deployment
- **Local servers** for offline field use

## 📝 Notes

- The app is designed for MVP demonstration purposes
- File uploads are optional to accommodate different field conditions
- Data validation includes basic sanity checks for measurements
- All collected data is stored locally and can be exported for analysis

## 🤝 Contributing

This is a Monitoring & Evaluation test project. Feel free to suggest improvements or report issues.

---

**For support or questions, please create an issue in the repository.**
