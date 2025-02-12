-- Remove a user from a room
DELETE FROM
    room_users
WHERE
    room_id = :room_id
    AND user_id = :user_id;