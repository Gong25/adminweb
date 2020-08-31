from . import db

def select_member_by_db(username,password):
    return db.select_one('''
    SELECT *
    FROM login
    WHERE name=? AND passwd=?
    ''',(username,password))

def add_member(name,age,phone):
    return db.execute_commit('''
            INSERT INTO member (name, age, phone)
            VALUES (? , ? , ?)
            ''',(name,age,phone))

def del_member(no):
    return db.execute_commit('DELETE FROM member WHERE idx=?',(no,))