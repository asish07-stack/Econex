# 🌱 EcoNex – AI-Powered Smart Food Waste Reduction & Sustainable Redistribution Ecosystem

## 📌 Project Overview

EcoNex is an AI-powered smart food waste reduction and sustainable redistribution ecosystem designed to minimize food wastage and promote efficient food redistribution.

The platform helps food providers identify surplus food, estimate demand, verify food quality, and connect available food with suitable recipient organizations. Its goal is to transform surplus food into meaningful social impact while reducing environmental waste.

## 🎯 Problem Statement

Food wastage is a major global challenge. Large quantities of food are wasted at different stages, including production, storage, distribution, retail, and consumption.

At the same time, many communities face food insecurity. The lack of efficient demand forecasting, surplus identification, and redistribution systems creates a gap between available food and people who need it.

## 💡 Proposed Solution

EcoNex provides a centralized web-based ecosystem that supports:

- Food demand forecasting.
- Surplus food identification.
- Food quality verification.
- Smart food redistribution.
- Impact monitoring and analytics.

The platform aims to improve food utilization, reduce unnecessary waste, and support sustainable food distribution.

## ✨ Key Features

### 1. 📊 Demand Forecasting
Helps estimate expected food demand using available inputs and forecasting logic.

### 2. 🍱 Surplus Food Detection
Identifies excess food by comparing available meals with expected demand.

### 3. 🥗 Food Quality Verification
Provides a food quality assessment interface to support safer food redistribution decisions.

### 4. 🚚 Smart Redistribution
Supports matching surplus food with suitable recipient organizations based on factors such as quantity, distance, food quality, and pickup requirements.

### 5. 📈 Impact Dashboard
Displays food rescue and sustainability-related metrics to demonstrate the impact of redistribution activities.

### 6. 🏢 Multiple User Interfaces
Includes dedicated interfaces for food providers and recipient organizations to support the redistribution process.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Flask | Backend web framework |
| HTML5 | Web page structure |
| CSS3 | Styling and responsive design |
| JavaScript | Interactive functionality |

## 🏗️ Project Structure

```text
EcoNex/
│
├── app.py
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── demand.html
│   ├── surplus.html
│   ├── quality.html
│   ├── redistribution.html
│   ├── impact.html
│   └── other HTML templates
│
└── static/
    └── CSS, JavaScript and image assets
```

*Note: The structure above describes the intended organization. Actual folders and files may vary according to the project implementation.*

## ⚙️ Installation and Setup

Follow these steps to run EcoNex locally.

### Prerequisites

- Python 3 installed.
- Visual Studio Code.
- Git installed.

### Step 1: Clone the repository

```bash
git clone https://github.com/asish07-stack/Econex.git
```

### Step 2: Open the project folder

```bash
cd Econex
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

Install Flask and any other packages required by the application:

```bash
pip install flask
```

### Step 6: Run the application

```bash
python app.py
```

### Step 7: Open the website

Visit the following address in your browser:

```text
http://127.0.0.1:5000/
```

## 🌍 Expected Impact

EcoNex aims to:

- Reduce food wastage through better surplus identification.
- Improve utilization of available food resources.
- Connect surplus food providers with recipient organizations.
- Encourage sustainable food management practices.
- Support communities through efficient food redistribution.
- Promote environmental awareness and responsible consumption.

## 🚀 Future Enhancements

- Integration with real-time AI-based demand prediction APIs.
- GPS-based live redistribution tracking.
- Real-time notifications for food providers and recipients.
- Advanced analytics and reporting.
- Integration with verified NGOs and food donation organizations.

## 👥 Project Information

**Project Name:** EcoNex

**Project Category:** AI and Sustainability

**Project Theme:** Smart Food Waste Reduction and Sustainable Redistribution

**Project Type:** Hackathon Web Application

## ❤️ Our Vision

**Turn Food Surplus Into Social Impact.**

EcoNex envisions a sustainable ecosystem where surplus food is identified, managed, and redistributed efficiently so that less food goes to waste and more people can benefit from available resources.

---

*Developed as a hackathon project with the aim of promoting food sustainability through technology.*
