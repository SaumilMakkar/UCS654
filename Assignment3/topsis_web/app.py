"""
TOPSIS Web Service
Flask application for TOPSIS analysis with email results
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import csv
import math
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Email configuration (Update with your SMTP details)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "saumilmakkar@gmail.com"  # Change this
SENDER_PASSWORD = "hlhz gmzv rtrv imqt"   # Change this (use App Password for Gmail)


def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_file(filename):
    """Check if file is CSV"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


def read_csv_file(filepath):
    """Read and parse CSV file"""
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if any(cell.strip() for cell in row)]
    
    if len(rows) < 2:
        raise ValueError("CSV file must have a header and at least one data row")
    
    return rows[0], rows[1:]


def validate_csv_data(header, data_rows):
    """Validate CSV structure and data"""
    if len(header) < 3:
        raise ValueError("CSV must have at least 3 columns (1 name + 2 criteria)")
    
    for r_idx, row in enumerate(data_rows, start=2):
        if len(row) != len(header):
            raise ValueError(f"Row {r_idx} has {len(row)} columns, expected {len(header)}")
        
        for c_idx in range(1, len(row)):
            try:
                float(row[c_idx])
            except ValueError:
                raise ValueError(f"Non-numeric value '{row[c_idx]}' in row {r_idx}, column {c_idx+1}")


def parse_weights(weight_str, n_criteria):
    """Parse and validate weights"""
    parts = [w.strip() for w in weight_str.split(",")]
    
    if len(parts) != n_criteria:
        raise ValueError(
            f"Number of weights ({len(parts)}) doesn't match criteria columns ({n_criteria}). "
            f"Your CSV has {n_criteria} criteria — please provide exactly {n_criteria} comma-separated weights (e.g. 1,1,1,1,1)."
        )
    
    weights = []
    for p in parts:
        try:
            weights.append(float(p))
        except ValueError:
            raise ValueError(f"Invalid weight '{p}'. Weights must be numeric")
    
    return weights



def parse_impacts(impact_str, n_criteria):
    """Parse and validate impacts"""
    parts = [i.strip() for i in impact_str.split(",")]
    
    if len(parts) != n_criteria:
        raise ValueError(
            f"Number of impacts ({len(parts)}) doesn't match criteria columns ({n_criteria}). "
            f"Your CSV has {n_criteria} criteria — please provide exactly {n_criteria} comma-separated impacts (e.g. +,+,+,-,+)."
        )
    
    for p in parts:
        if p not in ("+", "-"):
            raise ValueError(f"Invalid impact '{p}'. Must be '+' or '-'")
    
    return parts


def topsis(matrix, weights, impacts):
    """Perform TOPSIS analysis"""
    rows = len(matrix)
    cols = len(matrix[0])
    
    # Normalization
    norm = [[0.0] * cols for _ in range(rows)]
    for j in range(cols):
        denom = math.sqrt(sum(matrix[i][j]**2 for i in range(rows)))
        for i in range(rows):
            norm[i][j] = matrix[i][j] / denom if denom != 0 else 0.0
    
    # Weighted normalization
    v = [[norm[i][j] * weights[j] for j in range(cols)] for i in range(rows)]
    
    # Ideal solutions
    a_pos, a_neg = [0.0] * cols, [0.0] * cols
    for j in range(cols):
        col = [v[i][j] for i in range(rows)]
        if impacts[j] == "+":
            a_pos[j], a_neg[j] = max(col), min(col)
        else:
            a_pos[j], a_neg[j] = min(col), max(col)
    
    # Distances
    s_pos = [math.sqrt(sum((v[i][j] - a_pos[j])**2 for j in range(cols))) for i in range(rows)]
    s_neg = [math.sqrt(sum((v[i][j] - a_neg[j])**2 for j in range(cols))) for i in range(rows)]
    
    # Scores
    scores = []
    for i in range(rows):
        total = s_pos[i] + s_neg[i]
        scores.append(round((s_neg[i] / total) * 100, 2) if total != 0 else 0.0)
    
    # Ranks
    sorted_idx = sorted(range(rows), key=lambda i: scores[i], reverse=True)
    ranks = [0] * rows
    for rank_val, idx in enumerate(sorted_idx, start=1):
        ranks[idx] = rank_val
    
    return scores, ranks


def write_result_csv(header, names, matrix, scores, ranks, output_path):
    """Write TOPSIS results to CSV"""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(list(header) + ["Topsis Score", "Rank"])
        for i in range(len(names)):
            writer.writerow([names[i]] + matrix[i] + [scores[i], ranks[i]])


def send_email(recipient_email, result_file):
    """Send result file via email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "TOPSIS Analysis Results"
        
        body = """
        Hello,
        
        Your TOPSIS analysis has been completed successfully.
        
        Please find the results attached to this email.
        
        Thank you for using our TOPSIS Web Service!
        
        Best regards,
        TOPSIS Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach result file
        with open(result_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(result_file)}")
        msg.attach(part)
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, recipient_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False


@app.route('/')
def index():
    """Home page with form"""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Process TOPSIS analysis"""
    try:
        # Get form data
        file = request.files.get('file')
        weights_str = request.form.get('weights', '').strip()
        impacts_str = request.form.get('impacts', '').strip()
        email = request.form.get('email', '').strip()
        
        # Validate inputs
        if not file or file.filename == '':
            flash('Please select a CSV file', 'error')
            return redirect(url_for('index'))
        
        if not validate_file(file.filename):
            flash('File must be a CSV file', 'error')
            return redirect(url_for('index'))
        
        if not weights_str:
            flash('Please enter weights', 'error')
            return redirect(url_for('index'))
        
        if not impacts_str:
            flash('Please enter impacts', 'error')
            return redirect(url_for('index'))
        
        if not email:
            flash('Please enter email address', 'error')
            return redirect(url_for('index'))
        
        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        
        # Read and validate CSV
        header, data_rows = read_csv_file(input_path)
        validate_csv_data(header, data_rows)
        
        n_criteria = len(header) - 1
        
        # Parse weights and impacts
        weights = parse_weights(weights_str, n_criteria)
        impacts = parse_impacts(impacts_str, n_criteria)
        
        # Check if weights and impacts count match
        if len(weights) != len(impacts):
            flash('Number of weights must equal number of impacts', 'error')
            return redirect(url_for('index'))
        
        # Extract data
        names = [row[0].strip() for row in data_rows]
        matrix = [[float(row[c]) for c in range(1, len(row))] for row in data_rows]
        
        # Run TOPSIS
        scores, ranks = topsis(matrix, weights, impacts)
        
        # Write results
        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        write_result_csv(header, names, matrix, scores, ranks, result_path)
        
        # Send email
        email_sent = send_email(email, result_path)
        
        if email_sent:
            flash(f'Analysis completed! Results sent to {email}', 'success')
        else:
            flash('Analysis completed but email failed to send. Please check email configuration.', 'warning')
        
        # Clean up uploaded file
        os.remove(input_path)
        
        return redirect(url_for('index'))
        
    except ValueError as e:
        flash(f'Validation Error: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
