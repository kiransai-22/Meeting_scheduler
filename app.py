from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta

app = Flask(__name__)
meetings = []

@app.route('/')
def index():
    return render_template('index.html', meetings=meetings)

@app.route('/schedule', methods=['POST'])
def schedule():
    title = request.form.get('title')
    date = request.form.get('date')
    time = request.form.get('time')
    reminder_minutes = int(request.form.get('reminder'))

    meeting_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
    reminder_time = meeting_datetime - timedelta(minutes=reminder_minutes)

    meetings.append({
        'id': len(meetings),
        'title': title,
        'datetime': meeting_datetime.strftime('%Y-%m-%d %H:%M'),
        'reminder': reminder_time.strftime('%Y-%m-%d %H:%M')
    })
    return redirect(url_for('index'))

@app.route('/edit/<int:meeting_id>', methods=['GET', 'POST'])
def edit(meeting_id):
    meeting = next((m for m in meetings if m['id'] == meeting_id), None)
    if request.method == 'POST':
        meeting['title'] = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        reminder_minutes = int(request.form.get('reminder'))

        meeting_datetime = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        reminder_time = meeting_datetime - timedelta(minutes=reminder_minutes)

        meeting['datetime'] = meeting_datetime.strftime('%Y-%m-%d %H:%M')
        meeting['reminder'] = reminder_time.strftime('%Y-%m-%d %H:%M')
        return redirect(url_for('index'))
    return render_template('edit.html', meeting=meeting)

@app.route('/delete/<int:meeting_id>')
def delete(meeting_id):
    global meetings
    meetings = [m for m in meetings if m['id'] != meeting_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
