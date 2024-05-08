#Importing required libraries
from flask import Flask, render_template, request, redirect, url_for,jsonify, session, url_for, flash
import schedule
from customer_support_bot import CustomerSupportBot
import json
import random
import datetime
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import numpy as np
import os
import csv
import zipfile
import hashlib
from threading import Thread
import ssl
import smtplib
from email.message import EmailMessage
import time
from googleapiclient.discovery import build
import secrets
from datetime import date
from flask_socketio import SocketIO, emit
import serial
import threading
import os
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


# Set your YouTube API key
api_key = 'AIzaSyAJYVzSq7E4tzpoLrOxuxoH7Ex40CoVRUQ'

# Create a YouTube service object
youtube = build('youtube', 'v3', developerKey=api_key)

# Function to search YouTube videos based on a query
def search_youtube(query):
    # Make a search request to the YouTube API
    search_response = youtube.search().list(
        q=query,  # The search query
        type='video',  # Type of result: video
        part='id,snippet',  # Include snippet to get video details
        maxResults=10  # Maximum number of results to retrieve
    ).execute()

    videos = []
    # Iterate through the search results and extract video details
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            # Extract video information
            video_id = search_result['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_title = search_result['snippet']['title']
            video_thumbnail = search_result['snippet']['thumbnails']['default']['url']
            
            # Append video details to the list
            videos.append({
                'title': video_title,
                'url': video_url,
                'thumbnail': video_thumbnail
            })
    return videos  # Return the list of video details





# Import necessary modules
from googleapiclient.discovery import build

# Define the first set of YouTube API credentials
api_key1 = 'AIzaSyDMfqV2nCoymsGfa-3teHJU5I37DzQDJ6k'
youtube1 = build('youtube', 'v3', developerKey=api_key1)

# Function to search YouTube videos using the first set of credentials
def search_youtube1(query):
    search_response = youtube1.search().list(
        q=query,
        type='video',
        part='id,snippet',  # Include snippet to get video details
        maxResults=5
    ).execute()

    videos = []
    # Extract video details from the search response
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_title = search_result['snippet']['title']
            video_thumbnail = search_result['snippet']['thumbnails']['default']['url']
            # Append video details to the list
            videos.append({
                'title': video_title,
                'url': video_url,
                'thumbnail': video_thumbnail
            })
    return videos  # Return the list of video details

# Define the second set of YouTube API credentials
api_key2 = 'AIzaSyDq--3E3U_oD0s7FB_BsYKmAlWBgDqbRUg'
youtube2 = build('youtube', 'v3', developerKey=api_key2)

# Function to search YouTube videos using the second set of credentials
def search_youtube(query):
    search_response = youtube2.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()

    videos = []
    # Extract video details from the search response
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            video_id = search_result['id']['videoId']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            video_title = search_result['snippet']['title']
            video_thumbnail = search_result['snippet']['thumbnails']['default']['url']
            # Append video details to the list
            videos.append({
                'title': video_title,
                'url': video_url,
                'thumbnail': video_thumbnail
            })
    return videos  # Return the list of video details


# File storing email addresses
EMAILS_FILE = 'emails.json'

# Define Flask app and SocketIO
app = Flask(__name__)
socketio = SocketIO(app)

# Instantiate CustomerSupportBot
bot = CustomerSupportBot()
workout_history = ""

# Email content and credentials
email_sender = "fivecoders2022@gmail.com"
email_password = "cxtl wuqv xioo ldns"  # Example password (for demonstration purposes)
subject = 'FitKit NewsLetter'
body = """
... [Email Body Content] ...
"""

# Function to send emails to subscribers
def send_email_to_subscribers():
    # Load emails from a JSON file
    with open(EMAILS_FILE, 'r') as file:
        emails = json.load(file)

    # Create SSL context for secure email transmission
    context = ssl.create_default_context()

    # Loop through each email address and send the newsletter
    for email in emails:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body)

        # Connect to the SMTP server (Gmail in this case) and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            try:
                smtp.login(email_sender, email_password)
                smtp.send_message(em)
                print(f"Email sent to {email} successfully!")
            except Exception as e:
                print(f"An error occurred while sending email to {email}: {str(e)}")


# Function to create a PDF report with tables
@app.route('/report', methods=['GET','POST'])
def create_pdf_report():
    if request.method == 'POST':
        report_filename = "report.pdf"
        data_files = {
        "water_intake_data.csv": "Data Table",
        "workout_log.txt": "Text File",
        "bmi_records.txt": "Text File"
        }
        doc = SimpleDocTemplate(report_filename, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph("Health Report", styles["Title"]))

        for file, table_name in data_files.items():
            elements.append(Paragraph(table_name, styles["Heading2"]))

            if os.path.exists(file):
                if file.endswith(".csv"):
                    df = pd.read_csv(file)
                    data = [df.columns] + df.values.tolist()
                    t = Table(data)
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ]))
                    elements.append(t)
                elif file.endswith(".txt"):
                    with open(file, "r") as f:
                        text = f.read()
                    #append every Exercise to include a newline using for loop
                    paragraphs = []
                    for line in text.splitlines():
                        paragraphs.append(Paragraph(line, styles["Normal"]))
                    elements.extend(paragraphs)
            else:
                elements.append(Paragraph(f"{file} not found\n", styles["Normal"]))
        elements.append(Paragraph("\n", styles["Normal"]))
        elements.append(Paragraph("Water Intake Plot", styles["Heading2"]))
        image_path = "static/Figure 1.png"  # Replace with the path to your image file
        img = Image(image_path, width=300, height=200)
        elements.append(img)
        elements.append(Paragraph("Calorie Tracker Plot", styles["Heading2"]))
        image_path = "static/1.png"  # Replace with the path to your image file
        img = Image(image_path, width=300, height=200)
        elements.append(img)
        doc.build(elements)
        create_pdf_report()
        return send_file(report_filename, as_attachment=True)
    else:
        return render_template('report.html')


# Route for 'land.html' handling both GET and POST requests
@app.route('/land.html', methods=['GET', 'POST'])
def news():
    if request.method == 'POST':  # If a POST request is made
        email = request.form['email']  # Get the email from the form
        if email:  # If an email is provided
            # Add the email to the list stored in the EMAILS_FILE
            with open(EMAILS_FILE, 'r') as file:
                emails = json.load(file)
            emails.append(email)
            with open(EMAILS_FILE, 'w') as file:
                json.dump(emails, file)
        
    return render_template('hi.html')  # Render 'hi.html'

# Route for 'music.html'
@app.route('/music.html')
def videooo():
    search_query = 'workout playlist'  # Define the search query
    videos = search_youtube(search_query)  # Get workout playlist videos from YouTube
    return render_template('music.html', videos=videos)  # Render 'music.html' and pass videos data to the template

# Generating a secret key using the 'secrets' module
secret_key = secrets.token_hex(16)
app.secret_key = secret_key  # Set the generated secret key for the Flask app

# File operations related to water intake data
data_file = "water_intake_data.csv"
# If the data file doesn't exist, create it and write headers (Date, Intake)
if not os.path.exists(data_file):
    with open(data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Intake"])



# Load data from the CSV file
data = {}
with open(data_file, "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data[row["Date"]] = {"intake": float(row["Intake"])}

# Set a daily water consumption target
daily_target = 8  # Change this to your desired daily target in ml

def save_data():
    # Save data to the CSV file
    with open(data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Intake"])
        for date, info in data.items():
            writer.writerow([date, info["intake"]])

def add_log(date, amount):
    if date not in data:
        data[date] = {"intake": 0}
    data[date]["intake"] += amount
    save_data()

def delete_log_entry(date):
    if date in data:
        del data[date]
        save_data()
        print("Log deleted!")

def get_daily_intake(date):
    if date in data:
        return data[date]["intake"]
    else:
        return 0

def calculate_average_monthly_intake():
    today = datetime.today()
    total_intake = 0
    num_days = 0
    for date, info in data.items():
        log_date = datetime.strptime(date, "%Y-%m-%d")
        if log_date.year == today.year and log_date.month == today.month:
            total_intake += info["intake"]
            num_days += 1
    if num_days == 0:
        return 0
    return total_intake / num_days

def generate_plot():
    dates = []
    intake = []
    for date, info in data.items():
        dates.append(date)
        intake.append(info["intake"])

    plt.figure(figsize=(10, 6))
    plt.plot(dates, intake, marker='o', linestyle='-', color='b')
    plt.title("Water Intake Over Time")
    plt.xlabel("Date")
    plt.ylabel("Intake (ml)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("static/Figure 1.png")
    plt.show()
    #zip "Figure 1.png" to a file
    with zipfile.ZipFile('wi.zip', 'w') as file_zip:
        file_zip.write('Figure 1.png', compress_type=zipfile.ZIP_DEFLATED)
    print("File is zipped")
    
    with zipfile.ZipFile("wi.zip",'r') as extract_zip:
        extract_zip.extractall("EXTRACT")

# Main program loop

# Route for displaying 'menu.html'
@app.route('/menu.html')
def menu():
    return render_template('menu.html')

# Route for adding daily water intake log
@app.route('/add_log', methods=['GET', 'POST'])
def add_daily_log():
    if request.method == 'POST':
        # Capture date and amount from the form
        date = request.form['date']
        amount = float(request.form['amount'])
        session['amount'] = amount  # Store amount in the session
        add_log(date, amount)  # Add log entry
        return redirect(url_for('menu'))  # Redirect to the menu page
    return render_template('add_daily_log.html')  # Render 'add_daily_log.html' form

# Route for viewing daily water intake
@app.route('/view_daily_intake')
def view_daily_intake():
    return render_template('view_daily_intake.html', data=data)  # Render 'view_daily_intake.html'

# Route for setting daily water intake target
@app.route('/set_daily_target', methods=['GET', 'POST'])
def set_daily_target():
    amount = session.get('amount', 0)
    if request.method == 'POST':
        global daily_target
        daily_target = float(request.form['daily_target'])  # Set daily water intake target
        return redirect(url_for('menu'))  # Redirect to the menu page
    return render_template('set_daily_target.html', daily_target=daily_target, amount=amount)

# Route for displaying monthly average water intake
@app.route('/monthly_avg_intake', methods=['GET', 'POST'])
def monthly_avg_intake():
    average_monthly_intake = calculate_average_monthly_intake()  # Calculate average monthly intake
    return render_template('monthly_avg_intake.html', average_monthly_intake=average_monthly_intake)  # Render 'monthly_avg_intake.html'

# Route for deleting a log entry
@app.route('/delete_log', methods=['GET', 'POST'])
def delete_log():
    date = request.form.get('date')
    if date:
        delete_log_entry(date)  # Delete log entry for the given date
        return redirect(url_for('menu'))  # Redirect to the menu page
    return render_template('delete_log.html')  # Render 'delete_log.html'

# Route for generating and displaying a water intake plot
@app.route('/plot_water_intake', methods=['GET', 'POST'])
def plot_water_intake():
    generate_plot()  # Generate the plot for water intake
    return render_template('plot_graph.html', graph_image='static/Figure 1.png')  # Render 'plot_graph.html' with the generated image

# Route for exiting the application
@app.route('/exit_app', methods=['GET', 'POST'])
def exit_app():
    if request.method == 'POST':
        save_data()  # Save data before exiting the app
        flash("Data has been saved. Exiting the app.")  # Flash a message
    return render_template('maini.html')  # Render 'maini.html'



# Function to suggest a random exercise from the provided file
def random_exercise(filename):
    exercise_data = {}

    # Read data from the provided file and generate exercise dictionary
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip().split(",")
            exercise = line[0]
            video = line[1]
            exercise_data[exercise] = video

    # Choose a random exercise and return a recommendation message
    key, value = random.choice(list(exercise_data.items()))
    return "Try this exercise: " + key + ". Watch the video: " + value


# Function to log exercise details to a workout log file
def log_exercise(exercises, exercise, duration, sets, reps):
    current_date = date.today()

    # Construct exercise details
    ex = {
        "Exercise": exercise,
        "Duration": duration,
        "Sets": sets,
        "Reps per set": reps,
        "Date": current_date
    }

    # Append exercise details to the workout log file
    with open("workout_log.txt", "a") as exercises:
        for a, b in ex.items():
            exercises.write(f"{a}:{b}\n")
        exercises.write("\n")

    print("Exercise logged successfully")


# Function to view workout history from a specified file
def view_workout_history(filename):
    workout_history = []

    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            workout_history.append(line)

    return workout_history


# Function to get or create a file for existing history
def existing_history(filename):
    with open(filename, "a") as file:
        return file


# Function to load users' data from a JSON file
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# Function to save users' data to a JSON file
def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)


# Route to display workout videos
@app.route('/video.html')
def video():
    search_query = 'workout for beginners'
    videos = search_youtube(search_query)
    return render_template('video.html', videos=videos)


# Route to display healthy recipe videos
@app.route('/recipe.html')
def recipe():
    search_query = 'healthy diet recipes'
    videos = search_youtube1(search_query)
    return render_template('recipe.html', videos=videos)
# Function to calculate BMI
def calculate_bmi(weight, height):
    """
    Formula: BMI = weight (kg) / (height (m) * height (m))
    """
    bmi = weight / (height ** 2)
    return bmi

# Function to interpret BMI values and classify them into categories
def interpret_bmi(bmi):
    """
    Interpreting the BMI values and classify it into 3 categories: Underweight, Normal weight, Overweight, Obese
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Route to calculate BMI
@app.route('/bmi.html', methods=['POST', 'GET'])
def bmi():
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height_unit = request.form['height_unit']

        if height_unit == 'f':  # If height is in feet and inches
            feet = int(request.form['feet'])
            inches = float(request.form['inches'])
            height_meters = (feet * 0.3048) + (inches * 0.0254)
        elif height_unit == 'c':  # If height is in centimeters
            height_cm = float(request.form['height_cm'])
            height_meters = height_cm / 100
        else:
            return 'Invalid input for height unit'  # Return an error for an invalid height unit

        bmi = calculate_bmi(weight, height_meters)  # Calculate BMI
        interpretation = interpret_bmi(bmi)  # Interpret BMI value

        # Saving name and BMI information to a file (You can modify this part as needed)
        with open("bmi_records.txt", "a") as file:
            file.write(f"Name: {name}, BMI: {bmi:.2f}, Classification: {interpretation}\n")

        # Render the result template with name, BMI, and classification
        return render_template('result.html', name=name, bmi=bmi, classification=interpretation)
    else:
        return render_template('bmi.html')  # Render the BMI calculator form

# This code segment is for a Flask application that calculates BMI based on user input.


    

# Function to fetch weather data
def weather():
    api_keykp = 'adaea03744a19d0a552faaba674e52bc'
    city = 'Ahmedabad'
    country_code = 'India'
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': f'{city},{country_code}',
        'appid': api_keykp,
        'units': 'metric'  
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    description = weather_data['weather'][0]['description']
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    return description, temperature, humidity

# Route for the root URL
@app.route('/')
def index():
    # Fetch weather data
    description, temperature, humidity = weather()
    
    # Extract headlines and links from the Indian Express Lifestyle/Fitness section
    url = "https://indianexpress.com/section/lifestyle/fitness/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    d = soup.find_all('div', class_="img-context")
    count = 0
    headline_dict = {}
    
    # Extract headlines and links, limit to 10
    try:
        for i in d:
            headline = i.find('h2', class_='title')
            link = i.find('a')
            if headline and link:
                text = link['title']
                links = link['href']
                headline_dict[text] = links
                count += 1
                if count == 10:
                    break
    except Exception as e:
        print(e)
        
    # Render the 'land.html' template with extracted data and weather information
    return render_template('land.html', dict=headline_dict, description=description, temperature=temperature, humidity=humidity)

# Route for 'index.html'
@app.route('/index.html')
def mai():
    return render_template('index.html')

# Route for 'maini.html'
@app.route('/maini.html')
def m():
    return render_template('maini.html')

# Route for 'chat.html'
@app.route('/chat.html')
def chat():
    return render_template('chat.html')

# Route for processing user input and generating bot response
@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.form["user_input"]
    response = bot.respond(user_input)  # Assuming 'bot' is an instance of a chatbot
    return jsonify({"response": response})

# Function to hash passwords using SHA-256 algorithm
def hashpassword(password):
    m = hashlib.sha256(password.encode("UTF-8"))
    return m.hexdigest()


# Route for user signup
@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    users = load_users()  # Load existing user data

    # Check if username already exists
    if username in users:
        return "Username already exists!"

    # Add new user to the user dictionary
    users[username] = hashpassword(password)
    save_users(users)  # Save updated user data
    return redirect(url_for('index'))  # Redirect to the index page

# Route for user sign-in
@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    users = load_users()  # Load existing user data

    # Check if the username exists and the password is correct
    if username in users and users[username] == hashpassword(password):
        return render_template("maini.html")  # Render the maini.html page (on successful sign-in)
    else:
        return "Invalid username or password"  # Return an error message for unsuccessful sign-in

# Route for project selection after sign-in
@app.route('/project',methods=['POST'])
def mainii():
    choice1 = request.form["c1"]
    log_form = "log_form1"
    if choice1 == "Workout_log":

        return render_template("c1.html",log_form = log_form,workout_history = workout_history)
    elif choice1 == "calorie tracker":
        return render_template("calorie.html")
    elif choice1 == "water_intake":
        return render_template("menu.html")
    elif choice1 == "chatbot":
        return render_template("chat.html")
    elif choice1 == "bmi":
        return render_template("bmi.html")



# Route for handling submission from a form (Choice)
@app.route('/submit4', methods=['POST'])
def submit():
    random_ex = ""  # Initialize an empty string for a random exercise
    workout_history = ""  # Initialize an empty string for workout history
    choice = request.form["choice"]

    # Handling different choices from the form
    if choice == "Record Your Workout":
        log_form = "log_form2"
        return render_template("c1.html", log_form=log_form, workout_history=workout_history)
    elif choice == "Discover a Random Exercise":
        random_ex = random_exercise("exercise_video.txt")
        return render_template("c1.html", random_ex=random_ex, log_form="log_form1", workout_history=workout_history)
    elif choice == "Check Workout History":
        workout_history = view_workout_history("workout_log.txt")
        return render_template("c1.html", workout_history=workout_history, log_form="log_form1")
    elif choice == "Exit":
        return "YOU EXITED"

# Route to handle submission of exercise logs
@app.route('/submit1', methods=['POST'])
def submit1():
    exercises = existing_history("workout_log.txt")
    exercise = request.form["exercise"]
    duration = float(request.form["duration"])
    sets = int(request.form["sets"])
    reps = int(request.form["reps"])
    log_exercise(exercises, exercise, duration, sets, reps)
    log_form = "log_form1"
    return render_template("c1.html", log_form=log_form)

# Global variables for calorie tracking
num_days = 0
cal_data = []
plot_filename = '1.png'

# Route for calorie tracking page
@app.route('/calorie')
def cal():
    return render_template("calorie.html")

# Route for adding calorie data
@app.route('/add_calorie', methods=['POST'])
def add_calorie():
    global num_days
    global cal_data
    
    cal = int(request.form['calories'])
    num_days += 1
    cal_data.append(cal)
    
    return render_template("calorie.html")

# Route for 'steps.html'
@app.route('/steps.html')
def st():
    return render_template('steps.html')

# Route for plotting calorie data
@app.route('/plot_calorie')
def plot_calorie():
    if num_days == 0:
        return "No data available. Add some data first."
    
    # Plotting calorie intake data and saving the plot as an image file
    day = np.arange(1, num_days + 1)
    calories_data = np.array(cal_data)
    plt.plot(day, calories_data)
    plt.xlabel("Day")
    plt.ylabel("Calories Intake (CAL)")
    plt.title("Calorie Tracker")
    plt.savefig(os.path.join('static', plot_filename))  # Save plot image in the 'static' directory
    plt.close()  # Close the plot
    
    return render_template('plot.html', plot_filename=plot_filename)  # Render the plot.html template

# Function to send weekly emails to subscribers
def send_weekly():
    # Schedule to send emails every day at a specific time
    schedule.every().day.at("11:12").do(send_email_to_subscribers)
    
    while True:
        schedule.run_pending()  # Execute pending scheduled tasks
        time.sleep(1)  # Wait for 1 second before checking again



# ser = serial.Serial('COM9', 9600)  
# data = ""

# def read_from_port(ser):
#     global data
#     while True:
#         reading = ser.readline().decode()
#         if reading:
#             data = reading.strip()
#             socketio.emit('arduinoData', {'data': data}, namespace='/test')

# @socketio.on('connect', namespace='/test')
# def test_connect():
#     print('Client connected')
#     emit('arduinoData', {'data': data})

if __name__ == '__main__':
    import threading
    schedule_thread = threading.Thread(target=send_weekly)
    schedule_thread.start()
    app.run(debug=True)

    # thread = threading.Thread(target=read_from_port, args=(ser,))
    # thread.daemon = True
    # thread.start()
    # socketio.run(app)