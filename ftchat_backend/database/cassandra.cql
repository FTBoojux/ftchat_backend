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
)WITH CLUSTERING ORDER BY (TIMESTAMP DESC,message_id ASC);