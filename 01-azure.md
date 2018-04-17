# Azure setup

**Next**: [Cosmos DB setup](02-cosmosdb.md)

## Set up the Azure CLI

Install the latest version of the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and [log into your Azure account](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli).

If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin.

## Select your subscription

If you have multiple subscriptions, select the one you'd like to use as default:
```bash
az account set --subscription "Azure Internal - London"
```

You can list your subscriptions using:
```bash
az account list --output table
```

## Create a resource group

Create a resource group in a suitably close location:
```bash
az group create --location uksouth --name "gicampan-data-prod"
```

You can list all available locations using:
```bash
az account list-locations --output table
```

## Set defaults

Configure the newly created resource group as default:
```bash
az configure --defaults group="gicampan-data-prod"
```
