![image](https://github.com/23justo/url_shortener/assets/14941128/b9c3b7e0-fa0e-436e-beec-8bb48d167428)# url_shortener
FASTAPI URL Shortener Assessment

##Requirements
Python 3.11.8 (this tool should be compatible with other python3 version)

## Installation process
Creating a virtual env

run python -m venv virtual_env_name
when using windows run
```
./virtual_env_name/Script/activate
```
for linux
```
source virtual_env_name/bin/activate
```
when the virtual env is running install dependencies 
locate the requirements.txt file, inside that same folder run 
```
pip install -r requirements.txt
```
## Runing the project
locate the terminal in the same folder as main.py file and ensure the virtual env is running
![image](https://github.com/23justo/url_shortener/assets/14941128/8f2945aa-51a6-4d59-bb35-bb9aec7ba768)

Run the next command
```
uvicorn main:app --reload
```
This command will activate the uvicorn server on your local machine giving you a local server for testing
![image](https://github.com/23justo/url_shortener/assets/14941128/c5aee2d2-ef88-45ba-9359-e060089c64d0)

## Project Ussage 
Go to localhost:8000 or the url the uvicorn server provided for you, inside this page you have a swagger page wich will give you more information on how to use the 3 endpoints available
![image](https://github.com/23justo/url_shortener/assets/14941128/c701d518-b61e-4468-b8a0-5f544b1fdbd5)

If you click on a endpoint it will give you a try it out button where you can send a request, it will say wich type of data can be send and the type of responses available.
