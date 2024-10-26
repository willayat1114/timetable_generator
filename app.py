# app.py
from flask import Flask, render_template, request, jsonify
from datetime import timedelta
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    try:
        num_sections = int(data['num_sections'])
        num_classes = int(data['num_classes'])
        time_per_class = int(data['time_per_class'])
        lunch_break = int(data['lunch_break'])
        start_time = data['start_time']
        subjects = data['subjects']

        timetable = {f"Section {chr(65 + section)}": [] for section in range(num_sections)}
        current_time = timedelta(hours=int(start_time.split(':')[0]), minutes=int(start_time.split(':')[1]))

        for i in range(num_classes):
            if i == num_classes - 3:  # Add lunch break before the third last class
                end_time = current_time + timedelta(minutes=lunch_break)
                for section in range(num_sections):
                    timetable[f"Section {chr(65 + section)}"].append(f"{current_time} - {end_time}: Lunch Break")
                current_time = end_time

            end_time = current_time + timedelta(minutes=time_per_class)
            available_subjects = subjects[:]
            for section in range(num_sections):
                if not available_subjects:
                    available_subjects = subjects[:]
                subject = random.choice(available_subjects)
                available_subjects.remove(subject)
                timetable[f"Section {chr(65 + section)}"].append(f"{current_time} - {end_time}: {subject}")
            current_time = end_time

        return jsonify(timetable)
    except (ValueError, KeyError) as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)