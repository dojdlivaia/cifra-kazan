#авторизуем врача (guid_prov) и пациента (text - номер полиса)
def add_recipe(text, guid_prov, conn, database):
    with conn:
        cursor = conn.cursor()
        data = [(None, text,guid_prov)]
        cursor.execute("INSERT INTO recipe VALUES (?,?,?)", data)
        conn.commit()
    return None


def find_medicine(text, guid_prov, conn, database):
    cursor = conn.cursor()
    sql="SELECT id_recipe FROM recipe"
    cursor.execute(sql)
    #возвращаем id_rec из таблицы id_recipe
    id_rec=cursor.fetchall()[-1][0]
    with open("lp2019.json", "rb") as f:
        jsonfile = f.read().decode("utf_8_sig")
    l= text.lower().replace('.','').split()
    fl=True
    sum=0
    Naznacheno=''
    for stroka in json.loads(jsonfile):
        #Если название препарата есть в списке сказанных слов
            if stroka['MNN'].lower() in l:
               Naznachenie+=stroka['MNN']+' '
               #удаляем пробелы, меняем запятые на точки
               sum+=float(stroka['Price'].replace(' ','').replace(',','.'))
               #пишем новую строчку в базу
               product = [(None, stroka["Barcode"],id_rec, stroka['MNN'],
                      stroka['Count'], stroka['Price'],stroka['ReleaseForm'],text)]
               cursor.executemany("INSERT INTO recipe_product VALUES (?,?,?,?,?,?,?,?)", product)
               conn.commit()
               #удаляем название препарата
               l.remove(stroka['MNN'].lower())
               fl=False
    if fl:
        answer=['Не знаю такого лекарства. Может подорожник?',
            'Не знаком с таким препаратом. Повторите, пожалуйста!',
            'Не расслышал название препарата. Давайте поцелую и всё пройдёт!']
        response=random.choice(answer)
    else:
        response=('Вам назначено:'+Naznachenie+'Сумма вашего заказа ориентировочно '+str(int(sum*1.1))+' рублей')
    return response