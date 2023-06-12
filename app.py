from flask import Flask, request, url_for, render_template, make_response
from markupsafe import escape
import urllib, urllib.request
import feedparser
import time
import logging
from werkzeug.utils import secure_filename
import os 

# Create the 'logs' directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO,
                    filename=os.path.join(logs_dir, 'logs.log'),
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

app = Flask(__name__)                           # define app using flask
base_url = 'http://export.arxiv.org/api/query?' # base api query url
wait_time = 3                                   # number of seconds to wait between calls

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return search()
    else:
        return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['search']
    logger.info(f'Query: {query}')
    url = f'{base_url}search_query=all:{query}'

    try:
        response = urllib.request.urlopen(url).read()
        feed = feedparser.parse(response)
        logger.info('API response received')
        parse(feed)
        return render_template('podcast.html', query=query, results=feed)
    except Exception as e:
        logger.error(f'API request failed: {e}')
        return render_template('error.html')


def parse(feed):
    logger.info(f'Feed title: {feed.feed.title}')
    logger.info(f'Feed last updated: {feed.feed.updated}')

    logger.info(f'totalResults for this query: {feed.feed.opensearch_totalresults}')
    logger.info(f'itemsPerPage for this query: {feed.feed.opensearch_itemsperpage}')
    logger.info(f'startIndex for this query: {feed.feed.opensearch_startindex}')

    for entry in feed.entries:
        logger.info('e-print metadata')
        logger.info(f'arxiv-id: {entry.id.split("/abs/")[-1]}')
        logger.info(f'Published: {entry.published}')
        logger.info(f'Title: {entry.title}')

        author_string = entry.author
        try:
            author_string += ' (%s)' % entry.arxiv_affiliation
        except AttributeError:
            pass
        logger.info(f'Last Author: {author_string}')

        try:
            authors = ', '.join(author.name for author in entry.authors)
            logger.info(f'Authors: {authors}')
        except AttributeError:
            pass

        for link in entry.links:
            if link.rel == 'alternate':
                logger.info(f'abs page link: {link.href}')
            elif link.title == 'pdf':
                logger.info(f'pdf link: {link.href}')

        try:
            journal_ref = entry.arxiv_journal_ref
        except AttributeError:
            journal_ref = 'No journal ref found'
        logger.info(f'Journal reference: {journal_ref}')

        try:
            comment = entry.arxiv_comment
        except AttributeError:
            comment = 'No comment found'
        logger.info(f'Comments: {comment}')

        logger.info(f'Primary Category: {entry.tags[0]["term"]}')

        all_categories = ', '.join(t['term'] for t in entry.tags)
        logger.info(f'All Categories: {all_categories}')

        logger.info(f'Abstract: {entry.summary}')

if __name__ == '__main__':
    app.run(debug=True)


# flask --app app run --debug
