# RedditComments

#TODO
- Add looping/threading mechanism to the reddit_producer script which allows multiple subreddits to be streamed concurrently
- Add wait and retry logic to database connection to avoid issues when python script tries to initial when Postgres has not completed setup (this happens regardless of docker-compose depends_on setting)
