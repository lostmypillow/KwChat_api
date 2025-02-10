SELECT
    *
FROM
    messages
WHERE
    chat_id = :chat_id
ORDER BY
    timestamp ASC;