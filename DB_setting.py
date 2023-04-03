import pymysql

def basicProcess(sql, flag):
    db = pymysql.connect(host='52.78.193.207', port=55690, user='user', passwd='passwd', db='membership', charset='utf8')

    cursor = db.cursor()

    cursor.execute(sql)

    if(flag == 1):
        data = cursor.fetchall()

        db.commit()
        db.close()

        return data
    else:
        db.commit()
        db.close()

def getLoginData(id, password):
    sql = """
        SELECT nickname FROM account WHERE id='{}' AND pw=SHA2('{}', 512);
        """.format(id, password)

    data = basicProcess(sql, 1)

    if(data):
        return True, data[0][0]
    else:
        return False, None

def checkIDUnique(id):
    sql = """
        SELECT * FROM account WHERE id='{}';
        """.format(id)

    data = basicProcess(sql, 1)

    if(data):
        return False
    else:
        return True
    
def checkNicknameUnique(nickname):
    sql = """
        SELECT * FROM account WHERE nickname='{}';
        """.format(nickname)

    data = basicProcess(sql, 1)

    if(data):
        return False
    else:
        return True

def setMembership(id, password, email, nickname):
    sql = """
        INSERT INTO account (id, pw, email, nickname) VALUES('{}', SHA2('{}', 512),'{}','{}');
        """.format(id, password, email, nickname)

    basicProcess(sql, 0)

    sql = """
        INSERT INTO custom_setting (nickname, bookmark, history, download, metadata, cookie, cache, session) VALUES('{}','1','1','1','1','1','1','1');
        """.format(nickname)

    basicProcess(sql, 0)

def resetPw(newPw, nickname):
    sql="""
    UPDATE account 
    SET pw= hex(aes_encrypt('{}','ONabWBfohZuMburw'))
    WHERE nickname='{}'
    """.format(newPw, nickname)

    basicProcess(sql, 0)

def getID(nickname):
    sql = """
        SELECT id FROM account WHERE nickname='{}';
        """.format(nickname)

    data = basicProcess(sql, 1)

    if(data):
        return True, data[0][0]
    else:
        return False, None
    
def getEmail(id, nickname):
    sql = """
        SELECT email FROM account WHERE id='{}' AND nickname='{}';
        """.format(id, nickname)
    
    data = basicProcess(sql, 1)

    if data:
        return True, data[0][0]
    else:
        return False, None

def setCustomSetting(bookmarkCheck, visitCheck, downloadCheck, autoFormCheck, cookieCheck, cacheCheck, sessionCheck, nickname):
    sql="""
    UPDATE custom_setting 
    SET bookmark='{}', history='{}', download='{}', metadata='{}', cookie='{}', cache='{}', session='{}'
    WHERE nickname='{}'
    """.format(bookmarkCheck, visitCheck, downloadCheck, autoFormCheck, cookieCheck, cacheCheck, sessionCheck, nickname)

    data = basicProcess(sql, 0)

def getCustomSetting(nickname):
    sql="""
    SELECT bookmark, history, download, metadata, cookie, cache, session FROM custom_setting  WHERE nickname='{}';
    """.format(nickname)

    data = basicProcess(sql, 1)

    return data[0]