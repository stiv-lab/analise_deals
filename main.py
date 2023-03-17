# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:28:33 2023

@author: Origo
"""
# -*- coding: utf-8 -*-
"""
v3
 - привязываем таблицу с котировками и фиксируем цену открытия дня
 

"""
import xlrd
import wdc_v3_1 as wdc
import pathlib
from pathlib import Path

class deal_transaction:
    def __init__(self, row):
        self.end = 0
        self.date = row[0]
        self.account = row[1]
        self.name = row[4]
        self.kod = row[5]
        amount = row[9]*row[13]
        amount_point = row[11]*row[13]
        if row[7] == "Покупка": 
            self.bs = -1
            self.amount_dt = amount #row[16]
            self.amount_dt_point = amount_point
            self.number_dt = row[13]
            self.amount_cr = 0
            self.amount_cr_point = 0
            self.number_cr = 0
        else : 
            self.bs = 1
            self.amount_cr = amount #row[16]
            self.amount_cr_point = amount_point
            self.number_cr = row[13]
            self.amount_dt = 0
            self.amount_dt_point = 0
            self.number_dt = 0
        self.price = row[9]
        self.point_price = row[11]
        self.numbers = row[13]*self.bs
        self.amount = amount*self.bs
        self.amount_point = amount_point*self.bs
        if row[17] == '' : self.commision = 0
        else : self.commision = row[17]
        self.type = row[18]
        self.deal_close = row[0]
        #self.date_open_price = wdc.open_date_price(self.date)

        
    def print_transaction(self):
        print('name: ',self.name)
        print('acc: ',self.account)
        print('b/s: ',self.bs)
        print('price: ',self.price)
        print('пункты: ',self.point_price)
        print('кол-во: ',self.numbers)
        print('сумма: ',self.amount)
        print('комм: ',self.commision)
        print('type: ',self.type)

deals_close = []
deals_open = []

def print_row(row):
    for i, c_el in enumerate(row):
        print (i, ": ", c_el)
    
def print_deals_open(deals):
    print ("кол-во элементов в deals_open: ",len(deals))
    print ("N", '\t',"Name", '\t', "numbers", '\t', "open pos",'\t',"comm")
    for i,deal in enumerate(deals):
        print(i+1, '\t', deal.name,'\t', deal.number_cr,'\t', deal.amount_cr,'\t', deal.commision)

def add_deal(add_transaction):
    
    #print(add_transaction.amount, add_transaction.amount_point) #debug
    
    for i, deal in enumerate(deals_open):
        if add_transaction.name == deal.name:
            deal.numbers += add_transaction.numbers
            deal.amount += add_transaction.amount
            deal.amount_point += add_transaction.amount_point
            deal.commision += add_transaction.commision
            if (add_transaction.deal_close > deal.deal_close) : 
                deal.deal_close = add_transaction.deal_close
            if add_transaction.bs == -1:
                deal.amount_dt += add_transaction.amount_dt
                deal.amount_dt_point += add_transaction.amount_dt_point
                deal.number_dt += add_transaction.number_dt
            else:
                deal.amount_cr += add_transaction.amount_cr
                deal.amount_cr_point += add_transaction.amount_cr_point
                deal.number_cr += add_transaction.number_cr                
            if deal.numbers == 0 : 
                deals_close.append(deal)
                del deals_open[i]
            return;
        #действия с i
        #действия val
    deals_open.append(add_transaction)

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
    
# test_open_date_price()

# цикл по файлам: DealOwnsReport + MMYY
f_path = 'rep_deals\\'
f_name =  'DealOwnsReport'
f_name_add = ' 05-0622'
f_ext = '.xls'           

path = Path(pathlib.Path.cwd(), 'rep_deals', f_name+f_name_add+f_ext)
print(path)
print(f_path+f_name+f_name_add+f_ext)
#for i in 7
f=xlrd.open_workbook(f_path+f_name+f_name_add+f_ext)
listDeal = f.sheet_by_index(0)
    
for rownum in range(4,listDeal.nrows):
    add_deal(deal_transaction(listDeal.row_values(rownum)))

"""
f_name_add = ' 01-03.19'
f=xlrd.open_workbook(f_name+f_name_add+f_ext)
listDeal = f.sheet_by_index(0)
    
for rownum in range(4,listDeal.nrows):
    add_deal(deal_transaction(listDeal.row_values(rownum)))
"""
"""
f_name_add = ' 03.19'
f=xlrd.open_workbook(f_name+f_name_add+f_ext)
listDeal = f.sheet_by_index(0)
    
for rownum in range(4,listDeal.nrows):
    add_deal(deal_transaction(listDeal.row_values(rownum)))
"""

wdc.write_deals_close(deals_close)

print_deals_open(deals_open)

print (f.sheet_names())