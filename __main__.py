from flask import Flask, render_template, request, session

from database import link_sql

app = Flask(__name__, template_folder='./templates')
app.secret_key = '12345678'


@app.route('/')
def index():
    selected_region = session.get('selected_region', '台北市')
    db, cursor = link_sql()

    results = {}

    sql = f"SELECT * FROM `post` " \
          f"NATURAL JOIN `payment` " \
          f"WHERE `city` = '{selected_region}' " \
          f"ORDER BY `class` LIMIT 8"
    cursor.execute(sql)

    results[0] = cursor.fetchall()

    db.close()

    return render_template(
        'index.html',
        selected_region=selected_region,
        recomment_post=results[0]
    )


@app.route('/update', methods=['POST'])
def update():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'susses'


if __name__ == '__main__':
    app.run(debug=True)
