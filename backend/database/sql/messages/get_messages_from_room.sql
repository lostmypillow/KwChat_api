-- Get messages from the room (1-on-1/ group)
SELECT
    *
FROM
    messages
WHERE
    room_id = :room_id
ORDER BY
    timestamp ASC;