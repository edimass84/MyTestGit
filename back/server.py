from flask import Flask,request,jsonify
import yt_dlp
import uuid

app=Flask(__name__)

progress_data={}

SAVE_PATH="/home/dimas/windows/download/"

def hook(d):

    id=d['info_dict']['id']

    if d['status']=="downloading":

        progress_data[id]={
            "percent":round(d['_percent_str'].replace('%','').strip()),
            "speed":d['_speed_str'],
            "size":d['_total_bytes_str'],
            "done":False
        }

    if d['status']=="finished":
        progress_data[id]["done"]=True


def download(url,quality):

    id=str(uuid.uuid4())

    ydl_opts={
        'progress_hooks':[hook],
        'outtmpl':SAVE_PATH+'/%(title)s.%(ext)s'
    }

    if quality!="best":
        ydl_opts['format']=f'bestvideo[height<={quality}]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return id


@app.route("/download/video",methods=["POST"])
def video():

    data=request.json
    id=download(data["url"],data["quality"])

    return jsonify({"id":id})


@app.route("/download/playlist",methods=["POST"])
def playlist():

    data=request.json
    id=download(data["url"],data["quality"])

    return jsonify({"id":id})


@app.route("/progress/<id>")
def progress(id):

    if id in progress_data:
        return jsonify(progress_data[id])

    return jsonify({
        "percent":0,
        "speed":"0",
        "size":"0",
        "done":False
    })


app.run("0.0.0.0",5000)from flask import Flask,request,jsonify
import yt_dlp
import uuid

app=Flask(__name__)

progress_data={}

SAVE_PATH="/downloads/youtube/"

def hook(d):

    id=d['info_dict']['id']

    if d['status']=="downloading":

        progress_data[id]={
            "percent":round(d['_percent_str'].replace('%','').strip()),
            "speed":d['_speed_str'],
            "size":d['_total_bytes_str'],
            "done":False
        }

    if d['status']=="finished":
        progress_data[id]["done"]=True


def download(url,quality):

    id=str(uuid.uuid4())

    ydl_opts={
        'progress_hooks':[hook],
        'outtmpl':SAVE_PATH+'/%(title)s.%(ext)s'
    }

    if quality!="best":
        ydl_opts['format']=f'bestvideo[height<={quality}]+bestaudio/best'

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return id


@app.route("/download/video",methods=["POST"])
def video():

    data=request.json
    id=download(data["url"],data["quality"])

    return jsonify({"id":id})


@app.route("/download/playlist",methods=["POST"])
def playlist():

    data=request.json
    id=download(data["url"],data["quality"])

    return jsonify({"id":id})


@app.route("/progress/<id>")
def progress(id):

    if id in progress_data:
        return jsonify(progress_data[id])

    return jsonify({
        "percent":0,
        "speed":"0",
        "size":"0",
        "done":False
    })


app.run("0.0.0.0",5000)
