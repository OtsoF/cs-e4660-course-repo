import os
import glob
import joblib
import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_newest_model(directory):
  files = glob.glob(os.path.join(directory, '*'))
  if not files:
    print("No model found")
    exit(1)
  newest_file = max(files, key=os.path.getctime)
  return newest_file

@app.route('/predict', methods=['POST'])
def predict():
  print(request.get_json())
  request_data = request.get_json()
  if request_data is None:
    return jsonify({'error': 'Invalid JSON data'}), 400
  if 'row' not in request_data:
    return jsonify({'error': 'Invalid JSON data: "row" key missing'}), 400
  row = request_data['row']
  df = pd.DataFrame([row])
  col_names = ['ps_ind_01', 'ps_ind_02_cat', 'ps_ind_03',
      'ps_ind_04_cat', 'ps_ind_05_cat', 'ps_ind_14', 'ps_ind_15',
      'ps_car_01_cat', 'ps_car_02_cat','ps_car_03_cat', 'ps_car_06_cat']
  df.columns = col_names
  prediction = MODEL.predict(df)
  print(f"Prediction : {prediction[0]}")
  return jsonify({'prediction': str(prediction[0])}), 200


def main():
  global MODEL, ENCODER
  host = os.environ.get("API_HOST")
  port = os.environ.get("API_PORT")
  model_path = os.environ.get("MODEL_PATH")
  model_file = get_newest_model(model_path)
  MODEL = joblib.load(model_file)
  
  app.run(debug=True, host=host, port=port)

if __name__ == '__main__':
  main()