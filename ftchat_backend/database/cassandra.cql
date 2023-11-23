DROP TABLE IF EXISTS friend_requests;

CREATE TABLE IF NOT EXISTS friend_requests (
    requestee uuid,
    requester uuid,
    status text,
    timestamp timeuuid,
    text text,
    PRIMARY KEY (requestee, timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);

DROP TABLE IF EXISTS ft_chat.chat_message;

CREATE TABLE IF NOT EXISTS chat_message(
	conversation_id UUID,
	message_id UUID,
	sender_id UUID,
	timestamp TIMESTAMP,
	message_type INT,
	content TEXT,
	is_group_chat BOOLEAN,
	sentiment_analysis_result TEXT,
	PRIMARY KEY (conversation_id,message_id,timestamp)
)WITH CLUSTERING ORDER BY (message_id ASC,TIMESTAMP DESC);

DROP TABLE IF EXISTS gpt_message;

CREATE TABLE IF NOT EXISTS gpt_message(
    conversation_id text,
    srkey text,
    message_id text,
    content text,
    content_type int,
    read boolean,
    receiver text,
    send_at timestamp,
    sender text,
    sentiment_analysis_result text,
    PRIMARY KEY ((conversation_id, srkey), send_at)
) WITH CLUSTERING ORDER BY (send_at DESC);