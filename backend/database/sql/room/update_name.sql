UPDATE
    rooms
SET
    room_name = :new_name
WHERE
    room_id = :room_id;