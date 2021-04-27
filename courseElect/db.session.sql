SELECT C.id id,
	C.name name,
	C.credit credit,
	C.cid cid,
	C.depart depart,
	T.id tuid,
	T.tid tid,
	T.name tname,
	A.avg
FROM course_course C
	JOIN teacher_teacher T on T.id = C.keys_tid_id
	JOIN (
		SELECT avg(grade) avg,
			cid_id cid
		FROM election_election
		GROUP BY cid_id
	) A on A.cid = C.id
WHERE T.id = 5