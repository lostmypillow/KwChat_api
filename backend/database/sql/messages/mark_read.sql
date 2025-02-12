UPDATE
    message_recipients
SET
    read = 1
WHERE
    message_id = :message_id
    AND user_id = :user_id;