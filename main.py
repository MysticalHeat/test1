import workdb
from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)
database = workdb.SelectDatabase()


def do_none(req):
    if not req:
        return None
    else:
        return req


def last_time(lasttime):
    if lasttime == 1:
        return datetime.now() - timedelta(minutes=10)
    if lasttime == 2:
        return datetime.now() - timedelta(minutes=30)
    if lasttime == 3:
        return datetime.now() - timedelta(hours=1)
    if lasttime == 4:
        return datetime.now() - timedelta(days=1)
    if lasttime == 5:
        return datetime.now() - timedelta(days=30)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST" and 'validate' not in request.form:
        time0 = do_none(request.form['time0'])
        time1 = do_none(request.form['time1'])
        source_id0 = do_none(request.form['source_id0'])
        source_id1 = do_none(request.form['source_id1'])
        priority = do_none(request.form['priority'])
        weight0 = do_none(request.form['weight0'])
        weight1 = do_none(request.form['weight1'])
        keyword = do_none(request.form['keyword'])
        if 'lasttime' in request.form:
            lasttime = do_none(request.form['lasttime'])
            time0 = last_time(int(lasttime))
            time1 = datetime.now()
        if source_id1 and source_id0 is None:
            source_id0 = 0
        if source_id0 and source_id1 is None:
            source_id1 = 999
        if weight1 and weight0 is None:
            weight0 = 0
        if weight0 and weight1 is None:
            weight1 = 999
        if time1 and time0 is None:
            time0 = '1970-01-01 00:00:00'
        if time0 and time1 is None:
            time1 = datetime.now()
        result = database.get_info(
            time=[time0, time1],
            source_id=[source_id0, source_id1],
            priority=priority,
            weight=[weight0, weight1],
            keyword=keyword
        )
        return jsonify({
            'data': render_template('the_temp.html', result=result),
            'resp_count': len(result),
            'db_count': database.get_count()}
        )
    elif 'validate' in request.form:
        return jsonify({'data': render_template('the_temp.html')})
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
