from flask import Flask, render_template, request, session

from database import link_sql

app = Flask(__name__, template_folder='./templates')
app.secret_key = '12345678'


@app.route('/')
def index():
    selected_region = session.get('selected_region', '台北市')
    db, cursor = link_sql()
    
    sql = f"SELECT * FROM `post` WHERE `city` = '{selected_region}' LIMIT 8"
    cursor.execute(sql)
    
    results = cursor.fetchall()
    print(results)
    
    db.close()

    return render_template(
        'index.html', 
        selected_region=selected_region,
        post_results=results
    )


@app.route('/update', methods=['POST'])
def update():
    selected_region = request.json['region']
    session['selected_region'] = selected_region
    return 'sussess'



if __name__ == '__main__':
    app.run(debug=True)
