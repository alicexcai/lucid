# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, send_file, request
import subprocess
from diffusion_model import define_model
import subprocess

class Params:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

app = Flask(__name__)
params = Params()

@app.route('/getImage', methods=["POST"])
def VisualLucid():
    # Get text input
    print("endpoint hit:)")
    params.clip_input = request.form.get("clip_input") if request.form.get("clip_input") != None else request.args.get("clip_input")
    params.folder_name = request.form.get("folder_name") if request.form.get("folder_name") != None else request.args.get("folder_name")
    params.prompt_num = request.form.get("prompt_num") if request.form.get("prompt_num") != None else request.args.get("prompt_num")
    params.session = request.form.get("session") if request.form.get("session") != None else request.args.get("session")
    try:
        params.cutn = request.form.get("cutn") if request.args.get("cutn") else 16
        params.clip_guidance_scale = request.form.get("clip_guidance_scale") if request.args.get("clip_guidance_scale") else 50000
        params.tv_scale = request.form.get("tv_scale") if request.args.get("tv_scale") else 80000
        params.img_size = request.form.get("img_size") if request.args.get("img_size") else 512
        params.num_steps = request.form.get("num_steps") if request.args.get("num_steps") else 500
    except:
        print("no params given for cutn, clip_guidance_scale, tv_scale, num_steps, and/or img_size")
    
    print("PARAMS:\n", params.__dict__)
    # Run the Network
    define_model(clip_input=params.clip_input, folder_name=params.folder_name, prompt_num=params.prompt_num, session=params.session, cutn=params.cutn, clip_guidance_scale=params.clip_guidance_scale, tv_scale=params.tv_scale, img_size=params.img_size, num_steps=params.num_steps)
    # Make into video
#     makeMp4command=['bash', './makeMP4', params.session, params.folder_name, params.prompt_num]
#     subprocess.call(makeMp4command)
    # Return after done running
    return "All done."


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    print("Enter ????Lucid????")
    app.run(host='0.0.0.0', threaded=True)