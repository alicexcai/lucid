# lucid-dream

### Create a Text Database

Follow the [pygsheets documentation](https://pygsheets.readthedocs.io/en/stable/) to create a database.

Create a spreadsheet based on [this template](https://docs.google.com/spreadsheets/d/1-_cIxNZ5TfGMpYAyhbvGRaeDj2FD-e8UIDFwUiWszBg/edit?usp=sharing). Make sure to share the sheet with your gservice account.

Add your gservice authorization file to the directory and insert the file path in line 34 of dreams.py:
```gc = pygsheets.authorize(service_file='')```

### Create an Image Database

Create an AWS S3 bucket that allows all public access. 

Edit the permissions bucket policy to the following:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::insert_bucket_name/*"
        }
    ]
}
```

Edit line 137 in dream.py to specify the AWS S3 bucket path in ```base_path = "" + output_bucket```


### Create Server

Create an AWS access role and add your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY to .streamlit/secrets.toml

Launch a ml.g4dn.4xlarge sagemaker instance. 

Upload the files under the server directory to the sagemaker instance.

On line 111 in diffusion_model.py, edit ```def savetoS3Bucket(image_path)``` to specify your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and your S3 bucket name.

Setup the server by calling ```bash setup```

Launch the server by calling ```python server.py```

Install [localtunnel](https://github.com/localtunnel/localtunnel) and configure a persistent endpoint for your localhost:5000. 

Edit line 149 in dream.py to specify the localtunnel endpoint ```url = ''```


### Connect OpenAI

Add your OPENAI_API_KEY to .streamlit/secrets.toml