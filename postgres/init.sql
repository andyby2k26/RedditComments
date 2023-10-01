-- Create the database
CREATE DATABASE reddit;

-- Connect to the database
\c reddit;

-- Create the comments table
CREATE TABLE comments (
    id varchar(255) PRIMARY KEY,
    name varchar(255),
    link_id varchar(255),
    parent_id varchar(255),
    author varchar(255),
    body TEXT,
    subreddit varchar(255),
    subreddit_id varchar(255),
    upvotes integer,
    downvotes integer,
    score  integer,
    over_18 varchar(255),
    timestamp bigint,
    permalink varchar(255)
);

