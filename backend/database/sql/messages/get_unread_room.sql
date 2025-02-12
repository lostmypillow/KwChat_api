-- Get unread messages for a user in a room (1-on-1)
SELECT
    *
FROM
    messages
WHERE
    room_id = :room_id
    AND id IN (
        SELECT
            message_id
        FROM
            message_recipients
        WHERE
            user_id = :user_id
            AND read = 0
    );