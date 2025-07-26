# IoT Heart Disease Predictor

A real-time IoT-based Heart Disease detector that collects data from sensors and predicts heart disease using machine learning.

## Features

- Real-time heart disease prediction using XGBoost model
- IoT sensor data integration (heart rate, SpO2, etc.)
- User authentication and registration
- Health record management and history
- PDF report generation
- Live data monitoring from AWS DynamoDB
- Responsive web interface

## Technology Stack

- **Backend**: Django 5.2.3
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Machine Learning**: XGBoost, scikit-learn
- **Database**: SQLite (local), AWS DynamoDB (IoT data)
- **Cloud**: AWS (DynamoDB for sensor data)

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd disease_predictor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Setup**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   AWS_REGION=us-west-1
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## Usage

1. Open your browser and go to `http://127.0.0.1:8000/`
2. Register a new account or login
3. Navigate to the heart disease prediction page
4. Enter patient information and sensor data
5. Get instant heart disease prediction results

## Project Structure

```
disease_predictor/
├── disease_predictor/     # Django project settings
├── prediction/           # Main app
│   ├── models.py        # Database models
│   ├── views.py         # View functions
│   ├── urls.py          # URL routing
│   └── middleware.py    # Custom middleware
├── templates/           # HTML templates
├── static/             # CSS, JS, images
├── heart_disease_xgboost_model.pkl  # ML model
└── requirements.txt    # Python dependencies
```

## Configuration

### AWS DynamoDB Setup
1. Create a DynamoDB table named 'HeartData'
2. Configure AWS credentials using environment variables
3. Ensure proper IAM permissions

### Model File
The XGBoost model file (`heart_disease_xgboost_model.pkl`) should be placed in the project root.

## Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for sensitive data
4. Set up proper database (PostgreSQL recommended)
5. Configure static file serving

### Security Notes
- Never commit `.env` files or sensitive credentials
- Use environment variables for all secrets
- Keep the ML model file secure
- Regularly update dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue on the repository.
