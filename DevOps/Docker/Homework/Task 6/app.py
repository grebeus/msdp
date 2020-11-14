from flask import Flask
from redis import Redis

app = Flask(__name__)
db = Redis(host="redis")
@app.route("/")

def hello():
    visitCounter = db.incr('visitsCounter')
    html = "<H1> Hello!!! </H1>" \
        "<b>Visits: </b>{visits}" \
        "</br>"
    return html.format(visits=visitCounter)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80)