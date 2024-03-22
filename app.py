from flask import Flask,jsonify,abort,make_response,request,url_for
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()
@app.route('/')
def index():
	return "<h1>Hello World!</h1>"


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@auth.get_password
def get_password(username):
    if username == "Akshay":
        return 'Bitlingu'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({"error":"unauthorized user"}),403)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id=task['id'],_external=True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route("/todo/api/v1.0/tasks",methods=["GET"])
@auth.login_required
def view_tasks():
	return jsonify({"tasks":[make_public_task(task) for task in tasks]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error":"Resource Not Found"}),404)

@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=["GET"])
def get_task(task_id):
    task = [task for task in tasks if task["id"]==task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({"task" : task[0]})

#code 404 is page not found
#code 400 is bad request
#code 201 is created
#code 403 is forbidden
#code 500 is Internal server error

@app.route("/todo/api/v1.0/tasks",methods=["POST"])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id':tasks[-1]['id']+1,
        'title':request.json['title'],
        'description':request.json.get("description",""),
        'done':False
    }
    tasks.append(task)
    return jsonify({'task':task}), 201

@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=['PUT'])
def edit_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    print(task)
    if len(task) == 0:
        abort(404)
    elif not request.json:
        abort(400)
    elif 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    elif 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    elif 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task[0]['title'] = request.json.get("title",task[0]['title'])
    task[0]['description'] = request.json.get("description",task[0]['description'])
    task[0]['done'] = request.json.get("done",task[0]['done'])
    return jsonify({"task":task})

@app.route("/todo/api/v1.0/tasks/<int:task_id>",methods=["DELETE"])
def delete_task(task_id):
    task = [task for task in tasks if task['id']==task_id]
    if len(task)==0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({"result":True})

"""
comands to:
    show all tasks curl -i http://localhost:5000/todo/api/v1.0/tasks
    show specific task curl -i http://localhost:5000/todo/api/v1.0/tasks/task_id
    create task curl -i -H "Content-Type:application/json" -X POST -d '{"title":"book reading"}' http://localhost:5000/todo/api/v1.0/tasks
    edit task curl -i -H "Content-Type:application/json" -X PUT -d '{"description":"read power of your mind","done":true}' http://localhost:5000/todo/api/v1.0/tasks/task_id
    delete task curl -i -H "Content-Type:application/json" -X DELETE http://localhost:5000/todo/api/v1.0/tasks/task_id
    note:these commands only work when your flask application is running
"""





























