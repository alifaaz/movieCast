from flask import Flask, redirect, url_for,request, render_template,send_from_directory
from werkzeug.utils import secure_filename
from helpers import videoProcesssor, castImage
import cv2
import os
app = Flask(__name__,static_url_path='')
app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
   return render_template('upload.html')
@app.route('/admin/<coco>')
def admin(coco):
   return f'{coco}'

@app.route('/upload',methods = ['POST', 'GET'])
def upload():
   if request.method == 'POST':
      file = request.files['fofo']
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
      cap = cv2.VideoCapture(f'uploads/{file.filename}')
      vidUrl =f'uploads/{file.filename}'
      casts,times = videoProcesssor.videoProcess(vidUrl)

      castImgs = castImage.getImages(casts.split("\n")[3:8])

      return render_template('resp.html',time=f'start time: {((times[0]/1000)/60)}s , end time: {((times[-1]/1000)/60)}s',casts=castImgs)
      # return redirect(url_for('admin',coco = f'start time: {((times[0]/1000)/60)}s , end time: {((times[-1]/1000)/60)}s'))
   else:
      return redirect(url_for('/'))


if __name__ == '__main__':
   app.run(debug=True)