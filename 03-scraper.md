# Scraper setup

## Create resources

1. Create a VM for the scraper:
   ```bash
   az vm create --name "gicampan-scraper" \
                --resource-group "gicampan-data-prod" \
                --image UbuntuLTS \
                --size Standard_B1s \
                --generate-ssh-keys \
                --public-ip-address-dns-name "gicampan-scraper"
   ```
   You can list all available sizes using `az vm list-sizes --location uksouth --output table`

## Set up a `conda` virtual environment

1. Log into the VM:
   ```bash
   ssh gicampan-scraper.uksouth.cloudapp.azure.com
   ```
1. Download and install Miniconda:
   ```bash
   wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
   bash Miniconda3-latest-Linux-x86_64.sh -b
   ```
1. Clone this repository from GitHub and move to the scraper folder:
   ```bash
   git clone https://github.com/estimand/building-data-driven-products.git
   cd building-data-driven-products/ted-scraper
   ```
1. Create a new environment for the scraper:
   ```bash
   ~/miniconda3/bin/conda env create -f environment.yml
   ```

## Set up the scraper

1. Activate the environment:
   ```bash
   source ~/miniconda3/bin/activate tedbot
   ```
1. Update the configuration file `tedbot/settings.py` using the values you retrieved during [database setup](02-db-setup.md):

   | Variable            | Value                             |
   | ------------------- | --------------------------------- |
   | `COSMOSDB_ENDPOINT` | Your Cosmos DB endpoint           |
   | `COSMOSDB_KEY`      | Your Cosmos DB `primaryMasterKey` |
1. Start the scraper:
   ```bash
   scrapy crawl ted
   ```
