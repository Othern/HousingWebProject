from flask import Flask, render_template, request, session, redirect, url_for
from flask_login import logout_user, LoginManager, login_user, login_required, UserMixin

from database import link_sql

app = Flask(__name__, template_folder='./templates')
app.secret_key = '12345678'

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, user_id, email, permission):
        self.id = user_id
        self.email = email
        self.permission = permission

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    db, cursor = link_sql()

    cursor.execute(f"SELECT * FROM `user` WHERE `uId` = {user_id}")
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user:
        return None

    user = User(user['id'], user['email'], user['permission'])
    return user


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
          f"NATURAL JOIN `housesell` " \
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


# 登入的 API
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # 驗證使用者資訊
    db, cursor = link_sql()
    cursor.execute(f"SELECT * FROM `user` "
                   f"WHERE email = '{email}'")
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user is None:
        return '該用戶不存在，請註冊'

    if user['password'] != password:
        return '密碼錯誤，請檢查你的密碼'

    # 如果驗證成功，使用 login_user 函數登入使用者
    user = User(user['uId'], user['email'], user['permission'])
    login_user(user)
    return '成功登入'


# 登出的 API
@app.route('/logout')
@login_required
def logout():
    # 使用 logout_user 函數登出使用者
    logout_user()
    return redirect(url_for(''))


if __name__ == '__main__':
    app.run(debug=True)
