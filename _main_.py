
import pandas as pd
from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_login import logout_user, LoginManager, login_user, login_required, UserMixin
from database import link_sql, check_user_exist
from werkzeug.utils import secure_filename
from PIL import Image
import datetime as dt
import os
app = Flask(__name__, template_folder='./templates')
app.secret_key = '12345678'
app.config['UPLOAD_POST_IMAGE_FOLDER'] = "static/images/post/"
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

    user = User(user['uId'], user['email'], user['permission'])
    return user


@app.route('/')
def index():
    selected_region = session.get('selected_region', '台北市')
    uId=session.get('uId', 0)
    login_status=session.get('login_status', 0)
    permission_manager=session.get('manager', 0)
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


@app.route('/sell.html')
def sell():
    selected_region = session.get('selected_region', '台北市')
    selected_pattern = session.get('selected_pattern','>=0')
    selected_houseType = session.get('selected_houseType',"All")
    selected_Price = session.get('selected_price',">=0")
    selected_twPing = session.get('selected_twPing',">=0")
    selected_age = session.get('selected_age',">=0")
    selected_myPost = session.get('selected_myPost',"All")
    uId = session.get("uId",0)
    
    sql = f"SELECT * FROM ((`house` INNER JOIN `post` ON house.pId = post.pId) INNER JOIN `image` ON image.pId = post.pId) INNER JOIN `housesell` ON house.hId = housesell.hId WHERE `city` = '{selected_region}' AND type = '住宅'"
    houseType_sql = "" if str(selected_houseType) == "All" else f" AND `houseType` = '{selected_houseType}'"
    pattern_sql = f" AND `bedRoom` {selected_pattern}"
    price_sql = f" AND `price` {selected_Price}"
    twPing_sql = f" AND `twPing` {selected_twPing}"
    age_sql = f" AND  `age` {selected_age}"
    
    if selected_myPost == "1":
        myPost_sql = f" AND `uId` = {uId}"
    elif selected_myPost == "0":
        myPost_sql = f" AND `uId` != {uId}"
    else:
        myPost_sql = "" 

    
    sql = sql + houseType_sql + pattern_sql + price_sql + twPing_sql + age_sql + myPost_sql
    db, cursor = link_sql()
    cursor.execute(sql)
    results = cursor.fetchall()
    
    
    db.close()

    return render_template(
        'sell.html', 
        selected_region=selected_region,
        post_results=results
    )


@app.route('/rentals.html')
def rentals():
    selected_region = session.get('selected_region', '台北市')
    selected_pattern = session.get('selected_pattern','>=0')
    selected_type = session.get('selected_type',"All")
    selected_Price = session.get('selected_price',">=0")
    selected_twPing = session.get('selected_twPing',">=0")
    selected_myPost = session.get('selected_myPost',"All")
    uId = session.get("uId",0)

    if selected_myPost == "1":
        myPost_sql = f" AND `uId` = {uId}"
    elif selected_myPost == "0":
        myPost_sql = f" AND `uId` != {uId}"
    else:
        myPost_sql = ""
    

    sql = f"SELECT * FROM ((`house` INNER JOIN `post` ON house.pId = post.pId) INNER JOIN `image` ON image.pId = post.pId) INNER JOIN `houserent` ON house.hId = houserent.hId WHERE `city` = '{selected_region}' "
    
    type_sql = "" if str(selected_type) == "All" else f" AND `type` = '{selected_type}'"
    pattern_sql = f" AND `bedRoom` {selected_pattern}"
    price_sql = f" AND `price` {selected_Price}"
    twPing_sql = f" AND `twPing` {selected_twPing}"
    

    sql = sql +  pattern_sql + price_sql + twPing_sql + type_sql + myPost_sql
    db, cursor = link_sql()
    
    
    cursor.execute(sql)
    results = cursor.fetchall()
    
    
    db.close()

    return render_template(
        'rentals.html', 
        selected_region=selected_region,
        post_results=results
    )

@app.route('/myPost.html')
def myPost():
    selected_uId  = session.get("uId",0)
    rent_sql = f"SELECT * FROM ((`house` INNER JOIN `post` ON house.pId = post.pId) INNER JOIN `image` ON image.pId = post.pId) INNER JOIN `houserent` ON house.hId = houserent.hId WHERE `uId` = {selected_uId}" 
    sell_sql = f"SELECT * FROM ((`house` INNER JOIN `post` ON house.pId = post.pId) INNER JOIN `image` ON image.pId = post.pId) INNER JOIN `housesell` ON house.hId = housesell.hId WHERE `uId` = {selected_uId}" 
    print(rent_sql)
    print(sell_sql)
    db, cursor = link_sql()
    
    
    cursor.execute(rent_sql)
    rent_results = cursor.fetchall()
    cursor.execute(sell_sql)
    sell_results = cursor.fetchall()
    
    
    db.close()

    return render_template(
        'myPost.html', 
        post_rent_results= rent_results,
        post_sell_results = sell_results
    )


@app.route('/sellinfo.html')
def sellinfo():
    pId = request.args.get('pId')
    uId = session.get("uId",0)
    selected_region = session.get('selected_region', '台北市')
    db, cursor = link_sql()
    
    sql = f"SELECT house.*, post.*, image.*, housesell.*FROM ((`house` JOIN `post` ON house.pId = post.pId)JOIN `image` ON image.pId = post.pId)JOIN `housesell` ON house.hId = housesell.hId WHERE `city` = '{selected_region}' AND post.pId = {pId} LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchone()
    db.close()
    
    if uId == results["uId"]:
         revise_permission = 1
    else:
         revise_permission = 0
    print(uId,results["uId"])
    
    return render_template(
    'sellinfo.html', 
    pId=pId,
     revise_permission =  revise_permission,
    postType = "sell",
    post=results
    )

@app.route('/rentalsinfo.html')
def rentalsinfo():
    pId = request.args.get('pId')
    uId = session.get("uId",0)
    selected_region = session.get('selected_region', '台北市')
    db, cursor = link_sql()
    
    sql = f"SELECT house.*, post.*, image.*, houserent.*FROM ((`house` JOIN `post` ON house.pId = post.pId)JOIN `image` ON image.pId = post.pId)JOIN `houserent` ON house.hId = houserent.hId WHERE `city` = '{selected_region}' AND post.pId = {pId} LIMIT 1"
    cursor.execute(sql)
    results = cursor.fetchone()    
    revise_permission = 1 if uId == results["uId"] else  0
    
    db.close()
    print(uId,results["uId"])
    return render_template(
    'rentalsinfo.html', 
    pId=pId,
    postType="rent",
    revise_permission =  revise_permission,
    post=results
    )
@app.route('/addPost.html')
def addPost():
    postType = request.args.get('postType')
    
    return render_template(
    'addPost.html',
    postType = postType)

@app.route('/uploadPost', methods=['POST','GET'])
def uploadPost():	
    uId = session.get('uId',0)
    db, cursor = link_sql()
    sql = f"SELECT `pId` from `post` ORDER BY `pId` DESC LIMIT 1"
    cursor.execute(sql)
    pId = cursor.fetchone()["pId"] + 1
    sql = f"SELECT `hId` from `house` ORDER BY `hId` DESC LIMIT 1"
    cursor.execute(sql)
    hId = cursor.fetchone()["hId"] + 1

    def insert_data(entity,attrs,int_attrs=[],float_attrs=[],bool_attrs = []):
        result = []
        for attr in attrs:
            if attr == "pId":
                result.append(pId)
            elif attr == "uId":
                result.append(uId)
            elif attr == "hId":
                result.append(hId)
            elif attr in int_attrs:
                result.append(int(request.form.get(attr)))
            elif attr in float_attrs:
                result.append(float(request.form.get(attr)))
            elif attr in bool_attrs:  
                result.append(1) if request.form.get(attr) else result.append(0)
            else:
                result.append(request.form.get(attr))
        
        sql = "INSERT INTO " + entity +str(attrs).replace("'","`") + "VALUES" + str(tuple(result))
        cursor.execute(sql)
        db.commit()
    
    
    post = ('pId','uId','title','city','district','address','name','phone','description')
    insert_data('`post`',post)

    house = ('hId','type','twPing','floor','lived','bedRoom','livingRoom','restRoom','balcony','pId')
    insert_data('`house`',house,['bedRoom','livingRoom','restRoom','balcony'],float_attrs=['twPing'] ,bool_attrs=['lived'])

    postType = request.form.get("postType")

    if postType == "sell":

        houseSell = ('hId','ratioOfPublicArea','pricePerTwping','price','age','houseType','houseName')
        insert_data('`houseSell`',houseSell,int_attrs=['age'],float_attrs=['ratioOfPublicArea','pricePerTwping','price'])

    elif postType == "rent":
        houseRent = ("hId","price","refrigerator", "washingMachine", "TV", "airConditioner", 
                "waterHeater", "bed", "closet", "paiedTVChannel", "internet", 
                "gas", "sofa", "deskChair", "balcony", "elevater", "parkingSpace")

        houseRent_bool_attrs = ["refrigerator", "washingMachine", "TV", "airConditioner", 
                            "waterHeater", "bed", "closet", "paiedTVChannel", "internet", 
                            "gas", "sofa", "deskChair", "balcony", "elevater", "parkingSpace"]
        insert_data('`houseRent`',houseRent,int_attrs= ["price"],bool_attrs=houseRent_bool_attrs)
    
    image = request.files["image"]
    imageName = f"post{pId}_"+secure_filename(image.filename)
    imagePath = "../../static/images/post/"+ imageName
    sql = f"INSERT INTO `Image`(`pId`,`image`) VALUES ({pId},'{imagePath}')"
    image.save(os.path.join(app.config['UPLOAD_POST_IMAGE_FOLDER'], imageName))
    cursor.execute(sql)
    db.commit()

    month = int(request.form.get("month"))
    payDate = dt.date.today()
    endDate = payDate + dt.timedelta(days=month*30)  
    payDate = dt.date.strftime(payDate, '%Y-%m-%d')
    endDate = dt.date.strftime(endDate, '%Y-%m-%d')

    payClass = int(request.form.get("class"))
    expDate = request.form.get("expDate")
    if payClass == 1:
        cost = month * 300
    elif payClass == 2:
        cost = month * 600
    else:
        cost = month *1000
    cardNumber = request.form.get("cardNumber")

    payment = str(('pId','payDate','endDate','class','expDate','cardNumber','cost')).replace("'","`")
    sql = f"INSERT INTO `Payment`{payment} VALUES ({pId},'{payDate}','{endDate}','{payClass}','{expDate}','{cardNumber}',{cost})" 
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    
    # 開啟圖片
    with Image.open("./static/images/post/"+imageName) as im:
        # 調整大小
        size = (600, 400)
        im_resized = im.resize(size)
        # 儲存圖片
        im_resized.save("./static/images/post/"+imageName)
    
    flash('貼文新增成功')
    return redirect(url_for('index'))

@app.route('/revisePost', methods=['POST','GET'])
def  revisePost():	
    
    db, cursor = link_sql()
    pId = int(request.form.get("pId"))
    sql = f"SELECT `hId` from `house` where `pId` = {pId}"
    cursor.execute(sql)
    hId  = cursor.fetchone()["hId"]
    def update_data(entity,attrs,int_attrs=[],float_attrs=[],bool_attrs = [],withoutHId = False):
        
        set_sql = " SET "
        for attr in attrs:
            value = request.form.get(attr)
            if attr in ["pId","uId","hId"]:
                    continue
            elif attr in bool_attrs: 
                if value:
                    set_sql = set_sql + f"`{attr}` = 1, " 
                else:
                    set_sql = set_sql + f"`{attr}` = 0, "
            elif not value:
                continue   
            elif attr in int_attrs:
                set_sql = set_sql + f"`{attr}` = {int(value)}, "
            elif attr in float_attrs:
                set_sql = set_sql + f"`{attr}` = {float(value)}, "
            else:
                set_sql = set_sql + f"`{attr}` = '{value}', "
        if withoutHId:
            sql = "UPDATE " + entity + set_sql[:-2] + f" where `pId` = {pId}"
        else:
            sql = "UPDATE " + entity + set_sql[:-2] + f" where `hId` = {hId}"
        try:
            cursor.execute(sql)
            db.commit()
        except:
            print(sql)
    
    
    post = ('pId','uId','title','city','district','address','name','phone','description')
    update_data('`post`',post,withoutHId=True)

    house = ('hId','type','twPing','floor','lived','bedRoom','livingRoom','restRoom','balcony','pId')
    update_data('`house`',house,['bedRoom','livingRoom','restRoom','balcony'],float_attrs=['twPing'] ,bool_attrs=['lived'])

    postType = request.form.get("postType")

    if postType == "sell":

        houseSell = ('hId','ratioOfPublicArea','pricePerTwping','price','age','houseType','houseName')
        update_data('`houseSell`',houseSell,int_attrs=['age'],float_attrs=['ratioOfPublicArea','pricePerTwping','price'])

    elif postType == "rent":
        houseRent = ("hId","price","refrigerator", "washingMachine", "TV", "airConditioner", 
                "waterHeater", "bed", "closet", "paiedTVChannel", "internet", 
                "gas", "sofa", "deskChair", "balcony", "elevater", "parkingSpace")

        houseRent_bool_attrs = ["refrigerator", "washingMachine", "TV", "airConditioner", 
                            "waterHeater", "bed", "closet", "paiedTVChannel", "internet", 
                            "gas", "sofa", "deskChair", "balcony", "elevater", "parkingSpace"]
        update_data('`houseRent`',houseRent,int_attrs= ["price"],bool_attrs=houseRent_bool_attrs)
    '''
    
    image = request.files["image"]
    imageName = f"post{pId}_"+secure_filename(image.filename)
    imagePath = "../../static/images/post/"+ imageName
    sql = f"INSERT INTO `Image`(`pId`,`image`) VALUES ({pId},'{imagePath}')"
    image.save(os.path.join(app.config['UPLOAD_POST_IMAGE_FOLDER'], imageName))
    cursor.execute(sql)
    db.commit()

    month = int(request.form.get("month"))
    payDate = dt.date.today()
    endDate = payDate + dt.timedelta(days=month*30)  
    payDate = dt.date.strftime(payDate, '%Y-%m-%d')
    endDate = dt.date.strftime(endDate, '%Y-%m-%d')

    payClass = int(request.form.get("class"))
    expDate = request.form.get("expDate")
    if payClass == 1:
        cost = month * 300
    elif payClass == 2:
        cost = month * 600
    else:
        cost = month *1000
    cardNumber = request.form.get("cardNumber")

    payment = str(('pId','payDate','endDate','class','expDate','cardNumber','cost')).replace("'","`")
    sql = f"INSERT INTO `Payment`{payment} VALUES ({pId},'{payDate}','{endDate}','{payClass}','{expDate}','{cardNumber}',{cost})" 
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()
    
    # 開啟圖片
    with Image.open("./static/images/post/"+imageName) as im:
        # 調整大小
        size = (600, 400)
        im_resized = im.resize(size)
        # 儲存圖片
        im_resized.save("./static/images/post/"+imageName)
    
    
    '''
    flash('貼文修改成功')
    return redirect(url_for('myPost'))
  






@app.route('/update/region', methods=['POST'])
def update_region():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'sussess'

@app.route('/update/pattern', methods=['POST'])
def update_pattern():
    selected_pattern = request.json['pattern']
    session['selected_pattern'] = selected_pattern
    return 'sussess'

@app.route('/update/houseType', methods=['POST'])
def update_houseType():
    selected_houseType = request.json['houseType']
    session['selected_houseType'] = selected_houseType
    return 'sussess'

@app.route('/update/type', methods=['POST'])
def update_type():
    selected_type = request.json['type']
    session['selected_type'] = selected_type
    return 'sussess'

@app.route('/update/price', methods=['POST'])
def update_price():
    selected_price = request.json['price']
    session['selected_price'] = selected_price
    return 'sussess'

@app.route('/update/twPing', methods=['POST'])
def update_twPing():
    selected_twPing = request.json['twPing']
    session['selected_twPing'] = selected_twPing
    return 'sussess'

@app.route('/update/age', methods=['POST'])
def update_age():
    selected_age = request.json['age']
    session['selected_age'] = selected_age
    return 'sussess'

@app.route('/update/region', methods=['POST'])
def update():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'sussess'

@app.route('/update/myPost', methods=['POST'])
def update_myPost():
    
    selected_myPost = request.json['myPost']
    
    session['selected_myPost'] = selected_myPost
    return 'sussess'



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
        session['manager'] = 0
        return 'invalid email'
        
    if user['password'] != password:
        session['manager'] = 0
        return 'password error'

    # 如果驗證成功，使用 login_user 函數登入使用者
    user = User(user['uId'], user['email'], user['permission'])
    login_user(user)
    if user.permission == 'manager':
         session['manager'] = 1
         print("manager value:", session['manager'])
    else:
        session['manager'] = 0
        
    session['uId']=user.id 
    session['login_status'] = 1
    flash('成功登入')
    return 'success'


@app.route('/signup', methods=['POST'])
def signup():
    # 獲取表單提交的用戶詳細信息
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    # 檢查用戶是否已經註冊
    if check_user_exist(email):
        # 如果用戶已經註冊，返回錯誤消息
        flash('該用戶已經註冊')
        return 'already signup'

    # 如果用戶尚未註冊，將其詳細信息存儲到資料庫中
    db, cursor = link_sql()
    sql = "INSERT INTO `user` (`name`, `email`, `password`) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, password))
    db.commit()

    # 獲取用戶 ID
    sql = "SELECT * FROM `user` WHERE `email` = %s "
    cursor.execute(sql, (email,))
    user = cursor.fetchone()
    db.close()
    # 登入用戶
    user = User(user['uId'], user['email'], user['permission'])
    login_user(user)
    
    if user.permission == 'manager':
         session['manager'] = 1
         print("manager value:", session['manager'])
    else:
        session['manager'] = 0
        

    session['login_status'] = 1



    
    # 返回一個成功消息
    flash('用戶註冊成功')
    return 'success'


# 登出的 API
@app.route('/logout')
@login_required
def logout():
    # 使用 logout_user 函數登出使用者
    logout_user()
    session['login_status'] = 0
    session['manager'] = 0
    session['uId'] = 0
    flash('成功登出')
    return redirect(url_for('index'))


@app.route('/delete_post_sell')
def delete_post_sell():
    db, cursor = link_sql()
    pId = request.args.get('pId')
    

    sql = "DELETE house, post, image,housesell,payment FROM house JOIN post ON house.pId = post.pId JOIN image ON image.pId = post.pId JOIN housesell ON house.hId = housesell.hId JOIN payment ON payment.pId = post.pId WHERE post.pId = %s "
    cursor.execute(sql, (pId,))
    db.commit()
    url = request.url
    flash('貼文刪除成功')
    
    
    return redirect(url_for('sell'))

@app.route('/delete_post_rent')
def delete_post_rent():
    db, cursor = link_sql()
    pId = request.args.get('pId')
  

    sql = "DELETE house, post, image,houserent,payment FROM house JOIN post ON house.pId = post.pId JOIN image ON image.pId = post.pId JOIN houserent ON house.hId = houserent.hId JOIN payment ON payment.pId = post.pId WHERE post.pId = %s "
    cursor.execute(sql, (pId,))
    db.commit()
    url = request.url
    flash('貼文刪除成功')
    
    
    return redirect(url_for('rentals'))

if __name__ == '__main__':
    app.run(debug=True)
