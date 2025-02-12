UPDATE
    users
SET
    name = :new_name,
    image = :new_image
WHERE
    user_id = :user_id;