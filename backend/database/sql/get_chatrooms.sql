SELECT
       c.id,
       (
              CASE
                     WHEN c.user1_id = :user_id THEN c.user2_id
                     ELSE c.user1_id
              END
       ) AS other_user_id
FROM
       chatrooms c
WHERE
       c.user1_id = :user_id
       OR c.user2_id = :user_id;