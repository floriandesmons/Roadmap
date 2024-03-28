# roadmap

Scripts developed by HES-SO Valais-Wallis as part of the HES-SO project in collaboration with HEPIA. 
Main objective: Model and simulate the behavior of a CO2 network.

## Installation instructions  

First, make sure that Python version 3.11.5 is installed. If not, you can download it from the following link: https://www.python.org/downloads/release/python-3115/. 
During installation, be sure to check the option “Add Python 3.11 to PATH.” 🐍✨

### Windows (Python version = 3.11.5)

Start by creating a virtual environment: 
```
pip install virtualenv
pip install virtualenvwrapper-win
virtualenv -p C:\path\to\python.exe C:\path\to\desired_env_folder
```

Then activate the virtual environment: 
```
cd C:\path\to\desired_env_folder\Scripts
activate
``` 
Install the required libraries in the newly created virtual environment using the following command:
```
(roadmap_env) pip install -r requirements.txt
```
