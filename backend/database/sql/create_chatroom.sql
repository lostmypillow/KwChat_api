IF NOT EXISTS (
    SELECT
        1
    FROM
        chatrooms
    WHERE
        (
            user1_id = :user1_id
            AND user2_id = :user2_id
        )
        OR (
            user1_id = :user2_id
            AND user2_id = :user1_id
        )
) BEGIN
INSERT INTO
    chatrooms (user1_id, user2_id)
VALUES
    (:user1_id, :user2_id);

END;