# !/usr/bin/python3
# security testing app with input field and display http requests count + /
# reset button to reset the counter + /
# download button to download last 1 hour http requests along with response

from flask import Flask, request, render_template
import logging
import datetime as dt
import pandas as pd

logging.basicConfig(filename="app.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(threadName)s : %(message)s")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    increment_counter()
    code = 200
    text_date = request.form.get('payload')
    app.logger.info('payload submitted_' + str(request.method) + "_" + str(text_date) + "_" + str(code))
    log_request(request.method, text_date, code)

    if request.method == 'POST' and request.form.get('reset'):
        app.logger.info('reset submitted_' + str(request.method) + "_" + str(code))
        log_request(request.method, 'reset', code)
        reset_counter()

    return render_template('index.html', counter=counter)

counter = 0

def increment_counter():
    global counter
    counter += 1

def reset_counter():
    global counter
    counter = 0
    with open("payload.txt", "w") as f:
        f.write("")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    code = 404
    app.logger.info('url submitted_' + str(request.method) + "_" + str(request.path) + "_" + str(code))
    log_request(request.method, request.path, code)
    return render_template('404.html'), 404

def log_request(method, data, code):
    now = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    payload = str(data)
    code = str(code)
    with open('payload.txt', 'a') as f:
        f.write(f'{now},{method},{payload}, {code}\n')


@app.route('/info')
def info():
    # Load the data into a dataframe
    df = pd.read_csv('payload.txt', header=None, names=['timestamp', 'method', 'payload', 'status'])

    # Convert the timestamp column to a datetime object
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filter the data for the last 1 day
    now = dt.datetime.now()
    one_day_ago = now - dt.timedelta(days=1)
    df = df[(df['timestamp'] >= one_day_ago) & (df['timestamp'] <= now)]

    # Group the data by method, payload, and status
    grouped = df.groupby(['method', 'payload', 'status']).count()

    # Reset the index to make the grouped data a flat dataframe
    grouped = grouped.reset_index()

    # Pass the grouped data to the template to display in a table
    return render_template('info.html', data=grouped.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
