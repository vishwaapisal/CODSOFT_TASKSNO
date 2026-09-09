import os, cv2, json, urllib.request, tempfile, time
import numpy as np
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 120 * 1024 * 1024

ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(ROOT, "models")
FACE_DIR = os.path.join(ROOT, "data", "faces")
os.makedirs(MODEL_DIR, exist_ok=True); os.makedirs(FACE_DIR, exist_ok=True)

YUNET = os.path.join(MODEL_DIR, "face_detection_yunet_2023mar.onnx")
SFACE = os.path.join(MODEL_DIR, "face_recognition_sface_2021dec.onnx")
# Multiple mirrors because some networks block GitHub's LFS endpoint.
YUNET_URLS = [
    "https://media.githubusercontent.com/media/opencv/opencv_zoo/refs/heads/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx?download=true",
    "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx?download=true",
]
SFACE_URLS = [
    "https://media.githubusercontent.com/media/opencv/opencv_zoo/refs/heads/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx?download=true",
    "https://huggingface.co/opencv/face_recognition_sface/resolve/main/face_recognition_sface_2021dec.onnx?download=true",
]

detector = recognizer = reference = None

def api_error(message, status=500, details=None):
    x={"ok":False,"error":message}
    if details: x["details"]=details
    return jsonify(x),status

def valid_model(path, minimum):
    try:
        if not os.path.exists(path) or os.path.getsize(path)<minimum: return False
        with open(path,"rb") as f: head=f.read(120)
        return not head.startswith(b"version https://git-lfs.github.com/spec")
    except: return False

def download_model(urls,path,minimum):
    if valid_model(path,minimum): return
    temp=path+".download"; errors=[]
    for url in urls:
        try:
            if os.path.exists(temp): os.remove(temp)
            req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 FaceVision-CODSOFT/1.0","Accept":"application/octet-stream,*/*"})
            with urllib.request.urlopen(req,timeout=120) as r, open(temp,"wb") as out:
                while True:
                    chunk=r.read(1024*1024)
                    if not chunk: break
                    out.write(chunk)
            if not valid_model(temp,minimum): raise RuntimeError("Downloaded file is not a complete ONNX model.")
            os.replace(temp,path); return
        except Exception as e:
            errors.append(str(e))
            if os.path.exists(temp): os.remove(temp)
    raise RuntimeError("AI model download failed. Check internet access or place the ONNX files in the models folder manually. Tried mirrors: "+ " | ".join(errors))

def load_models():
    global detector,recognizer
    if detector is not None and recognizer is not None: return detector,recognizer
    download_model(YUNET_URLS,YUNET,150000)
    download_model(SFACE_URLS,SFACE,20000000)
    detector=cv2.FaceDetectorYN.create(YUNET,"",(320,320),0.85,0.3,5000)
    recognizer=cv2.FaceRecognizerSF.create(SFACE,"")
    return detector,recognizer

def detect(im):
    d,_=load_models(); h,w=im.shape[:2]; d.setInputSize((w,h)); _,fs=d.detect(im)
    return [] if fs is None else fs

def embed(im,f):
    _,r=load_models(); return r.feature(r.alignCrop(im,f))

def cosine(a,b):
    a=np.asarray(a,np.float32).ravel(); b=np.asarray(b,np.float32).ravel()
    return float(np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))) if np.linalg.norm(a)*np.linalg.norm(b) else 0.0

def meta_path(): return os.path.join(FACE_DIR,"reference.json")
def img_path(): return os.path.join(FACE_DIR,"reference.jpg")

def load_reference():
    global reference
    if reference is not None: return reference
    if not os.path.exists(meta_path()) or not os.path.exists(img_path()): return None
    try:
        with open(meta_path(),encoding="utf-8") as f: name=json.load(f)["name"]
        im=cv2.imread(img_path())
        fs=detect(im)
        if len(fs)!=1:return None
        reference={"name":name,"embedding":embed(im,fs[0])}
        return reference
    except:return None

def analyze_frame(im):
    ref=load_reference()
    fs=detect(im)
    results=[]
    for f in fs:
        sim=cosine(ref["embedding"],embed(im,f)) if ref else 0
        results.append({"x":int(f[0]),"y":int(f[1]),"w":int(f[2]),"h":int(f[3]),"confidence":round(float(f[-1])*100,1),"similarity":round(sim*100,1)})
    best=max(results,key=lambda x:x["similarity"]) if results else None
    return {"reference":ref["name"] if ref else None,"detected":len(results),"faces":results,"matched":bool(best and best["similarity"]>=36.3),"similarity":best["similarity"] if best else 0}

@app.route("/")
def home(): return render_template("index.html")

@app.get("/health")
def health():
    return jsonify({"ok":True,"reference":load_reference() is not None})

@app.post("/enroll")
def enroll():
    global reference
    try:
        name=request.form.get("name","").strip()
        if not name:return api_error("Enter a person's name.",400)
        if "image" not in request.files:return api_error("Please provide an enrollment photo.",400)
        im=cv2.imdecode(np.frombuffer(request.files["image"].read(),np.uint8),cv2.IMREAD_COLOR)
        if im is None:return api_error("Invalid enrollment image.",400)
        fs=detect(im)
        if len(fs)!=1:return api_error(f"Enrollment requires exactly one face. Detected {len(fs)}.",400)
        reference={"name":name,"embedding":embed(im,fs[0])}
        cv2.imwrite(img_path(),im)
        with open(meta_path(),"w",encoding="utf-8") as f:json.dump({"name":name},f)
        return jsonify(ok=True,name=name,message="Reference face enrolled.")
    except Exception as e:return api_error("Enrollment failed.",500,str(e))

@app.post("/test")
def test():
    try:
        if load_reference() is None:return api_error("Enroll a reference face first.",400)
        if "image" not in request.files:return api_error("Please provide a test image.",400)
        im=cv2.imdecode(np.frombuffer(request.files["image"].read(),np.uint8),cv2.IMREAD_COLOR)
        if im is None:return api_error("Invalid test image.",400)
        r=analyze_frame(im); r["ok"]=True; return jsonify(r)
    except Exception as e:return api_error("Test failed.",500,str(e))

@app.post("/live")
def live():
    try:
        if load_reference() is None:return api_error("Enroll a reference face first.",400)
        raw=request.files["image"].read()
        im=cv2.imdecode(np.frombuffer(raw,np.uint8),cv2.IMREAD_COLOR)
        if im is None:return api_error("Invalid camera frame.",400)
        r=analyze_frame(im); r["ok"]=True; return jsonify(r)
    except Exception as e:return api_error("Live recognition failed.",500,str(e))

@app.post("/video")
def video():
    # Process an uploaded video and return a short recognition summary.
    path=None
    try:
        if load_reference() is None:return api_error("Enroll a reference face first.",400)
        if "video" not in request.files:return api_error("Please select a video.",400)
        vf=request.files["video"]
        suffix=os.path.splitext(vf.filename or ".mp4")[1] or ".mp4"
        fd,path=tempfile.mkstemp(suffix=suffix); os.close(fd); vf.save(path)
        cap=cv2.VideoCapture(path)
        if not cap.isOpened(): return api_error("Could not open this video file.",400)
        fps=cap.get(cv2.CAP_PROP_FPS) or 25
        total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        step=max(1,int(fps/3)) # analyze ~3 frames/sec
        frames=matches=0; best=0; last_faces=0
        while True:
            ok,frame=cap.read()
            if not ok: break
            idx=int(cap.get(cv2.CAP_PROP_POS_FRAMES))-1
            if idx%step: continue
            frames+=1
            r=analyze_frame(frame)
            last_faces=r["detected"]
            if r["matched"]: matches+=1
            best=max(best,r["similarity"])
        cap.release()
        return jsonify(ok=True,name=reference["name"],frames_analyzed=frames,match_frames=matches,best_similarity=round(best,1),last_faces=last_faces,match_ratio=round((matches/frames*100) if frames else 0,1))
    except Exception as e:return api_error("Video analysis failed.",500,str(e))
    finally:
        if path and os.path.exists(path):
            try:os.remove(path)
            except:pass

if __name__=="__main__":
    app.run(host="127.0.0.1",port=5000,debug=True)
