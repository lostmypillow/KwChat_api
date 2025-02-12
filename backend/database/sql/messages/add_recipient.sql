-- Add recipients for the message (1-on-1 + group)
INSERT INTO
    message_recipients (message_id, user_id, delivered, read)
SELECT
    :message_id,
    user_id,
    0,
    0
FROM
    room_users
WHERE
    room_id = :room_id;