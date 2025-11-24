-- ChargeNow Case Study – Staging Model (Silver Layer)
-- Handles:
--   - Schema evolution (VARIANT JSON)
--   - Robust parsing
--   - Safe optional fields

with source as (

    select
        payload:author_id::string                                  as author_id,
        payload:created_at::timestamp_tz                           as tweet_datetime,

        -- hashtags can be absent or null → safe extraction
        payload:entities:hashtags                                  as hashtags_raw,

        payload:public_metrics:retweet_count::int                  as retweet_count,
        payload:public_metrics:reply_count::int                    as reply_count,
        payload:public_metrics:like_count::int                     as like_count,
        payload:public_metrics:quote_count::int                    as quote_count,

        payload:referenced_tweets                                  as referenced_tweets_raw

    from {{ source('raw', 'twitter_chargenow') }}

)

select *
from source;
