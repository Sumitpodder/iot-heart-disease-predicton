import pickle
from django.shortcuts import render,HttpResponse, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from prediction.middleware import auth, guest  # User-defined middleware imports
from django.contrib import messages
from django.shortcuts import render
from .models import *
from django.utils.timezone import now
import pandas as pd
import logging
import os
from django.http import JsonResponse
from prediction.models import HealthRecord
from .models import HealthRecord
import boto3
import statistics
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa 


# Connect to DynamoDB
# Note: Configure AWS credentials using environment variables or AWS CLI
# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY should be set in environment
try:
    dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
    table = dynamodb.Table('HeartData')
except Exception as e:
    print(f"AWS DynamoDB connection failed: {e}")
    table = None


# Function to fetch latest 5 rows
def get_latest_rows(n=5):
    response = table.scan()
    items = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)
    return items[:n]

# View to render in template
def live_data_view(request):
    latest_data = get_latest_rows()
    
    return render(request, 'live_data.html', {'data': latest_data})
   
def compute_mean(data_list, field):
    values = [float(row[field]) for row in data_list if field in row]
    return round(statistics.mean(values), 2) if values else None

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response if not pisa_status.err else HttpResponse('PDF generation failed')

def download_pdf(request, record_id):
    record = HealthRecord.objects.get(id=record_id)
    return render_to_pdf('summary.html', {'records': [record]})

@auth
def homePage(request):
    return render(request,'homePage.html')

@auth
def diseasePage(request):
    return render(request,'disease.html')

@guest
def signupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        uemail = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        try:
            my_user = User.objects.create_user(uname, uemail, pass1)
            my_user.save()
            messages.success(request, "Signup successful! Please log in.")
            return redirect('login') 
        except Exception as e:
            messages.error(request, f"Error during signup: {e}")
            return redirect('register')

    return render(request, 'register.html')

@guest
def loginPage(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        u_pass = request.POST.get('pass')
        user = authenticate(request, username=u_name, password=u_pass)

        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  

    return render(request, 'login.html')


def delete_records(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_records')
        if selected_ids:
            HealthRecord.objects.filter(id__in=selected_ids).delete()
    return redirect('history')


def add(request):
    return HttpResponse("add")

def edit(request):
    return HttpResponse("Edit")

def update(request):
    return HttpResponse("update")

def delete(request):
    return HttpResponse("delete")


# Prediction.......................................

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Construct the absolute path to the model
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'heart_disease_xgboost_model.pkl')

# Load the model
try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    model = None
    logger.error("Model file not found. Ensure 'heart_disease_model.pkl' exists.")
except pickle.UnpicklingError:
    model = None
    logger.error("The Pickle file is corrupted or incompatible.") 

@auth
def heart_disease_predictPage(request):
    if request.method == 'POST':
        latest_rows = get_latest_rows(5)

        sensor_mean = {
            'heartrate': compute_mean(latest_rows, 'heart_rate'),
            'spo2': compute_mean(latest_rows, 'spo2'),
            'oldpeak': compute_mean(latest_rows, 'oldpeak'),
            'thalach': compute_mean(latest_rows, 'thalach'),
            'slope': compute_mean(latest_rows, 'slope'),
        }

        if model is None:
            return HttpResponse("Error: Prediction model is not available.")

        try:
            # Extract form data
            name = str(request.POST.get('name', ''))
            gender = str(request.POST.get('gender', ''))
            age = int(request.POST.get('age', 0))
            cp = int(request.POST.get('cp', 0))
            trestbps = int(request.POST.get('trestbps', 0))
            chol = int(request.POST.get('chol', 0))

            # Use form input or fallback to computed mean
            thalach = int(request.POST.get('thalach', sensor_mean.get('thalach', 0)))
            oldpeak = float(request.POST.get('oldpeak', sensor_mean.get('oldpeak', 0)))
            heartrate= int(request.POST.get('heartrate',sensor_mean.get('heartrate',0)))
            spo2= int(request.POST.get('spo2',sensor_mean.get('spo2',0)))

            ca = int(request.POST.get('ca', 0))
            thal = int(request.POST.get('thal', 0))

            # Prepare input for model
            input_data = pd.DataFrame({
                'age': [age],
                'cp': [cp],
                'trestbps': [trestbps],
                'chol': [chol],
                'thalach': [thalach],
                'oldpeak': [oldpeak],
                'ca': [ca],
                'thal': [thal]
            })

            # Perform prediction
            prediction = model.predict(input_data)
            result = "Negative" if prediction[0] == 0 else "Positive"

            # Save result to database
            records = HealthRecord(
                name=name,
                gender=gender,
                age=age,
                cp=cp,
                trestbps=trestbps,
                chol=chol,
                thalach=thalach,
                oldpeak=oldpeak,
                heartrate=heartrate,
                spo2=spo2,
                ca=ca,
                thal=thal,
                result=result
            )
            records.save()

            return render(request, 'heart_predict.html', {'result': result})

        except ValueError as e:
            return HttpResponse(f"Invalid input: {e}")
        except Exception as e:
            return HttpResponse(f"Error during prediction: {e}")

    return render(request, 'heart_predict.html')

   
def diabetes_predictPage(request):
    return HttpResponse("Diabetes Prediction Page")

def brain_tumor_predictPage(request):
    return HttpResponse("Brain_tumor Predict page")

def contact(request):
    return render(request,'contact.html')

@auth
def historyPage(request):
    records = HealthRecord.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'records':records})
@auth
def reportPage(request):
    latest_record = HealthRecord.objects.latest('timestamp')  # Get the most recent entry
    return render(request, 'reportPage.html', {'records': [latest_record]})  # Wrap in list
    # records=HealthRecord.objects.all()
    # return render(request,'reportPage.html',{'records':records})

# Logout Page View
def logoutPage(request):
    logout(request)
    return redirect('login')