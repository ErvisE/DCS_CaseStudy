-- dbt staging model for tweets (conceptual)
with source as (
    select
        payload:author_id::string          as author_id,
        payload:created_at::timestamp_tz   as tweet_datetime,
        payload:entities:hashtags          as hashtags_raw,
        payload:public_metrics:retweet_count::int  as retweet_count,
        payload:public_metrics:reply_count::int    as reply_count,
        payload:public_metrics:like_count::int     as like_count,
        payload:public_metrics:quote_count::int    as quote_count
    from raw.twitter_chargenow
)
select * from source;
