# ISRO Satellite Tracker

This project allows users to track the real-time locations of ISRO satellites on a map using **Streamlit** and **Python**. The satellite data is fetched using an API, and the satellite locations are displayed on an interactive map.

---

## Features

- Real-time tracking of ISRO satellites like Cartosat, INSAT, GSAT, RISAT, etc.
- Visual display of satellite positions on a map using **PyDeck**.
- User-friendly interface to select and display different satellites.
- **Streamlit** interface for easy usage and deployment.

---

## Requirements

Before running this application, make sure you have the following installed:

- **Python** 3.7+ (preferably Python 3.9 or higher)
- **Git** (for version control)
- **Virtual Environment** (recommended to avoid conflicts with system libraries)

---

## Installation

### 1. Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/your-username/ISRO-Satellite-Tracker.git
cd ISRO-Satellite-Tracker
```

### 2. Set Up a Virtual Environment
It's a good idea to create a virtual environment for the project:

For Windows:

```bash
Copy code
python -m venv venv
```
For macOS/Linux:

```bash
Copy code
python3 -m venv venv
```
### 3. Activate the Virtual Environment
For Windows:

```bash
Copy code
.\venv\Scripts\activate
```
For macOS/Linux:

```bash
Copy code
source venv/bin/activate
```
### 4. Install Required Dependencies
Install all the necessary Python libraries using pip. Run the following command to install the required dependencies:

```bash
Copy code
pip install streamlit requests pydeck pandas
```

### 5. API Setup
This application uses the N2YO API to fetch satellite data. You will need an API key to run the app.

Sign up for a free API key at N2YO API.
Once you receive your API key, create a .env file in the project root directory and add the following line:
```bash
N2YO_API_KEY=your_api_key_here
```
Replace your_api_key_here with the actual key you received.


### 6. Running the Application
Once the setup is complete, you can run the Streamlit app by using the following command:

```bash
Copy code
streamlit run main.py
```
