-- Get all users in a room
SELECT
    user_id
FROM
    room_users
WHERE
    room_id = :room_id;
