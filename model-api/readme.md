# Model training

The model api simply gets the latest model from the mock blob storage (node filesystem volume) and predicts requests on the `/predict` endpoint

## Local testing

```bash
#start api
API_HOST="localhost" API_PORT="5000" MODEL_PATH="../model-training/data/" python model-api.py


# test api 
curl -X POST -H "Content-Type: application/json" \
-d '{"row": [ 2, 5, 11, 10, 4 ]}' \
http://localhost:5000/predict
```

## Building

`docker build -t model-api .`

## Deploying

`kubectl apply -f model-api.yaml`
`kubectl delete -f model-api.yaml`

## Getting predictions

```bash
# test api 
curl -X POST -H "Content-Type: application/json" \
-d '{"row": [ 2, 5, 11, 10, 4 ]}' \
http://localhost:30004/predict
```