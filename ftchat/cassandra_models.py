class GptMessage:
    def __init__(self, message_id, sender, receiver, content_type, content, sent_at, read, sentiment_analysis_result):
        self.message_id = message_id
        self.sender = sender
        self.receiver = receiver
        self.content_type = content_type
        self.content = content
        self.sent_at = sent_at
        self.read = read
        self.sentiment_analysis_result = sentiment_analysis_result


    def __repr__(self):
        return f"<GptMessage {self.message_id}>"