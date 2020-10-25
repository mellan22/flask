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
    osechi_count = OsechiWishes.query.filter(OsechiWishes.id < 14).count()
    return render_template('start.html', title='start game', osechi_count=osechi_count)


@app.route('/start_game', methods=["post"])
def start_game():
    return question()


@app.route('/question')
def question():
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


@app.route('/setting')
def setting_mode():
    return render_template('setting.html', title='setting')


@app.route('/setting', methods=["post"])
def setting():
    primary_data = [
        ['チョロギ', 'チョロギは漢字で「長老喜」や「長老貴」と書きます。この漢字が長寿に縁起が良いとされ、おせち料理の食材として用いられるようになりました。',
            '/static/images/osechi_chorogi.png', '最近、不老長寿を意識している'],
        ['伊達巻', '伊達巻の名前の由来は、長崎から江戸に伝わった「カステラ蒲鉾」が、伊達者（シャレ者）たちの着物に似ていたからと言われています。',
            '/static/images/osechi_datemaki.png', '来年は本をたくさん読むことが目標だ'],
        ['海老', 'えびは、長いひげをはやし、腰が曲がるまで長生きすることを願っておせち料理に使われます。',
            '/static/images/osechi_ebi.png', 'できれば腰が曲がるまで長生きしたい'],
        ['海老芋', '海老芋は、親芋の周りに子いもができ、その子いもからさらに孫いもができます。このように親・子・孫と増え続けていくので、子孫繁栄の象徴として、縁起の良い食材だと言われています。',
            '/static/images/osechi_ebiimo.png', '来年も家族仲良く暮らしたい'],
        ['かまぼこ', '蒲鉾は「日の出」を象徴するものとして、元旦にはなくてはならない料理です。紅はめでたさと慶びを、白は神聖を表します。',
            '/static/images/osechi_kamaboko.png', 'できれば来年は初日の出がみたい'],
        ['数の子', '数の子はニシンの卵。二親(にしん)から多くの子が出るのでめでたいと、子孫繁栄を祈っていただきます。',
         '/static/images/osechi_kazunoko.png', '来年は子宝に恵まれたい'],
        ['昆布巻き', '昆布は「喜ぶ」の言葉にかけて、正月の鏡飾りにも用いられている一家発展の縁起ものです。',
            '/static/images/osechi_kobumaki.png', '最近喜ばしいことが少ない気がする'],
        ['栗きんとん', 'きんとんは「金団」と書き、「金色の団子」もしくは「金色の布団」という意味があります。また「勝ち栗」とも言われるように、武家社会では戦の勝機を高めるための縁起物として重宝されたという経緯があります。',
            '/static/images/osechi_kurikinton.png', 'お金をもっとたくさん稼ぎたい'],
        ['黒豆', '「まめ」は元来、丈夫・健康を意味する言葉です。「まめに働く」との語呂合わせから、元気に働けるようにとの願いが込められています。',
            '/static/images/osechi_kuromame.png', '来年もとにかく元気に働きたい'],
        ['なます', '紅白の色がおめでたい紅白なます。消化に良い栄養素を含み、さっぱりした味わいはお正月料理中の箸休めにぴったりです。',
            '/static/images/osechi_namasu.png', '胃もたれしやすいほうだ'],
        ['田作り', 'イワシを田んぼの肥料にしたところ大変豊作になり、五万俵もの米が収穫できたことから、田を作ることにちなみ「田作り」と呼ばれるようになりました。「五穀豊穣」の象徴です。',
            '/static/images/osechi_tadukuri.png', '来年は農業に挑戦したい！'],
        ['たたきごぼう', '細く長く地中にしっかり根を張るごぼうは、家の基礎が堅牢であることを願う縁起のよい食材として様々に使われています。',
            '/static/images/osechi_tatakigobou.png', 'そろそろ家を建てようと考えている'],
        ['ゆりね', 'ゆりねは鱗茎が花びらのように重なり合っていることから「歳を重ねる」あるいは「和合（仲が良いこと）」に通じるとされ、吉祥の象徴とされています。',
            '/static/images/osechi_yurine.png', '周りの人々ともっと仲良くなりたい']
    ]
    for i in primary_data:
        content = OsechiWishes(i[0], i[1], i[2], i[3], 0)
        db_session.add(content)
    db_session.commit()
    return question()


if __name__ == "__main__":
    app.run(debug=True)
