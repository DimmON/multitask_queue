from celery import Celery
from celery.utils.log import get_task_logger
from PIL import Image
import os

SOURCE_PATH = '../source_file'
RESULT_PATH = '../result_file'

img_size = (200, 200)


logger = get_task_logger(__name__)

app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)


def resize_img_prop(image, new_size=(100, 100)):
    """
    Возвращает картинку, пропорционально изменив ее размер до заданных значений
    """
    k_w, k_h = new_size[0] / image.size[0], new_size[1] / image.size[1]
    if k_w > k_h:
        new_size = (int(image.size[0] * k_h), new_size[1])
    elif k_w < k_h:
        new_size = (new_size[0], int(image.size[1] * k_w))
    return image.resize(new_size)


def edit_image(filename):
    with Image.open(os.path.join(SOURCE_PATH, filename)) as img:
        img = resize_img_prop(img, img_size)
        img.save(os.path.join(RESULT_PATH, filename))


@app.task()
def edit_img(filename):
    logger.info('Begin image resize' + filename)
    edit_image(filename)
    logger.info('End image resize' + filename)
    return filename

