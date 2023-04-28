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

    # For recommend.html
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

    # For family.html
    sql = f"SELECT `pId`, `address`, `district`, " \
          f"       `type`, `twPing`, `image`," \
          f"       `housesell`.`price` as `sellPrice` " \
          f"FROM `post` " \
          f"NATURAL JOIN `payment` " \
          f"NATURAL JOIN `house` " \
          f"NATURAL JOIN `image` " \
          f"NATURAL JOIN `housesell` "  \
          f"WHERE `city` = '{selected_region}' " \
          f"ORDER BY `class` DESC " \
          f"LIMIT 8 "

    cursor.execute(sql)

    results[1] = cursor.fetchall()

    # For suite.html
    sql = f"SELECT `pId`, `address`, `district`, " \
          f"       `type`, `twPing`, `image`," \
          f"       `houserent`.`price` as `rentPrice` " \
          f"FROM `post` " \
          f"NATURAL JOIN `payment` " \
          f"NATURAL JOIN `house` " \
          f"NATURAL JOIN `image` " \
          f"NATURAL JOIN `houserent` " \
          f"WHERE `city` = '{selected_region}' AND" \
          f"      `type` = '獨立套房'" \
          f"ORDER BY `class` DESC " \
          f"LIMIT 8 "

    cursor.execute(sql)

    results[2] = cursor.fetchall()

    # For suite.html
    sql = f"SELECT `pId`, `address`, `district`, " \
          f"       `type`, `twPing`, `image`," \
          f"       `houserent`.`price` as `rentPrice` " \
          f"FROM `post` " \
          f"NATURAL JOIN `payment` " \
          f"NATURAL JOIN `house` " \
          f"NATURAL JOIN `image` " \
          f"NATURAL JOIN `houserent` " \
          f"WHERE `city` = '{selected_region}' AND" \
          f"      `type` IN ('分租套房', '雅房')" \
          f"ORDER BY `class` DESC " \
          f"LIMIT 8 "

    cursor.execute(sql)

    results[3] = cursor.fetchall()

    db.close()

    return render_template(
        'index.html',
        selected_region=selected_region,
        recommend_post=results[0],
        family_post=results[1],
        suite_post=results[2],
        shared_post=results[3]
    )


@app.route('/update/region', methods=['POST'])
def update():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'susses'


if __name__ == '__main__':
    app.run(debug=True)
