import pandas as pd
from flask import Flask, render_template, request, session

from database import link_sql

app = Flask(__name__, template_folder='./templates')
app.secret_key = '12345678'


@app.route('/')
def index():
    selected_region = session.get('selected_region', '台北市')
    db, cursor = link_sql()

    results = {}

    sql = f"SELECT `pId`, `address`, `district`, " \
          f"       `type`, `twPing`, `image`," \
          f"       `housesell`.`price` as `sellPrice`, " \
          f"       `houserent`.`price` as `rentPrice` " \
          f"FROM `post` " \
          f"NATURAL JOIN `payment` " \
          f"NATURAL JOIN `house` " \
          f"NATURAL JOIN `image` " \
          f"LEFT OUTER JOIN `housesell` " \
          f"             ON `house`.`hId` = `housesell`.`hid`" \
          f"LEFT OUTER JOIN `houserent` " \
          f"             ON `house`.`hId` = `houserent`.`hid`" \
          f"WHERE `city` = '{selected_region}' " \
          f"ORDER BY `class` DESC " \
          f"LIMIT 8 "

    cursor.execute(sql)

    results[0] = cursor.fetchall()

    db.close()

    print(pd.DataFrame(results[0]).columns)

    return render_template(
        'index.html',
        selected_region=selected_region,
        recommend_post=results[0]
    )


@app.route('/update/region', methods=['POST'])
def update():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'susses'


if __name__ == '__main__':
    app.run(debug=True)
