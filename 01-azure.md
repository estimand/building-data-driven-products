# Azure setup

## Set up the Azure CLI

1. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/free) before you begin
1. Install the latest version of the [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) and [log into your Azure account](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli)
1. If you have multiple subscriptions, select the one you'd like to use as default:
   ```bash
   az account set --subscription "Azure Internal - London"
   ```
   You can list your subscriptions using `az account list --output table`

## Create a resource group

1. Create a resource group in a suitably close location:
   ```bash
   az group create --location uksouth --name "gicampan-data-prod"
   ```
   You can list all available locations using `az account list-locations --output table`
