# Waste Classification System 🌱♻️

An AI-powered application that uses computer vision to identify different types of waste materials and provide recycling guidance.

## Features

- **Image Classification**: Upload images of waste items for instant classification
- **Recycling Guidance**: Get specific recycling instructions for each waste type
- **Interactive Dashboard**: View classification history and waste distribution analytics
- **Educational Resources**: Learn about different waste types and recycling best practices

## Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: TensorFlow, OpenCV
- **Data Processing**: Pandas, NumPy, Pillow
- **Visualization**: Plotly, Matplotlib

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/RecycleAI.git
cd RecycleAI
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Launch the application using the command above
2. Upload an image of waste material through the interface
3. Get instant classification and recycling guidance
4. View analytics and historical data in the dashboard
5. Explore educational resources about waste management

## Project Structure

```
RecycleAI/
├── app.py              # Main application file
├── model.py           # AI model and prediction functions
├── utils.py           # Utility functions
├── waste_info.py      # Waste category information
├── requirements.txt   # Project dependencies
├── pages/            # Additional application pages
│   ├── about.py     # About page
│   ├── dashboard.py # Analytics dashboard
│   └── education.py # Educational resources
└── assets/          # Images and other static files
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 