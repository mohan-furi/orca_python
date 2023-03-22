from flask import Flask, jsonify, request
from base_api import BaseApi
from markupsafe import escape

app = Flask(__name__)
app.PYDEVD_DISABLE_FILE_VALIDATION = 1
base_api = BaseApi()


@app.route('/', methods=['GET', 'POST'])
def home():
    print('-----------returing')
    return jsonify({'body': 'hello world'})


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = base_api.find_one('users', data, fields_except={'password': 0})
    user['_id'] = user.get('_id').__str__()
    print('------------------user', user)
    return jsonify(user)


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    registered = base_api.insert_one('users', data)
    print('---------------registered', registered)
    return jsonify({'status': 'Ok', 'registered': True if registered else False})


@app.route('/get_by_id/<string:user_id>/<string:model>/<int:id>')
def get_by_id(user_id, model, id):
    if (id != 0):
        data = {'user_id': user_id, 'id': id}

    else:
        data = {'user_id': user_id}

    companies = base_api.find_all(model, query=data)
    print('-----------------companies', companies)
    return jsonify(companies)


@app.route('/create', methods=['POST'])
def create():
    data = request.json
    content = data.get('body')
    model = data.get('model')
    print('---------------model', model)
    print('---------------content', content)
    res = base_api.insert_one(data=content, table=model)
    return jsonify({'status': 'success', 'id': res.__str__(), 'msg': f'Content for {model} created successfully'})


@app.route('/read', methods=['POST'])
def read():
    data = request.json
    filters = data.get('body').get('filters')
    model = data.get('model')
    print('---------------model', model)
    print('---------------filters', filters)
    res = base_api.find_all(table=model, filter_by=filters)
    print('====================res', res)
    return jsonify({'status': 'success', 'id': 1, 'msg': f'Content for {model} extracted successfully with respect to filters {filters}',
                    'data': res})


@app.route('/delete', methods=['POST'])
def delete():
    data = request.json
    ids = data.get('body').get('ids')
    model = data.get('model')
    print('---------------model', model)
    print('---------------filters', ids)
    res = base_api.delete_one(table=model, ids=ids)
    print('====================res', res)
    return jsonify({'status': 'success', 'id': 1, 'msg': f'Content deleted successfully' if res == True else f'Something went wrong while deleting',
                    'data': res})


@app.route('/getData', methods=['POST'])
def getData():
    filters = request.json
    print(filters)
    res = base_api.find_all(filters.get(
        'table'), filter_by=filters.get('filterBy'))
    return jsonify(res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
