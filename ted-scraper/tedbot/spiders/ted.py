import json
import re
import scrapy

from bs4 import BeautifulSoup
from urllib.parse import urljoin

from ..items import Speaker, Talk


class TEDSpider(scrapy.Spider):
    name = 'ted'
    start_urls = (
        'https://www.ted.com/talks',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_talks)

    def parse_talks(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # Follow link to next page, if present
        next_page = soup.find('a', rel='next')
        if next_page:
            yield scrapy.Request(urljoin(response.url, next_page['href']),
                                 callback=self.parse_talks)

        # Follow links to search results (talks)
        results = soup.find('div', 'results')
        if results:
            for x in results.find_all('a', 'ga-link'):
                yield scrapy.Request(urljoin(response.url, x['href']),
                                     callback=self.parse_talk)

    def parse_talk(self, response):
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract JavaScript blurb, and parse its argument as JSON
        js_text = next(x.text for x in soup.find_all('script')
                       if 'talkPage.init' in x.text)
        json_info = json.loads(re.findall(r'({.+})', js_text, re.MULTILINE)[0])
        talk_info = json_info['talks'][0]

        talk = Talk()
        talk['id'] = str(talk_info['id'])
        talk['url'] = json_info['url']
        talk['title'] = talk_info['title']
        talk['description'] = talk_info['description']
        talk['event'] = talk_info['event']
        talk['duration'] = talk_info['duration']
        talk['filmed_at'] = talk_info['player_talks'][0]['filmed']
        talk['published_at'] = talk_info['player_talks'][0]['published']
        talk['tags'] = talk_info['tags']
        talk['viewed'] = talk_info['viewed_count']
        talk['ratings'] = {x['name']: x['count'] for x in talk_info['ratings']}

        # Build list of speakers, simultaneously yielding Speaker objects
        talk['speakers'] = []
        for x in talk_info['speakers']:
            speaker = Speaker()
            speaker['id'] = str(x['id'])
            speaker['first_name'] = x['firstname']
            speaker['last_name'] = x['lastname']
            speaker['description'] = x['description']
            speaker['bio'] = x['whotheyare']
            talk['speakers'].append(speaker['id'])
            yield speaker

        # Extract external links
        external_links = []
        if talk_info['more_resources']:
            external_links.extend(x['link_url']
                                  for x in talk_info['more_resources'])
        if talk_info['recommendations']:
            for l in talk_info['recommendations']['rec_lists']:
                external_links.extend(x['link_url'] for x in l['rec_items'])

        # Filter out empty URLs, and remove duplicates
        external_links = list({x for x in external_links if len(x) != 0})

        talk['external_links'] = external_links

        yield talk
