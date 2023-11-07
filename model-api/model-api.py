import os
import glob
import joblib
import pandas as pd
import category_encoders as ce
from flask import Flask, request, jsonify
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

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
  request_data = request.get_json()
  if request_data is None:
    return jsonify({'error': 'Invalid JSON data'}), 400
  if 'row' not in request_data:
    return jsonify({'error': 'Invalid JSON data: "row" key missing'}), 400
  row = request_data['row']
  df = pd.DataFrame([row])
  df.columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety']
  df = ENCODER.transform(df)
  prediction = MODEL.predict(df)
  print(f"Prediction : {prediction[0]}")
  return jsonify({'prediction': prediction[0]}), 200


def main():
  global MODEL, ENCODER
  host = os.environ.get("API_HOST")
  port = os.environ.get("API_PORT")
  model_path = os.environ.get("MODEL_PATH")
  model_file = get_newest_model(model_path)
  MODEL = joblib.load(model_file)

  df_unique = pd.read_csv('unique.csv', header=None)
  df_unique.columns = ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety', 'class']
  df_unique.drop('class', axis=1, inplace=True)
  ENCODER = ce.OrdinalEncoder(cols=['buying', 'maint', 'doors', 'persons', 'lug_boot', 'car_safety'])
  ENCODER.fit(df_unique)
  
  app.run(debug=True, host=host, port=port)

if __name__ == '__main__':
  main()