import streamlit as st
import sqlite3
import pandas as pd

filds = ['Создана', 'Номер договора', 'Адрес объекта оценки',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Площадь',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Год постройки',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Материал стен',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Этажность', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Отделка',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Комнатность',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м']

filds1 = ['ИНФОРМАЦИЯ ПО ОТЧЕТУ: Площадь',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Год постройки',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Материал стен',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Этажность', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Отделка',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Комнатность']

cities = ['','Красногорск', 'Видное', 'Одинцово', 'Люберцы', 'Мытищи', 'Балашиха',
        'Химки', 'Котельники', 'Домодедово', 'Солнечногорск', 'Пушкино',
        'Реутов', 'Щёлково', 'Подольск', 'Наро-Фоминск', 'Серпухов', 'Истра',
        'Долгопрудный', 'Дмитров', 'Раменское', 'Чехов', 'Королёв', 'Ногинск',
        'Жуковский', 'Орехово-Зуево', 'Сергиев Посад', 'Апрелевка',
        'Воскресенск', 'Лобня', 'Клин', 'Ступино', 'Дубна', 'Фрязино',
        'Электросталь', 'Железнодорожный', 'Лосино-Петровский', 'Лыткарино',
        'Кашира', 'Протвино', 'Краснознаменск', 'Коломна', 'Ивантеевка',
        'Хотьково', 'Руза', 'Талдом', 'Волоколамск', 'Звенигород', 'Бронницы',
        'Старая Купавна', 'Ликино-Дулёво', 'Краснозаводск', 'Егорьевск',
        'Красноармейск', 'Зарайск', 'Электрогорск', 'Черноголовка', 'Пущино',
        'Дедовск']








st.title('Название?')

main, load = st.tabs(['Таблица', 'Загрузить'])


with load:
    @st.cache_data
    def load_data(file):
        df = pd.read_excel(file)
        df.to_sql('info', con)
        
    file = st.file_uploader('Загрузите xlsx Файл')

    con = sqlite3.connect('tt.sqlite')
    cur = con.cursor()

    if file is not None:
        load_data(file)

with main:
    if "disabled" not in st.session_state:
        st.session_state["disabled"] = False

    def disable():
        if city == '':
            st.session_state["disabled"] = True
        else:
            st.session_state["disabled"] = False

    def districts(area):
        sql_d = f'SELECT "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area}" GROUP BY "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район"'
        d = [i[0] for i in cur.execute(sql_d).fetchall() if i[0] is not None]
        d.insert(0, 'ВСЕ')
        return d

    try:
        c1, c2, c3 = st.columns(3)
        with c1:
            city = st.selectbox('Город', cities, on_change = disable)
        with c2:
            area = st.selectbox('Округ', ['НАО', 'ЗАО', 'ЮВАО', 'САО', 'СЗАО', 'ЮАО', 'СВАО', 'ЦАО', 'ВАО','ЮЗАО', 'ЗелАО', 'ТАО'], disabled = st.session_state.disabled)
        with c3:
            district = st.selectbox('Район', districts(area), disabled = st.session_state.disabled)

        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            square = st.multiselect('Площадь', ['30-44', '45-65', '65-90', 'до 29', '90-140', '140+'])
            year = st.multiselect('Год постройки', ['2010+', '1954-1990', '1991-2010', '1920-1941', '1942-1953', 'до 1920'])

        with col2:
            material = st.multiselect('Материал стен', ['кирпич/монолит', 'панель'])
            floar = st.multiselect('Этажность', ['до 5 этажей', '6-25 этажей', '26 этажей +'])

        with col3:
            remont = st.multiselect('Отделка', ['простая', 'без отделки', 'евро'])
            rooms = st.multiselect('Комнатность', [1.0, 2.0, 3.0, 4.0, 5.0])

        st.divider()
        upload = st.button("Сохранить")



        if upload:
            # sql = 'SELECT * FROM info WHERE
            # pd.read_sql(sql, con, index_col=['index'])
            sql = 'SELECT "Создана", "Номер договора", "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м", "Адрес объекта оценки", '
            
            if st.session_state.disabled:
                sql += '"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город"'
            else:
                sql += '"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ", "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район"'
                
            sql += ''.join(f', "{i}"' for i in filds1)
            sql += ' FROM info WHERE '

            if st.session_state.disabled:
                sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город" = "{city}" AND '
            elif district == 'ВСЕ':
                sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area}" AND '
            else:
                sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area}" AND "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" = "{district}" AND '


            
            ans = [square, year, material, floar, remont, rooms]
            

            for i in range(len(filds1)):
                if ans[i] != []:
                    sql += '('
                    for j in ans[i]:
                        sql += f'"{filds1[i]}" = "{j}" OR '
                    sql = sql[:-4]
                    sql += ') AND '
            sql = sql[:-5]

            st.dataframe(pd.read_sql(sql, con)) #index_col = ['index']
    except sqlite3.OperationalError:
            st.error('Загрузите базу данных')



