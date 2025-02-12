-- Add a user to a room
INSERT INTO
    room_users (room_id, user_id)
VALUES
    (:room_id, :user_id);