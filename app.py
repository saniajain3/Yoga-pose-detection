from flask import Flask, request, jsonify, render_template
import cv2
import traceback
from sip import *
import pickle
import warnings
warnings.filterwarnings("ignore")
# from ml import *
global label
global certainty

model = pickle.load(
    open("D:\\Projects\\ML SIP\\finalized_ensemble_soft.sav", "rb")
)
app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def home():
    return render_template("main.html")


@app.route("/try_now")
def try_now():
    return render_template("trynow.html")


@app.route("/accuracy")
def try1():
    return render_template("accuracy.html")


@app.route("/process_frame", methods=["POST"])
def predict():
    global label
    global certainty
    all_landmarks = []
    try:
        frame_file = request.files["frame"]
        frame_data = bytearray(frame_file.read())
        frame_np = np.asarray(frame_data, dtype=np.uint8)
        frame_np = np.array(frame_np)
        frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        image = equalize(image)
        image, landmarkss = landmarks(image)
        all_landmarks.append(landmarkss)
        # print(all_landmarks)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        label = model.predict(landmarkss)
        label = label[0]
        print(label)
        certainity = model.predict_proba(landmarkss)
        certainity = np.argmax(certainity)
        certainity = int(certainity)
        print(certainity)
        return jsonify({"label": label, "certainty": certainity})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route("/update_labels_certainty", methods=["POST"])
def update_labels_certainty():
    global label, certainty
    return jsonify({"label": label, "certainty": round(certainty * 100, 2)})


if __name__ == "__main__":
    app.run(debug=True)
