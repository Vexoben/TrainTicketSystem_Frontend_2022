from flask import Flask, request, render_template, jsonify, make_response, send_from_directory
from trans import Courier

app = Flask(__name__)
courier = Courier('./code')

@app.route('/', methods = ['POST','GET'])
def hello():
    courier.add_user('you_know_who', 'you_know_who', 'you_know_what', '大摆锤', 'vegetable@sjtu.edu.cn', 10)
    user_info = request.form.to_dict()
    if ('current_user' in user_info.keys() and user_info['current_user'] != ''):
        return render_template('./user.html', current_user = user_info['current_user'])
    if (request.form.get('username') is not None):
        us = request.form.get('username')
        ps = request.form.get('password')
        courier.logout(us)
        res = courier.login(us, ps)
        if (res == 0):
            return render_template('./user.html', current_user = us)
        else:
            return render_template('./front.html', fail_login = 1)
    else:
        return render_template('./front.html', fail_login = 0)

#    return render_template("./front.html", fail_login = 0)

@app.route('/login', methods = ['POST','GET'])
def login():
    us = request.form.get('username')
    ps = request.form.get('password')
    courier.logout(us)
    res = courier.login(us, ps)
    if (res == 0):
        return render_template('./login.html', fail_login = 0, user = us)
    else:
        return render_template('./login.html', fail_login = 1)

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if (request.form.get('username')):
        us = request.form.get('username')
        n = request.form.get('name')
        m = request.form.get('mailAddr')
        ps = request.form.get('password')
        te = request.form.get('terms')
        if (te is not None):
            root_login = courier.login('you_know_who', 'you_know_what')
            res = courier.add_user('you_know_who', us, ps, n, m, 0)
            if (res == 0):
                if (root_login == 0):
                    courier.logout('you_know_who')
                return render_template('./register.html', fail_register = 0)
            else:
                if (root_login == 0):
                    courier.logout('you_know_who')
                return render_template('./register.html', fail_register = 1)            
        else:
            return render_template('./register.html', fail_register = 2)
    else:
        return render_template('./register.html', fail_register = -1)

@app.route('/personal_profile', methods = ['POST', 'GET'])
def personal_profile():
    user_info = request.form.to_dict()
    if ('current_user' in user_info.keys() and user_info['current_user'] != ''):
        info = courier.query_profile(user_info['current_user'], user_info['query_user'])
        return render_template('./personal_profile.html', username = info[0], name = info[1], mailAddr = info[2], privilege = int(info[3]), current_user = info[0])
    else:
        return render_template('./register.html')

@app.route('/modify_user', methods = ['POST', 'GET'])
def modify_user():
    user_info = request.form.to_dict()
    print(user_info)
    if (not('current_user' in user_info.keys() and user_info['current_user'] != '')):
        return render_template('./register.html')
    if ('username' in user_info.keys() and user_info['username'] != ''):
        current_user = user_info['current_user']
        username = user_info['username']
        cu_info = courier.query_profile(current_user, current_user)
        us_info = courier.query_profile(current_user, username)
        if ('privilege' in user_info.keys() and user_info['privilege'] != '' and (us_info[0] == '-1' or int(cu_info[3]) < int(user_info['privilege']))):
            return render_template('./modify_user.html', fail_type = 1, current_user = current_user)
        else:
            s = '[0] modify_profile -c ' + current_user + ' -u ' + username
            if ('name' in user_info.keys() and user_info['name'] != ''):
                s = s + ' -n ' + user_info['name']
            if ('mailAddr' in user_info.keys() and user_info['mailAddr'] != ''):
                s = s + ' -m ' + user_info['mailAddr']
            if ('privilege' in user_info.keys() and user_info['privilege'] != ''):
                s = s + ' -g ' + user_info['privilege']
            if ('password' in user_info.keys() and user_info['password'] != ''):
                s = s + ' -p ' + user_info['password']
            res = courier.modify_user(s)
            if (res[0] == '-1'):
                return render_template('./modify_user.html', fail_type = 1)
            else :
                return render_template('./modify_user.html', fail_type = 0, current_user = current_user)
    else:
        return render_template('./modify_user.html', current_user = user_info['current_user'], fail_type = 2)

@app.route('/add_user', methods = ['POST', 'GET'])
def add_user():
    user_info = request.form.to_dict()
    print(user_info)
    if (not('current_user' in user_info.keys() and user_info['current_user'] != '')):
        return render_template('./register.html')
    if ('username' in user_info.keys() and user_info['username'] != ''):
        current_user = user_info['current_user']
        username = user_info['username']
        s = '[0] add_user -c ' + current_user + ' -u ' + username
        if ('privilege' in user_info.keys() and user_info['privilege'] != ''):
            s = s + ' -g ' + user_info['privilege']
        else:
            return render_template('add_user.html', fail_type = 4, current_user = current_user)
        cu_info = courier.query_profile(current_user, current_user)
        us_info = courier.query_profile(current_user, username)
        if (us_info[0] != '-1' or int(cu_info[3]) <= int(user_info['privilege'])):
            return render_template('add_user.html', fail_type = 3, current_user = current_user)
        else:
            if ('name' in user_info.keys() and user_info['name'] != ''):
                s = s + ' -n ' + user_info['name']
            else:
                return render_template('add_user.html', fail_type = 4, current_user = current_user)
            if ('mailAddr' in user_info.keys() and user_info['mailAddr'] != ''):
                s = s + ' -m ' + user_info['mailAddr']
            else:
                return render_template('add_user.html', fail_type = 4, current_user = current_user)
            if ('password' in user_info.keys() and user_info['password'] != ''):
                s = s + ' -p ' + user_info['password']
            else:
                return render_template('add_user.html', fail_type = 4, current_user = current_user)
            res = courier.add_user2(s)
            return render_template('./add_user.html', fail_type = 1, current_user = current_user)
    else:
        return render_template('./add_user.html', current_user = user_info['current_user'], fail_type = 4)

@app.route('/train', methods = ['POST', 'GET'])
def train():
    return render_template("./train.html")

@app.route('/add_train', methods = ['POST', 'GET'])
def add_train():
    return render_template("./add_train.html")      

@app.route('/delete_train', methods = ['POST', 'GET'])
def delete_train():
    return render_template("./delete_train.html")      

@app.route('/release_train', methods = ['POST', 'GET'])
def release_train():
    return render_template("./release_train.html")      

@app.route('/query_train', methods = ['POST', 'GET'])
def query_train():
    return render_template("./query_train.html")

@app.route('/ticket', methods = ['POST', 'GET'])
def ticket():
    return render_template("./ticket.html")      

@app.route('/buy_ticket', methods = ['POST', 'GET'])
def buy_ticket():
    return render_template("./buy_ticket.html")

@app.route('/query_ticket', methods = ['POST', 'GET'])
def query_ticket():
    return render_template("./query_ticket.html")

@app.route('/refund_ticket', methods = ['POST', 'GET'])
def refund_ticket():
    return render_template("./refund_ticket.html")


if __name__ == '__main__':
    #app.run()
    app.run(host = '0.0.0.0', port = 8888)
