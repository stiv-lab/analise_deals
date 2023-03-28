# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 15:43:30 2023

@author: Origo

v3
    добавлена функция open_price(date) - возвращает цену открытия дня
v3.1
    156 строка ( if deal.bs==-1 : ) поменял на -1, так как длинная сделка дебетует счет
"""


import xlrd
from openpyxl import utils
import pandas as pd


def read_ticket():
    """    
        читаем файл с котировками в 
    """
    tmp_df = pd.read_excel("tickets\\RIH2 D.xls")
    # tmp_df = pd.read_excel("tickets\\RIH2 D.xls", index_col = '<DATE>')
    # print(tmp_df)
    # print(tmp_df[0][0])
    return tmp_df


def open_date_price(date, ticket_df):
    """
        1 создаем словарь по дате и цене открытия
        2 проверяем на наличие даты в словаре, если есть возвращаем
        3 если нет в словаре, идем в файл находим цену и заносим в словарь и возвращаем
        4 если не найдено, возвращаем 0
    """
    #offset = 693594
    #print(xlrd.xldate_as_datetime(date, 0))
    date = xlrd.xldate_as_datetime(date, 0).date()
    #print(date, type(date))

    # print(ticket_df)
    # print(date)

    # print(int(date))
    #print (datetime.fromtimestamp(int(date)))
    #print(ticket_df[ticket_df['<DATE>'] == int(date)])

    for i, row in ticket_df.iterrows():
        row_date = row['<DATE>'].date()

        if row_date == date:
            #print(i, row['<DATE>'], row_date, row['<OPEN>'])
            pass
            return row['<OPEN>']

    pass
    return 0


def compare_openday_opendeal(open_day, open_deal, bs):
    """
    bs = 1 short
    bs = -1 long

    если направление сделки совпадает с направлением дневной свечи то 1
    если не совпадает, то -1
    """
    if bs == -1:  # long
        if open_day > open_deal:
            return -1
        if open_day < open_deal:
            return 1
    if bs == 1:  # short
        if open_day > open_deal:
            return 1
        if open_day < open_deal:
            return -1
    return 0


def check_PL(deal):
    if deal.bs == -1:
        if deal.number_dt == 0:
            price_open = 'dt = 0'
        else:
            price_open = deal.amount_dt/deal.number_dt
            price_open_point = deal.amount_dt_point/deal.number_dt
        if deal.number_cr == 0:
            price_close = 'cr = 0'
        else:
            price_close = deal.amount_cr/deal.number_cr
            price_close_point = deal.amount_cr_point/deal.number_cr
    else:
        if deal.number_cr == 0:
            price_open = 'cr = 0'
        else:
            price_open = deal.amount_cr/deal.number_cr
            price_open_point = deal.amount_cr_point/deal.number_cr
        if deal.number_dt == 0:
            price_close = 'dt = 0'
        else:
            price_close = deal.amount_dt/deal.number_dt
            price_close_point = deal.amount_dt_point/deal.number_dt
    return


# функция проверяет на корректность данных в df deals
def check_close_deals(deals):
    zero_value_df = deals.loc[(deals['qty_cr'] == 0) | (deals['qty_dt'] == 0)]
    num_zero_value = len(zero_value_df)
    if num_zero_value > 0:
        print(
            f"Error: There are {num_zero_value} rows with zero value in 'qty_dt' and 'qty_cr' columns")
        return 1
    return 0


# запись df deals в xls


def write_deals_close(deal_manager, file_name='deals_close.xlsx'):
    # Создаем DataFrame для записи данных
    deals_close_df = pd.DataFrame(deal_manager.deals_close)

    # Группировка инструментов по их базовому инструменту и типу (фьючерс или опцион)
    grouped_deals = deals_close_df.groupby(
        by=[deals_close_df['name'].str[:2], deals_close_df['name'].str.len()])

    try:
        # Записываем данные в файл Excel
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            for (base_instrument, name_length), group in grouped_deals:
                sheet_name = f"{base_instrument}_{'Futures' if name_length == 4 else 'Options'}"
                try:
                    group.to_excel(writer, sheet_name=sheet_name, index=False)
                except utils.exceptions.IllegalCharacterError as e:
                    print(f"Ошибка записи данных на лист {sheet_name}: {e}")
    except Exception as e:
        print(f"Ошибка записи файла {file_name}: {e}")


""""
def write_deals_close(deal_manager):

    deals = deal_manager.deals_close

    if check_close_deals(deals):
        print("Error: при анализе df deals обнаружены ошибки, запись файла не возможно")
        return 1

    work_sheet = 'Deals close'
    file_name = "Deals_close v1.1.xls"

    deals.to_excel(file_name, sheet_name=work_sheet, index=False)
"""

"""   
def write_deals_close(deals):

    ticket_df = read_ticket()

    ws = 'Deals close'

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'
#    print ("N\tName\tкол-во\tPL\tОбщ позиция\tкомм\tДата расчетная")    
    time_format = xlwt.XFStyle()
    time_format.num_format_str = 'h:mm:ss'
#   num_format = xlwt.XFStyle()
#    num_format.
#    num_format('# ##0.00')

    ws.write(0, 0, 'N')
    j=1
    ws.write(0, j, 'Date')
    j=2
    ws.write(0, j, 'Time')
    j=3
    ws.write(0, j, 'Name')
    j=4
    ws.write(0, j, 'B/S')
    j=5
    ws.write(0, j, 'Contracts 1')
    j=6
    ws.write(0, j, 'Price O')
    j=7
    ws.write(0, j, 'Price O point')
    j=8
    ws.write(0, j, 'Price C')
    j=9
    ws.write(0, j, 'Price C point')
    j=10
    ws.write(0, j, 'Price C date')    
    j=11
    ws.write(0, j, 'Marge')
    j=12
    ws.write(0, j, 'Marge point')
    j=13
    ws.write(0, j, 'Form enter')
    j=14
    ws.write(0, j, 'Profit')
    j=15
    ws.write(0, j, 'Profit point')
    j=16    
    ws.write(0, j, 'Loss')
    j=17    
    ws.write(0, j, 'Loss point')
    j=18
    ws.write(0, j, 'PLwC')
    j=19
    ws.write(0, j, 'Open')
    j=20
    ws.write(0, j, 'Close')
    j=21
    ws.write(0, j, 'Comm')
    j=22
    ws.write(0, j, 'Contracts 2')
    j=23
    ws.write(0, j, 'Type')
    j=24
    ws.write(0, j, 'Date Open Price')
    j=25
    ws.write(0, j, 'Deal BS Eq candle date?')

    for i, deal in enumerate(deals):
        
        date_open_price = open_date_price(deal.date, ticket_df)

        j=0 #N
        ws.write(i+1, j, i+1)
        j=1 #Date
        ws.write(i+1, j, deal.date)
        j=2 #Time
        ws.write(i+1, j, deal.date, time_format)
#        ws.write(i+1, j, deal.deal_close, time_format)
        j=3 # Name
        ws.write(i+1, j, deal.name)

        if deal.bs==-1 : 
            j=4 # B/S
            ws.write(i+1, j, 'L')
            if deal.number_dt == 0 : 
                price_open = 'dt = 0'
            else : 
                price_open = deal.amount_dt/deal.number_dt
                price_open_point = deal.amount_dt_point/deal.number_dt
            if deal.number_cr == 0 : 
                price_close = 'cr = 0'
            else : 
                price_close = deal.amount_cr/deal.number_cr           
                price_close_point = deal.amount_cr_point/deal.number_cr           
        else : 
            j=4 #B/S
            ws.write(i+1, j, 'S')
            if deal.number_cr == 0 : 
                price_open = 'cr = 0'
            else : 
                price_open = deal.amount_cr/deal.number_cr
                price_open_point = deal.amount_cr_point/deal.number_cr
            if deal.number_dt == 0 : 
                price_close = 'dt = 0'
            else : 
                price_close = deal.amount_dt/deal.number_dt
                price_close_point = deal.amount_dt_point/deal.number_dt           
#        ws.write(i+1, j, deal.bs)        
        j=5 # Contracts
        ws.write(i+1, j, deal.number_cr)
        j=6 # Price O
        ws.write(i+1, j, price_open)
        j=7 # Price O point
        ws.write(i+1, j, price_open_point)
        j=8 # Price C
        ws.write(i+1, j, price_close)
        j=9 # Price C pomt
        ws.write(i+1, j, price_close_point)
        j=10 # Price C pomt
        ws.write(i+1, j, deal.deal_close)
        j=11 # Marge
        if deal.bs == 1 : ws.write(i+1, j, price_open-price_close)
        else : ws.write(i+1, j, price_close-price_open)
        j=12 # Marge point
        if deal.bs == 1 : ws.write(i+1, j, price_open_point-price_close_point)
        else : ws.write(i+1, j, price_close_point-price_open_point)
#        ws.write(i+1, j, '')
        j=13
        ws.write(i+1, j, '')
        j=14
        if ( deal.amount_point > 0) :
            ws.write(i+1, j, deal.amount)
            ws.write(i+1, j+1, deal.amount_point)
            ws.write(i+1, j+2, 0)
            ws.write(i+1, j+3, 0)
        else:
            ws.write(i+1, j, 0)
            ws.write(i+1, j+1, 0)
            ws.write(i+1, j+2, deal.amount)
            ws.write(i+1, j+3, deal.amount_point)
        j=18
        ws.write(i+1, j, deal.amount-deal.commision)
        j=19
        ws.write(i+1, j, deal.amount_cr)
        j=20
        ws.write(i+1, j, deal.amount_dt)
        j=21
        ws.write(i+1, j, deal.commision)
        j=22
        ws.write(i+1, j, deal.number_dt)
        j=23
        ws.write(i+1, j, deal.type)
        j=24
        ws.write(i+1, j, date_open_price)
        j=25
        ws.write(i+1, j, compare_openday_opendeal(date_open_price,price_open_point,deal.bs))
        
    
    wb.save('Deals_close v3_1.xls')
"""


def print_deals_close(deals_open):
    print("кол-во элементов в deals_close: ", len(deals_open))
    print("N\tName\tкол-во\tPL\tОбщ позиция\tкомм\tДата расчетная")
#    print ("N", '\t',"Name:", '\t', "кол-во", '\t', "PL", '\t', "Общ позиция",'\t',"комм")
    for i, deal in deals_open.iterrows():
        print(i+1, '\t', deal.name, '\t', deal.number_cr, '\t', deal.amount, '\t',
              deal.amount_cr, '\t', deal.commision, '\t', xlrd.xldate_as_tuple(deal.deal_close, 0))
