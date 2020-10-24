from flask import Flask, render_template, request, url_for
from models.models import OsechiWishes

from models.database import db_session


app = Flask(__name__)


# @app.route('/')
# def hello():
#     name = "Hello World"
#     return name

@app.route('/')
@app.route('/start')
def start():
    name = "start"
    return render_template('start.html', title='start game', name=name)


@app.route('/start_game', methods=["post"])
def start_game():
    return question()


@app.route('/question')
def question():
    osechi = ''
    osechi = OsechiWishes.query.filter(OsechiWishes.want == 0).first()
    return render_template('questions.html', title='question', osechi=osechi)


@app.route('/answer', methods=["post"])
def post():
    answer = request.form["answer"]
    id = request.form['id']
    update_status = OsechiWishes.query.filter(OsechiWishes.id == id).first()
    update_status.want = 1 if answer == 'yes' else 2
    db_session.add(update_status)
    db_session.commit()
    return question()


@app.route('/end', methods=["post"])
def end():
    selected_osechi = OsechiWishes.query.filter(OsechiWishes.want == 1).all()
    return render_template('end.html', title='end game', selected_osechi=selected_osechi)


@app.route('/reset', methods=["post"])
def reset():
    selected_osechi = OsechiWishes.query.filter(OsechiWishes.want != 0).all()
    for i in selected_osechi:
        i.want = 0
        db_session.add(i)
    db_session.commit()
    return start()

# @app.route('/detail', methods=["post"])
# def detail():
#     OsechiWishes.query.filter(OsechiWishes.want != 0).query.update(
#         {OsechiWishes.want: 0})
#     return render_template('questions.html', title='question')


if __name__ == "__main__":
    app.run(debug=True)
