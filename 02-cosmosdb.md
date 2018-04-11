# Cosmos DB setup

## Create resources

1. Create a Cosmos DB account within your resource group:
   ```bash
   az cosmosdb create --name "gicampan-cosmosdb" \
                      --resource-group "gicampan-data-prod"
   ```
1. Create a database within the account:
   ```bash
   az cosmosdb database create --db-name "ted" \
                               --name "gicampan-cosmosdb" \
                               --resource-group-name "gicampan-data-prod"
   ```

## Retrieve credentials

1. Retrieve your Cosmos DB endpoint:
   ```bash
   az cosmosdb list --resource-group "gicampan-data-prod" --output table
   ```
1. Retrieve your Cosmos DB keys:
   ```bash
   az cosmosdb list-keys --name "gicampan-cosmosdb" \
                         --resource-group "gicampan-data-prod"
   ```
