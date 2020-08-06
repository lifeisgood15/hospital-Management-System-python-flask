# hospital-Management-System-python-flask
steps:
1. Download code and save to your project folder
2. In terminal go to your project folder 
    cd foldername
3. Create a virtual environment using command:
    py -m venv YOUR_ENV_NAME
   And activate your environment using
    YOUR_ENV_NAME\Scripts\activate
4. Install all requirements for this project using:
    pip install -r requirements.txt
5. Connect to mongodb and in config.py write your database's name
6. In mongoDB add a collection 'userstore' and store one user and password(encrypted) and set department as 'admin'
7. Run your app using
    flask run
  
