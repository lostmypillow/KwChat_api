SELECT
    m.*
FROM
    messages m
    JOIN message_recipients mr ON m.id = mr.message_id
WHERE
    mr.user_id = :user_id
    AND mr.read = 0;