from flask import Flask, request, jsonify
import subprocess
import os
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

custom_keywords = {
   'dikhao': 'print',
   'pucho': 'input',
   'agar': 'if',
   'warna': 'else',
   'jabtak': 'while',
   'keLiye': 'for',
   'mein': 'in',
   'ruko': 'break',
   'jaariRakho': 'continue',
   'wapsi': 'return',
   'kaise': 'def',
   'varg': 'class',
   'sankhaya': 'int',
   'bindusankhaya': 'float',
   'lekh': 'str',
   'sach': 'True',
   'jhoot': 'False',
   'kuchNahi': 'None'
}

def preprocess_code(code):
    pattern = re.compile(r'\b(' + '|'.join(custom_keywords.keys()) + r')\b')
    preprocessed_code = pattern.sub(lambda x: custom_keywords[x.group()], code)
    return preprocessed_code

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    code = data.get('code', '')
    preprocessed_code = preprocess_code(code)
    
    temp_file = 'temp_code.py'
    exec_command = ['python', temp_file]

    try:
        with open(temp_file, 'w') as file:
            file.write(preprocessed_code)
        result = subprocess.run(exec_command, capture_output=True, text=True)
        output = result.stdout
        errors = result.stderr
    except Exception as e:
        output = ""
        errors = str(e)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return jsonify({'output': output, 'errors': errors})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
