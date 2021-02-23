# coding=utf-8
from flask_cors import CORS
from flask import Flask, jsonify,request, session, redirect, url_for, render_template, make_response,json,send_file,send_from_directory
import config
import os
import cv2       
from faced import FaceDetector
from faced.utils import annotate_image
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app,resources=r'/*')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        argsJson = request.data.decode('utf-8')
        argsJson = json.loads(argsJson)
        argsJson["code"]=200
        print(argsJson)
        result = process_json(argsJson)
        print(result)
        result = json.dumps(result, ensure_ascii=False)
        return result
def process_json(data):
    # if(data.username=='admin'&data.password==123):
    t={} 
    t['data']=data
    return t

@app.route('/result', methods=['POST','GET'])
def result():
    f = request.files['file']
    print(f)
    print(f.filename)
    # f = f.read()
    # fdecode = f.decode('gbk')

    imagname = f.filename
    print(imagname)
    path = './acceptimage/unresult.jpg'
    f.save(path)
    image_file = detectimag(path) 
    basedir ='f:\\VueProjects\\py36\\hcbackstage\\responseimage\\timg.jpg'
    # img_stream = return_img_stream(basedir)
    # return img_stream
    return 'http://localhost:8443/result/responseimage/timg.jpg'    
# def return_img_stream(img_local_path):
#   """
#   工具函数:
#   获取本地图片�?
#   :param img_local_path:文件单张图片的本地绝对路�?
#   :return: 图片�?
#   """
#   import base64
#   img_stream = ''
#   with open(img_local_path, 'r') as img_f:
#     img_stream = img_f.read()
#     img_stream = base64.b64encode(img_stream)
#   return img_stream
def check_charset(file_path):
    import chardet
    with open(file_path, "rb") as f:
        data = f.read(4)
        charset = chardet.detect(data)['encoding']
    return charset


def detectimag(filename):
    face_detector = FaceDetector()
    img = cv2.imread(filename)
    rgb_img = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGB)
    bboxes = face_detector.predict(rgb_img, thresh=0.85)
    ann_img = annotate_image(img, bboxes)
    image = cv2.imwrite('F:/VueProjects/hcplatform/src/assets/timg.jpg',ann_img)

@app.after_request
def func_res(resp):     
    res = make_response(resp)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Methods'] = 'GET,POST'
    res.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return res

# your_path='f:\\VueProjects\\py36\\hcbackstage\\responseimage\\timg.jpg'
# with open(your_path, encoding=check_charset(your_path)) as f:
#     print()
#     print(your_path)
#     data = f.read(4)
#     print(data)

if __name__ == '__main__':
    app.run(host='localhost', port=8443,debug=True) 
