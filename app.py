import csv
from datetime import datetime

import humanize
from flask import Flask, render_template

from env import HOST, PORT, DEBUG

app = Flask(__name__)


@app.route('/')
def index():
    stories = {}
    with open('data/top.csv') as file:
        reader = csv.DictReader(file)
        items = []
        for item in list(reader):
            time = int(item.pop('time'))
            ago_time = humanize.naturaltime(datetime.utcnow() - datetime.utcfromtimestamp(time))
            item['time'] = ago_time
            item['hn_url'] = f'https://news.ycombinator.com/item?id={item["id"]}'
            item['user_url'] = f'https://news.ycombinator.com/user?id={item["by"]}'
            items.append(item)
        stories['Top'] = items

    return render_template('index.html', stories=stories)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=DEBUG)
