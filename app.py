from flask import Flask, Markup, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/<sys_name>', methods=['GET'])
# TBD динамическая генерация страниц
def table(sys_name):
    template = "table_" + sys_name + ".html"
    data = get_data()
    return render_template(template, name = sys_name, colnames = colnames, data = data)

@app.route('/data')
def generate_data():
    data = pd.read_csv('trash_tmp/pivot_0.01_0.9.csv', sep=';')
    data = data.fillna(0)
    data = data.to_json(orient='split')
    return data

def get_data():
    
