# Data analysis

**Previous**: [Scraper setup](03-scraper.md) | **Next**: [Web app setup](05-web-app.md)

## Create a DSVM

Create a [Data Science VM (DSVM)](https://docs.microsoft.com/en-gb/azure/machine-learning/data-science-virtual-machine/overview):
```bash
az vm create --name "gicampan-dsvm" \
             --image "microsoft-ads:linux-data-science-vm-ubuntu:linuxdsvmubuntu:latest" \
             --size "Standard_D8s_v3" \
             --generate-ssh-keys \
             --public-ip-address-dns-name "gicampan-dsvm"
```

## Set up access to JupyterHub

1. Allow inbound JupyterHub traffic on port 8000:
   ```bash
   az vm open-port --port 8000 --priority 1010 --name "gicampan-dsvm"
   ```
1. Log into the VM:
   ```bash
   ssh gicampan-dsvm.uksouth.cloudapp.azure.com
   ```
1. Clone this repository from GitHub:
   ```bash
   cd notebooks
   git clone https://github.com/estimand/building-data-driven-products.git
   ```
1. Set your password:
   ```bash
   sudo passwd `whoami`
   ```

## Analyse the data

1. Log in at [`https://gicampan-dsvm.uksouth.cloudapp.azure.com:8000/`](https://gicampan-dsvm.uksouth.cloudapp.azure.com:8000/)
1. Run through the notebooks

