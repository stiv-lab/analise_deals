# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:28:33 2023

@author: Origo
v3
 - привязываем таблицу с котировками и фиксируем цену открытия дня
 
"""

import argparse
import os
import sys
import xlrd

import wdc
import mod_deals
from mod_deals import deal_transaction
from mod_deals import deals_close
from mod_deals import deals_open

def print_row(row):
    for i, c_el in enumerate(row):
        print (i, ": ", c_el)
    
def print_deals_open(deals):
    print ("кол-во элементов в deals_open: ",len(deals))
    print ("N", '\t',"Name", '\t', "numbers", '\t', "open pos",'\t',"comm")
    for i,deal in enumerate(deals):
        print(i+1, '\t', deal.name,'\t', deal.number_cr,'\t', deal.amount_cr,'\t', deal.commision)

def test_open_date_price():   #test open_date_price
    #test 1
    print("test 1: open day 145 open deal 147 long return 1")
    if wdc.compare_openday_opendeal(145, 147, -1) == 1 : print ("pass")
    else : print ("False")
    #test 2
    print("test 2: open day 147 open deal 145 long return -1")
    if wdc.compare_openday_opendeal(147, 145, -1) == -1 : print ("pass")
    else : print ("False")
    #test 3
    print("test 3: open day 145 open deal 147 short return 1")
    if wdc.compare_openday_opendeal(145, 147, 1) == -1 : print ("pass")
    else : print ("False")
    #test 4
    print("test 4: open day 147 open deal 145 short return -1")
    if wdc.compare_openday_opendeal(147, 145, 1) == 1 : print ("pass")
    else : print ("False")
    
    return 0
    
# определяем имя файла или из параметров строки вызова или из виртуального окружения
def get_file_path():
    
    parser = argparse.ArgumentParser(description='Обработка XLS файла с транзакциями и группировка в сделки')
    parser.add_argument('file_path', nargs='?', help='Имя файла для обработки. Если не указано, используется по умолчанию из перепенных среды')
    args = parser.parse_args()
    
    file_path = args.file_path or os.getenv('DEFAULT_CSV_PATH')
    
    if not file_path:
        print('Не указан путь к файлу и переменная среды DEFAULT_CSV_FILE не задана')
        return None
    
    if not os.path.isfile(file_path):
        print(f"Файл {file_path} не найдет.")
        return None
    
    return  file_path
    
# основная фукнция 
def main():
    
    os.environ['DEFAULT_CSV_PATH'] = "rep_deals/DealOwnsReport 01-02 23.xls"
    
    file_path = get_file_path()
    
    if not file_path: sys.exit(1)
           
    #for i in 7
    f=xlrd.open_workbook(file_path)
    listDeal = f.sheet_by_index(0)
        
    # читаем файл построчно, каждая строка инициирует класс с данными транзакции
    # для каждого определенного экземпляра класса вызываем функцию расчета сделок
    for rownum in range(4,listDeal.nrows):
        mod_deals.add_deal(deal_transaction(listDeal.row_values(rownum)))
    
    
    wdc.write_deals_close(deals_close)
    
    print_deals_open(deals_open)
    
    print (f.sheet_names())
    
if __name__=='__main__':
    main()
    