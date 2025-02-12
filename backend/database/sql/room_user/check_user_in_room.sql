-- Check if a user is in a room
SELECT
    1
FROM
    room_users
WHERE
    room_id = :room_id
    AND user_id = :user_id;