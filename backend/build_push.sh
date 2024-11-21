az acr login --name crhackathonassistant
docker build --push --network host --platform linux/amd64 --tag crhackathonassistant.azurecr.io/hackathon-api:latest .