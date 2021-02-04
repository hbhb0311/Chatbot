#%% 테이블 생성
import pymysql

db = None

try:
    db = pymysql.connect(
        host = '',
        port = ,
        user = '',
        password = '',
        database = '',
        charset = 'utf8')
    print('DB 연결 성공')

    sql ='''
    CREATE TABLE tb_student(
    id int primary key auto_increment not null,
    name varchar(32),
    age int,
    address varchar(32)
    )ENGINE = innoDB DEFAULT CHARSET = utf8
    '''

    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 연결 닫기 성공')


#테이블에 인자 추가#
import pymysql

db = None

try:
    db = pymysql.connect(
        host='',
        port=,
        user='',
        password='',
        database='',
        charset='utf8')
    print('DB 연결 성공')

    sql ='''
    INSERT tb_student(name, age, address) values('hyebin', 20, 'Korea')'''

    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 연결 닫기 성공')


#인자업데이트#
import pymysql

db = None

try:
    db = pymysql.connect(
        host='',
        port=,
        user='',
        password='',
        database='',
        charset='utf8')
    print('DB 연결 성공')

    id = 1
    sql ='''
    UPDATE tb_student set name = "parkhyebin", age = 25 where id = %d ''' %id

    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 연결 닫기 성공')

#인자삭제#
import pymysql

db = None

try:
    db = pymysql.connect(
        host='',
        port=,
        user='',
        password='',
        database='',
        charset='utf8')
    print('DB 연결 성공')

    id = 3
    sql ='''
    DELETE from tb_student where id = %d ''' %id

    with db.cursor() as cursor:
        cursor.execute(sql)
    db.commit()

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 연결 닫기 성공')


#다수의데이터삽입#
import pymysql
import pandas as pd

db = None

try:
    db = pymysql.connect(
        host='',
        port=,
        user='',
        password='',
        database='',
        charset='utf8')
    print('DB 연결 성공')

    students = [
        {'name': 'hyebin', 'age': 36, 'address': 'SEOUL'},
        {'name': 'hye', 'age': 22, 'address': 'Ulsan'},
        {'name': 'bbb', 'age': 31, 'address': 'ANYANG'},
        {'name': 'ccc', 'age': 27, 'address': 'PUSAN'},
    ]
    for s in students:
        with db.cursor() as cursor:
            sql ='''
            INSERT tb_student(name, age, address) values("%s", "%d", "%s") 
            ''' % (s['name'], s['age'], s['address'])
            cursor.execute(sql)
    db.commit()

    cond_age = 30
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql =''' select * from tb_student where age > %d ''' % cond_age

        cursor.execute(sql)
        results = cursor.fetchall()
    print(results)

    cond_name = 'hye'
    with db.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = '''
        select * from tb_student where name = "%s" ''' % cond_name
        cursor.execute(sql)
        result = cursor.fetchone()
    print(result['name'], result['age'])

    df = pd.DataFrame(results)
    print(df)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
        print('DB 연결 닫기 성공')