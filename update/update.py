#!/usr/bin/env python3

import requests
import csv
from datetime import date, datetime
import json

today = date.today().isoformat()
features = ['confirmados', 'decesos', 'recuperados', 'sospechosos', 'descartados']
departamentos = {'lp': 'La Paz', 'cb': 'Cochabamba', 'sc': 'Santa Cruz', 'or': 'Oruro', 'pt': 'Potosí', 'tj': 'Tarija', 'ch': 'Chuquisaca', 'bn': 'Beni', 'pn': 'Pando'}
locations = {'La Paz':[-15.0,-68.333333],
             'Cochabamba':[-17.333333,-65.5],
             'Santa Cruz':[-17.33333333,-61.5],
             'Oruro':[-18.666666666,-67.666666666],
             'Potosí':[-20.66666667,-66.66666667],
             'Tarija':[-21.583333333, -63.833333333],
             'Chuquisaca':[-20.0,-64.416666666],
             'Beni':[-14.0,-65.0],
             'Pando':[-11.183333333,-67.183333333]}
header = ['Fecha'] + [departamentos[d] for d in departamentos.keys()]
updated = {'number': 0, 'message': ''}

def format_by_feature(data, features):
  return {feature:{departamentos[dep]:str(data[dep]['contador'][feature]) for dep in data.keys()} for feature in features}

def format_total(data, features, fecha):
  now = datetime.strptime(fecha, '%d/%m/%y %H:%M').isoformat()
  return {departamentos[d]: [now, str(data[d]['contador']['confirmados']), str(data[d]['contador']['decesos']), str(data[d]['contador']['recuperados'])]for d in data.keys()}
  
def read_old_features():
  archived = {}
  for feature in features:
    with open(feature + '.csv', 'r') as csvfile:
      archived[feature] = [dict(row) for row in list(csv.DictReader(csvfile, fieldnames=header))[1:]]
  return archived

def is_new_day(old_data):
  return old_data[features[0]][0]['Fecha'] != today

def update_json(data):
  json_data = {feature: [{"fecha": dia['Fecha'], 'dep': {d.lower().replace(" ", "_"): int(dia[d])for d in [departamentos[d] for d in departamentos.keys()]}} for dia in data[feature]] for feature in features}
  with open('data.json', 'w+') as f:
    json.dump(json_data, f, ensure_ascii=False)

def new_row(old_data, new_data):
  for feature in features:
    new_data[feature]['Fecha'] = today
    old_data[feature].insert(0, new_data[feature])
    save_feature(feature, old_data)
    updated['number'] += 1
  updated['message'] = 'nuevo día'
  update_json(old_data)

def save_feature(feature, data):
  with open(feature + '.csv', 'w+') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for dia in data[feature]:
      writer.writerow(dia)

def any_new_features(new, old):
  updated_features = []
  for feature in features:
    for dep in new[feature].keys():
      if new[feature][dep] != old[feature][0][dep]:
        new[feature]['Fecha'] = today
        old[feature][0] = new[feature]
        save_feature(feature, old)
        updated['number'] += 1
        updated_features.append(feature)
        break
  updated['message'] = ', '.join(updated_features)
  if len(updated_features) > 0:
    update_json(old)

def save_total(data):
  headers2 = ['Province/State', 'Country/Region', 'Last Update', 'Confirmed', 'Deaths', 'Recovered', 'Latitude', 'Longitude']
  with open('total.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers2)
    for d in data.keys():
      writer.writerow([d, 'Bolivia'] + data[d] + locations[d])

def read_old_total():
  with open('total.csv', 'r') as csvfile:
    return {d[0]: d[2:6]for d in list(csv.reader(csvfile))[1:]}
      
def any_new_total(new, old):
  changed = []
  for d in old.keys():
    if old[d][1:] != new[d][1:]:
      old[d] = new[d]
      changed.append(d)
  if len(changed) > 0:
    save_total(old)
    updated['message'] = updated['message'] + ' en ' + ', '.join(changed)

def what_changed():
  print(json.dumps(updated, ensure_ascii=False))

def update_features(response):
  by_feature = format_by_feature(response['departamento'], features)
  old_features = read_old_features()
  if is_new_day(old_features):
    new_row(old_features, by_feature)
  else:
    any_new_features(by_feature, old_features)

def update_total(response):
  total = format_total(response['departamento'], features, response['fecha'])
  old_total = read_old_total()
  any_new_total(total, old_total)
    
def init():
  url = 'https://www.boliviasegura.gob.bo/wp-content/json/api.php'
  response = requests.get(url).json()
  update_features(response)
  update_total(response)
  what_changed()
    
init()
