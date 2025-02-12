SELECT
    user_id
FROM
    message_recipients
WHERE
    message_id = :message_id
    AND read = 0;