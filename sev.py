import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

filds1 = ['Наименование ЖК', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Площадь',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Год постройки', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Материал стен',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Этажность', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Отделка',
       'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Комнатность']

cities = ['Красногорск', 'Видное', 'Одинцово', 'Люберцы', 'Мытищи', 'Балашиха',
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

st.title('Аналитика Sevial')

main, load = st.tabs(['Таблица', 'Загрузить'])

with load:
    @st.cache_data
    def load_data(file):
        df = pd.read_excel(file)
        df['Создана'] = df['Создана'].dt.date
        df.to_sql('info', con, if_exists = 'replace')
        
    file = st.file_uploader('Загрузите xlsx Файл')

    con = sqlite3.connect('tt.sqlite')
    cur = con.cursor()

    if file is not None:
        load_data(file)

    # cc1, cc2 = st.columns([3, 1])
    # with cc2:
    #     reloud = st.button('Перезагрузить')
    #     if reloud:
    #         st.cache_data.clear()
    #         st.experimental_rerun()

with main:
    if "disabled" not in st.session_state:
        st.session_state["disabled"] = True

    def districts(area):
        if len(area) == 1:
            sql_d = f'SELECT "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area[0]}" GROUP BY "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район"'       
        else:
            sql_d = f'SELECT "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" in {tuple(area)} GROUP BY "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район"'
        d = [i[0] for i in cur.execute(sql_d).fetchall() if i[0] is not None]
        return d
    
    def j_k(value, city = False):
        if city:
            sql_d = f'SELECT "Наименование ЖК" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город" = "{value}" GROUP BY "Наименование ЖК"'
        else:
            if len(value) == 1:
                sql_d = f'SELECT "Наименование ЖК" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{value[0]}" GROUP BY "Наименование ЖК"'
            else:
                sql_d = f'SELECT "Наименование ЖК" FROM info WHERE "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" in {tuple(value)} GROUP BY "Наименование ЖК"'
        d = [i[0] for i in cur.execute(sql_d).fetchall() if i[0] is not None]
        return d

    try:
        c1, c2, c3 = st.columns(3)
        with c1:
            city = st.selectbox('Город', cities, disabled = st.session_state.disabled)
            st.checkbox('Москва', key= "disabled")
        with c2:
            area = st.multiselect('Округ', ['НАО', 'ЗАО', 'ЮВАО', 'САО', 'СЗАО', 'ЮАО', 'СВАО', 'ЦАО', 'ВАО','ЮЗАО', 'ЗелАО', 'ТАО'], disabled = not st.session_state.disabled)
            district = st.multiselect('Район', districts(area), disabled = not st.session_state.disabled)
        with c3:
            if not st.session_state.disabled:
                jk = st.multiselect('Наименование ЖК', j_k(city, city = True))
            else:
                jk = st.multiselect('Наименование ЖК', j_k(area))
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

        upload = st.button("Показать")
        st.divider()

        if upload:
            sql = 'SELECT "Создана", "Номер договора", "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м", "Адрес объекта оценки", '
            
            if not st.session_state.disabled: # Добавление к запросу
                sql += '"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город"'
            else:
                sql += '"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ", "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район"'
                
            sql += ''.join(f', "{i}"' for i in filds1)
            sql += ' FROM info WHERE '

            if not st.session_state.disabled: # Выдор по выбранным данным
                sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Город" = "{city}" AND '

            elif district == []:
                if len(area) == 1:
                    sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area[0]}" AND '
                else:
                    sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" in {tuple(area)} AND '
            else:
                if len(area) == 1:
                    if len(district) == 1:
                        sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area[0]}" AND "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" = "{district[0]}" AND '
                    else:
                        sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" = "{area[0]}" AND "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" in {tuple(district)} AND '
                else:
                    if len(district) == 1:
                        sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" in {tuple(area)} AND "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" = "{district[0]}" AND '
                    else:
                        sql += f'"ИНФОРМАЦИЯ ПО ОТЧЕТУ: Округ" in {tuple(area)} AND "ИНФОРМАЦИЯ ПО ОТЧЕТУ: Район" in {tuple(district)} AND '


            

            ans = [jk, square, year, material, floar, remont, rooms]

            for i in range(len(filds1)):
                if ans[i] != []:
                    sql += '('
                    for j in ans[i]:
                        sql += f'"{filds1[i]}" = "{j}" OR '
                        # sql += f'"{filds1[i]}" = "{j}" OR '
                    sql = sql[:-4]
                    sql += ') AND '
            sql = sql[:-5]
            print(sql)


            df = pd.read_sql(sql, con)
            if len(df) > 1:
                st.dataframe(df)
                chart = df[['Создана', 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м']].sort_values('Создана')
                chart['ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м'] = chart['ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м'].apply(lambda x: x.replace(' ', '').replace('р.', '').replace('р', '')).astype(float).astype(int)

                minn = '{0:,}'.format(chart["ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м"].min()).replace(',', ' ')
                meann = '{0:,}'.format(chart["ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м"].mean().astype(int)).replace(',', ' ')
                maxx =  '{0:,}'.format(chart["ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м"].max()).replace(',', ' ')

                fig = px.line(chart, x = 'Создана', y = 'ИНФОРМАЦИЯ ПО ОТЧЕТУ: Стоимость 1 кв.м', color_discrete_sequence = ["#ff0000"], 
                            title = f'Мин. цена = {minn}р.\
                                Ср. цена = {meann}р.\
                                Макс. цена = {maxx}р.')
                st.plotly_chart(fig)

            elif len(df) == 1: 
                st.dataframe(df)
            else:
               a1, a2, a3 =  st.columns(3)
               a2.header('Нет данных')

    except sqlite3.OperationalError:
            st.error('Загрузите базу данных')
