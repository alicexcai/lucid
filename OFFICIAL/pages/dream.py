import streamlit as st
import pandas as pd
import pygsheets
from datetime import datetime
import openai
import requests

def app():
    
    # SET APP PROPERTIES

    st.title("LUCID DREAM")
    
    class Params:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
            
    params = Params()
    imgparams = Params()
    results = Params()
    
    with st.sidebar.expander("See instructions"):
        st.markdown("""
                    ### Instructions:
                    * Every day, before you go to bed, fill out the form.
                    * Click "Begin Incubation" to begin the incubation process.
                    * Follow the incubation process.
                    ---
                    \n\n
                    """)

    openai.api_key = st.secrets["OPENAI_API_KEY"]
    
    gc = pygsheets.authorize(service_file='')
    sheet = gc.open('Lucid_Database')
    completions_wks = sheet.worksheet('title', 'sessions')
    
    user = st.sidebar.text_input("What is your name?")
    params.environment = st.text_input("What is the most memorable location you've been to today?", help="Ex: a beautiful beach")
    params.event = st.text_input("What is the most interesting event that's happened to you today?", help="Ex: explored an abandoned house")
    params.temperature = st.slider("How novel do you want your dream to be?", min_value=0.0, max_value=1.0, value=0.7)
    
    imgparams.clip_guidance_scale = 50000
    imgparams.tv_scale = 80000
    imgparams.img_size = 400
    imgparams.num_steps = 200
    
    # RUN EXPLORATION
    
    if st.button("Begin Incubation"):
        
        params.session = datetime.now().strftime("%Y%m%d%H%M%S")
        params.prompt = f"""Environment: a beautiful and relaxing beach
            Interesting Event: went to first day of classes 
            Dream: I am walking on the beach with a Harvard professor, our feet sifting through the sand and the wind blowing lightly in the air. In the background, we hear the sound of waves hitting the shore as the two of us walk there like old friends.

            ###

            Environment: rainy night
            Interesting Event: thought about the end of the world
            Dream: I am running downstairs toward the uproar of noise, toward the chaos. Rain pours from the sky, water rises above my knees on the ground. Everyone is out on the street, walking toward something in the far distance. I try to squeeze through the mass of bodies toward the front trying to find my family. I can't find anyone, the kids are crying on the streets, I just want to figure out why this is happening. I look up and see a huge spaceship hovering overhead, and it feels so close to my head. 

            ###

            Environment: {params.environment}
            Interesting Event: {params.event}
            Dream:"""
        
        params.num_output = 1
        params.model = 'davinci'
        params.max_tokens = 250
        params.stop = '###'
        params.top_p = 1.0
        params.frequency_penalty = 0.0
        params.presence_penalty = 0.0
        params.best_of = 1
        
        # OPTION TO SEE EXPLORATION PARAMETERS
        # with st.expander("See Parameters"):
        #     st.write(params.__dict__)

        with st.spinner('Generating...'):  
                
            priming_response = openai.Completion.create(
                model=params.model,
                prompt=params.prompt,
                temperature=params.temperature,
                max_tokens=params.max_tokens,
                top_p=params.top_p,
                frequency_penalty=params.frequency_penalty,
                presence_penalty=params.presence_penalty,
                n=params.num_output,
                stop=params.stop,
                )
            
            results.priming = priming_response['choices'][0]['text']           
            st.write("Priming: ", results.priming)
            
            imgparams.prompt = f"""Dream: I am walking on the beach with a Harvard professor, our feet sifting through the sand and the wind blowing lightly in the air. In the background, we hear the sound of waves hitting the shore as the two of us walk there like old friends.
                Caption: two figures walking along a beautiful sandy beach | peaceful oceanside waves lap onto the shore

                ###

                Dream: I am running downstairs toward the uproar of noise, toward the chaos. Rain pours from the sky, water rises above my knees on the ground. Everyone is out on the street, walking toward something in the far distance. I try to squeeze through the mass of bodies toward the front trying to find my family. I can't find anyone, the kids are crying on the streets, I just want to figure out why this is happening. I look up and see a huge spaceship hovering overhead, and it feels so close to my head. 
                Caption: end of the world, thunderstorm flooding the earth | hundreds of bodies squeezing past each other | huge alien spaceship hovering overhead

                ###

                Dream: I am sitting in a colossal cathedral surrounded by the spirits of the dead. They are whispering something among themselves, something I can't quite make out. I look at them, a sea of pale faces. I try to speak, but I have no voice. One of them hands me a pen and a piece of paper. I start to write.
                Caption: art nouveau design of a cathedral interior | glowing glossy stained glass windows, high vaulted ceilings | intricately detailed chandeliers and godly lights | translucent spirits of the dead floating in the air

                ###

                Dream: {results.priming}
                Caption:"""
            
            caption_response = openai.Completion.create(
                model=params.model,
                prompt=imgparams.prompt,
                temperature=params.temperature,
                max_tokens=params.max_tokens,
                top_p=params.top_p,
                frequency_penalty=params.frequency_penalty,
                presence_penalty=params.presence_penalty,
                n=params.num_output,
                stop=params.stop,
                )

            imgparams.caption = caption_response['choices'][0]['text']   
            completions_data = completions_wks.get_all_records()
            last_row_completions = len(completions_data)+1
            new_completion_data = [datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f"), params.environment, params.event, params.temperature, priming_response['choices'][0]['text'], caption_response['choices'][0]['text'], 'https://lucid-dream.s3.us-east-2.amazonaws.com/' + params.session]
            completions_wks.insert_rows(last_row_completions, number=1, values=new_completion_data)

        def display_images(output_bucket, num_steps):
        
            base_path = "" + output_bucket
            num_images = 130

            initial, mid, final = st.columns(3)
            initial.image(base_path + f"/progress_30.png")
            mid.image(base_path + f"/progress_{int(num_images/2)}.png")
            final.image(base_path + f"/progress_{int(num_images)}.png")
            
        output_bucket = f"lucid-dream/images/{user}/{params.session}"
        with st.expander("See Images"):
            display_images(output_bucket, imgparams.num_steps)

        url = ''
        request_data = {
            'caption': imgparams.caption.strip(),
            'session': 'lucid-dream',
            'room': 'images',
            'topic': user,
            'prompt_num': params.session,
            'clip_guidance_scale': imgparams.clip_guidance_scale,
            'tv_scale': imgparams.tv_scale,
            'img_size': imgparams.img_size,
            'num_steps': imgparams.num_steps,            
                        }

        x = requests.post(url, data = request_data)