FROM bitnami/kubectl:1.28.2

WORKDIR /app

COPY config.yaml /app/
COPY model-api.yaml /app/

ENV KUBECONFIG=/app/config.yaml

CMD [ "apply", "-f", "model-api.yaml" ]