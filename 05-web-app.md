# Web app setup

**Previous**: [Data analysis](04-analysis.md) | **Next**: [Clean up](06-cleanup.md)

## Build a Docker image

1. Move to the app folder and update the configuration file `app/tedapp/config.py` using the values you retrieved during [database setup](02-db-setup.md):

   | Variable            | Value                             |
   | ------------------- | --------------------------------- |
   | `COSMOSDB_ENDPOINT` | Your Cosmos DB endpoint           |
   | `COSMOSDB_KEY`      | Your Cosmos DB `primaryMasterKey` |

   In addition, set `SECRET_KEY` to the output of the following command:
   ```python
   import os
   os.urandom(24)
   ```
1. Build a Docker image:
   ```bash
   docker build --network=host -t tedapp .
   ```
1. Run the Docker image in a container:
   ```bash
   docker run -d --name tedcontainer --network=host tedapp
   ```
1. Verify that you can access the app at [http://localhost](http://localhost)
1. Stop and remove the container:
   ```bash
   docker container stop tedcontainer
   docker container rm tedcontainer
   ```

## Upload the Docker image to Container Registry

1. Create a new container registry:
   ```bash
   az acr create --name gicampanacr --sku Basic --admin-enabled true
   ```
1. Retrieve the name of the login server:
   ```bash
   az acr list --query "[].{acrLoginServer:loginServer}" --output table
   ```
1. Log in:
   ```bash
   az acr login --name gicampanacr
   ```
1. Tag the Docker image:
   ```bash
   docker tag tedapp gicampanacr.azurecr.io/tedapp:v1
   ```
1. Push the Docker image to the container registry:
   ```bash
   docker push gicampanacr.azurecr.io/tedapp:v1
   ```
1. Verify that the image was successfully uploaded:
   ```bash
   az acr repository list --name gicampanacr --output table
   ```

## Run the app on App Service

1. Create an App Service plan:
   ```bash
   az appservice plan create --name gicampan-service-plan --is-linux --sku B1
   ```
1. Create a Web App:
   ```bash
   az webapp create --name gicampan-ted-explorer \
                    --plan gicampan-service-plan \
                    --deployment-container-image-name gicampanacr.azurecr.io/tedapp
   ```
1. Retrieve your Container Registry credentials:
   ```bash
   ACR_CREDENTIALS=$(az acr credential show --name gicampanacr)
   ACR_USERNAME=$(echo $ACR_CREDENTIALS | jq -r '.username')
   ACR_PASSWORD=$(echo $ACR_CREDENTIALS | jq -r '.passwords[0].value')
   ```
1. Pass the credentials to the Web App:
   ```bash
   az webapp config container set --name gicampan-ted-explorer \
                                  --docker-custom-image-name gicampanacr.azurecr.io/tedapp:v1 \
                                  --docker-registry-server-url https://gicampanacr.azurecr.io \
                                  --docker-registry-server-user $ACR_USERNAME \
                                  --docker-registry-server-password $ACR_PASSWORD
   ```
1. Access the app at [https://gicampan-ted-explorer.azurewebsites.net](https://gicampan-ted-explorer.azurewebsites.net)
