# RedditComments
## Project Overview

The Reddit Comments Pipeline is designed to collect comments from Reddit using the Reddit API and store the processed data in a PostgreSQL database. The pipeline leverages containerization using Docker.

**NOTE: This projectmay be effectd by the change to [Reddit API terms and policies](https://www.reddit.com/r/reddit/comments/12qwagm/an_update_regarding_reddits_api/). So far I have not encountered any issues but it is possible the use of the API may be restricted.**

# Installation and Setup

## System Requirements
- [Docker Engine](https://www.docker.com/)

To setup the pipeline locally, first you will have to add a config file for accessing reddit API, and with details for the Postgres database. II chose to do this with an accompanying config.py file, however storing as json or using a config parser are alternative options. The config.py file which i used following this template:

```python
class Reddit():
    client_id = 'client_id'
    client_secret = 'client_secret'
    user_agent = 'user_agent'

class Postgres():
    hostname = 'db'
    database = 'reddit'
    username = 'myuser'
    pwd = 'mypassword'
    port_id = '5432'
```

## Running

Once Docker is installed, it should be as simple as running the following docker command to being the pipeline:

docker-compose up -d


# To-Do / improvements 
- Add looping/threading mechanism to the reddit_producer script which allows multiple subreddits to be streamed concurrently
- Add wait and retry logic to database connection to avoid issues when python script tries to initial when Postgres has not completed setup (this happens regardless of docker-compose depends_on setting)
- Build in more data sources and model with dbt
- Add sentiment analysis to the comments
- Add update script to update the scores of comments for additional analysis

# Acknowledgements
