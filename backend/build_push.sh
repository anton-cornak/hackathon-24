az acr login --name crhackathonassistant
docker build --push --network host --platform linux/amd64 --tag crhackathonassistant.azurecr.io/hackathon-api:latest .
echo "Container app revision needs to be manually restarted for changes to take effect"