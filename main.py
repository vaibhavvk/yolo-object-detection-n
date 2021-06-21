from flask import Flask,render_template,request,json,jsonify,session,redirect,send_file,url_for,flash
import os
from werkzeug.utils import secure_filename
import object_detection_yolo
import cv2

#import systemcheck


app=Flask(__name__)
app.secret_key="secure"
app.config['UPLOAD_FOLDER'] = str(os.getcwd())+'/static/uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
data =0
name=0
gender=0
age=0
treatment_duration=0
image_name=0
image_data=0


@app.route('/',methods=["post","get"])
def first_page():
    if request.method=="POST":
        global image_name,image_data


        
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            new_data = []

            image = cv2.imread('static/uploads/'+filename)

            item_names, confidences, frame = object_detection_yolo.detect_object(image)
            if item_names == confidences == frame == 0:
                print("Upload Color Image")
            elif item_names == confidences == 0 and frame != 0:
                print("Some Error", frame)
            else:
                print("Image Processed Successfully")
                cv2.imwrite("static/uploads/processed.png", frame)

            return render_template("data_page.html",
                           filename="processed.png", result = str(item_names))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)

    else:
        return render_template("form_page.html")


@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

app.run(debug=True)