import pymysql

def basicProcess(sql, flag):
    db = pymysql.connect(host='43.201.104.255', port=57892, user='user', passwd='passwd', db='membership', charset='utf8')

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
        SELECT nickname FROM account WHERE id='{}' AND pw=hex(aes_encrypt('{}','ONabWBfohZuMburw'));
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

def setMembership(id, password, nickname):
    sql = """
        INSERT INTO account (id, pw, nickname) VALUES('{}', hex(aes_encrypt('{}','ONabWBfohZuMburw')),'{}');
        """.format(id, password, nickname)

    basicProcess(sql, 0)

    sql = """
        INSERT INTO custom_setting (nickname, bookmark, history, download, metadata, cookie, cache, session) VALUES('{}','1','1','1','1','1','1','1');
        """.format(nickname)

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

def getPW(id, nickname):
    sql = """
        SELECT aes_decrypt(unhex(pw),'ONabWBfohZuMburw') FROM account WHERE id='{}' AND nickname='{}';
        """.format(id, nickname)

    data = basicProcess(sql, 1)

    if(data):
        return True, data[0][0].decode('ascii')
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