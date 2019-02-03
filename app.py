from flask import Flask, Markup, render_template, jsonify

import pandas as pd
from requests_html import HTMLSession
import os
import json
import re

app = Flask(__name__)

@app.route('/<sys_name>', methods=['GET'])
# TBD динамическая генерация страниц в зависимости от имени системы в URL
# сейчас темплэйт есть только для Транзакта
def table(sys_name):
    print(sys_name)
    template = "table_" + sys_name + ".html"

    ### получаем JSON с данными по кластерам 
    # data = get_data_from_elastic()
    data = get_data_from_file()
    ###

    colnames = data['columns']
    data = purify_cluster_data(data['data']) # delicious naming

    return render_template(template, name = sys_name, colnames = colnames, data=data)

@app.route('/data')
def generate_data():
    data = pd.read_csv('trash_tmp/pivot_0.01_0.9.csv', sep=';')
    data = data.fillna(0)
    data = data.to_json(orient='split')
    return data

def get_data_from_elastic():
    # кусок кода по получению json из URL рабочий, но Flask не умеет читать сам с себя
    session = HTMLSession()
    elastic_url = 'http://127.0.0.1:5000/data'
    r = session.get(elastic_url)
    rr = r.json()
    rr = r.text
    return rr

def get_data_from_file():
    json_data = open('trash_tmp/data.json').read()
    data = json.loads(json_data)
    return data

def purify_cluster_data(data):
    for cluster in data:
        # дописываю названия кластеров без пробелов, чтобы использовать их в параметре
        # не стал делать этого в темплейте        
        cluster[0] = re.sub(' ','_',cluster[0])
        for i, v in enumerate(cluster):
            if isinstance(v, float):
                cluster[i] = int(v)
    return data

