import praw
import config
import psycopg2
import sys

top_subreddit_list = ['AskReddit', 'funny', 'gaming', 'aww', 'worldnews']
countries_subreddit_list = ['india', 'usa', 'unitedkingdom', 'australia', 'russia', 'China']


class PostgresDb:
    def __init__(self):
        self.hostname = config.Postgres.hostname
        self.database = config.Postgres.database
        self.username = config.Postgres.username
        self.pwd = config.Postgres.pwd
        self.port_id = config.Postgres.port_id
        self.conn = None
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(
            host=self.hostname, 
            database=self.database, 
            user=self.username, 
            password=self.pwd, 
            port=self.port_id
            )

            print(f"Connected to {self.database} Database")
        
        except Exception as error:
            print(error)
            sys.exit(1)
    
    def disconnect(self):
        if self.conn:
            self.conn.close()
            print(f"Disconnected from {self.database} database!")
    
    def execute_query(self, query, params=None):
        if self.conn is None:
            print("Not connected to a database")
            return
        
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
   
                results = cursor.fetchall()   
                self.conn.commit()
                return results
            
        except Exception as e:
            print(f"Error executing the query: {e}")

    def execute_insert_query(self, query, params=None):
        if self.conn is None:
            print("Not connected to a database")
            return
        
        try:
            with self.conn.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)                  
                self.conn.commit()
                print("row inserted")
                return
        except Exception as e:
            print(f"Error executing the query: {e}")
class RedditProducer:

    def __init__(self):
        self.reddit = self.__get_reddit_client__()

    def __get_reddit_client__(self) -> praw.Reddit:
        
        try:
            client_id = config.Reddit.client_id
            client_secret = config.Reddit.client_secret
            user_agent = config.Reddit.user_agent
        except:
            raise ValueError("The config file does not contain a reddit credentials.")
        
        return praw.Reddit(
            user_agent = user_agent,
            client_id = client_id,
            client_secret = client_secret
        )

    def start_stream(self, subreddit_name) -> None:
        subreddit = self.reddit.subreddit(subreddit_name)
        #comment: praw.models.Comment
        for comment in subreddit.stream.comments(skip_existing=True):
            try:
                comment_json = {
                    "id": comment.id,
                    "name": comment.name,
                    "link_id": comment.link_id,
                    "parent_id": comment.parent_id,
                    "author": comment.author.name,
                    "body": comment.body,
                    "subreddit": comment.subreddit.display_name,
                    "subreddit_id" : comment.subreddit.id,
                    "upvotes": comment.ups,
                    "downvotes": comment.downs,
                    "score": comment.score,
                    "over_18": comment.over_18,
                    "timestamp": comment.created_utc,
                    "permalink": comment.permalink,
                }
                
                insert_query = "INSERT INTO comments (id, name,link_id, parent_id,author, body, subreddit, subreddit_id, upvotes,downvotes, score ,over_18 , timestamp , permalink) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s, %s, %s,%s );"
                data_to_insert = (comment_json["id"], 
                                  comment_json["name"], 
                                  comment_json["link_id"], 
                                  comment_json["parent_id"], 
                                  comment_json["author"], 
                                  comment_json["body"], 
                                  comment_json["subreddit"], 
                                  comment_json["subreddit_id"], 
                                  comment_json["upvotes"], 
                                  comment_json["downvotes"],
                                  comment_json["score"],  
                                  comment_json["over_18"], 
                                  comment_json["timestamp"], 
                                  comment_json["permalink"])
                
                db.execute_insert_query(insert_query, data_to_insert)
                
            except Exception as e:
                print("An error occurred:", str(e))
    

if __name__ == "__main__":
    
    #intiate database class
    db = PostgresDb()

    #connect to db
    db.connect()

    #initiate reddit_producer class
    reddit_producer = RedditProducer()

    #begin stream of selected subreddit
    reddit_producer.start_stream('AskReddit')
    
    #disconnect from db
    #db.disconnect()