import ConfigParser, logging, datetime, os, json

from flask import Flask, render_template, request

import mediacloud

CONFIG_FILE = 'settings.config'
basedir = os.path.dirname(os.path.realpath(__file__))

# load the settings file
config = ConfigParser.ConfigParser()
config.read(os.path.join(basedir, 'settings.config'))

# set up logging
logging.basicConfig(level=logging.DEBUG)
logging.info("Starting the MediaCloud example Flask app!")

# clean a mediacloud api client
mc = mediacloud.api.MediaCloud( config.get('mediacloud','api_key') )

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("search-form.html")


@app.route("/search",methods=['POST'])
def search_results():
    keywords = request.form['keywords']
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    # now = datetime.datetime.now()
    results = mc.sentenceCount(keywords,
                                solr_filter=[mc.publish_date_query(datetime.datetime.strptime(start_date, "%Y-%m-%d"),
                                                                   datetime.datetime.strptime(end_date, "%Y-%m-%d")),
                                            'tags_id_media:9139487'],
                                split=True,
                                split_start_date=start_date,
                                split_end_date=end_date)
    print(json.dumps(results['split'], indent=4, separators=(',', ': ')))
    clean_data = {}
    for key in results['split']:
        # if a date, append to clean_data dict
        if len(key.encode('utf-8')) > 5:
            clean_data[key.encode('utf-8')] = results['split'][key]

    # print(type(key.encode('utf-8')))
    # print(json.dumps(clean_data))
    # print(type(clean_data))
    # print(type(json.dumps(clean_data)))
    # print(type(json.loads(json.dumps(clean_data))))
    return render_template("search-results.html",
                           keywords=keywords,
                           sentenceCount=results['count'],
                           weeklyResults=json.dumps(clean_data))

if __name__ == "__main__":
    app.debug = True
    app.run()
