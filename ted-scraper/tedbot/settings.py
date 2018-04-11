BOT_NAME = 'TEDBot'

SPIDER_MODULES = ['tedbot.spiders']

AUTOTHROTTLE_ENABLED = True

ITEM_PIPELINES = {
    'tedbot.pipelines.TimingsDownloaderPipeline': 100,
    'tedbot.pipelines.TranscriptDownloaderPipeline': 100,
    'tedbot.pipelines.CosmosDBSaverPipeline': 200,
}

COSMOSDB_ENDPOINT = '<Your Cosmos DB endpoint>'
COSMOSDB_KEY = '<Your Cosmos DB "primaryMasterKey">'
