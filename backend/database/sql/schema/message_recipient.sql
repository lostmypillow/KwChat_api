CREATE TABLE message_recipients (
    message_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    delivered INTEGER DEFAULT 0,
    read INTEGER DEFAULT 0,
    PRIMARY KEY (message_id, user_id),
    FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES room_users(user_id) ON DELETE CASCADE
);