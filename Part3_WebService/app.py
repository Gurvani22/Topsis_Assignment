from flask import Flask, render_template, request
import os
import re
from topsis import topsis
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    file = request.files['file']
    weights = request.form['weights']
    impacts = request.form['impacts']
    email = request.form['email']

    # Email validation
    if not valid_email(email):
        return "Invalid Email Format"

    weights = weights.split(',')
    impacts = impacts.split(',')

    # Validate weights and impacts length
    if len(weights) != len(impacts):
        return "Number of weights must equal number of impacts"

    # Validate impacts symbols
    if not all(i in ['+', '-'] for i in impacts):
        return "Impacts must be + or -"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    output_file = "result.csv"

    # Run TOPSIS
    topsis(filepath, weights, impacts, output_file)

    # Send email
    msg = EmailMessage()
    msg['Subject'] = "TOPSIS Result"
    msg['From'] = "your_email@gmail.com"
    msg['To'] = email
    msg.set_content("Attached is your TOPSIS result file.")

    with open(output_file, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application',
                           subtype='octet-stream',
                           filename=output_file)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login("gurvani2205@gmail.com", "gmqtdakpombhtryq")
        smtp.send_message(msg)

    return "Result sent to your email!"

if __name__ == '__main__':
    app.run(debug=True)
