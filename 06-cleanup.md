# Clean up

**Previous**: [Web app setup](05-web-app.md)

## Delete resources

Delete the resource group:
```bash
az group delete --name "gicampan-data-prod" --no-wait --yes
```

## Restore default settings

Reset the default resource group:
```bash
az configure --defaults group=""
```
