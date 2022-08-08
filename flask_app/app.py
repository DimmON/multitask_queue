from flask import Flask, request, send_file
from celery import Celery
import os

SOURCE_PATH = './source_file'
RESULT_PATH = '../result_file'

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    backend=app.config['CELERY_RESULT_BACKEND']
)

celery.conf.update(app.config)


@app.route('/start_resize', methods=['GET', 'POST'])
def start_task():
    if request.method == 'GET':
        return 'Only POST method'
    else:
        file = request.files['file']
        if file:
            if file.content_type == 'image/jpeg':
                filename = file.filename
                file.save(os.path.join(SOURCE_PATH, filename))
                #                        queue name in task folder.function name
                task = celery.send_task('tasks.edit_img', kwargs={'filename': filename})
        return task.id


@app.route('/resize_status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = celery.AsyncResult(task_id, app=celery)
    return "Status of the Task " + str(status.state)


@app.route('/resize_result/<task_id>', methods=['GET'])
def task_result(task_id):
    result = celery.AsyncResult(task_id).result
    return send_file(os.path.join(RESULT_PATH, result))


if __name__ == '__main__':
    app.run(debug=True)
