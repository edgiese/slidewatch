import flask
import state
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    with open('index.html', 'r') as file:
        data = file.read()
    return data


@app.route('/poll_state')
def poll_state():
    return state.get_current()


@app.route('/slide/<int:slide_num>', methods=['GET'])
def set_slide(slide_num):
    print(slide_num)
    state.set_slide(slide_num)
    return "<p>processed %d</p>" % slide_num

def init():
    with open('2020-12-19.json') as f:
        data = json.load(f)
    state.init(data)

init()
app.run(host='0.0.0.0')
