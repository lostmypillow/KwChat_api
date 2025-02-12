-- Get all rooms a user is in
SELECT
    room_id
FROM
    room_users
WHERE
    user_id = :user_id;