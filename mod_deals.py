# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:48:45 2023

@author: Origo
"""
import pandas as pd

def deal_transaction(row):
    transaction = pd.Series({'date':None, 'time': None, 'name': None, 
                             'kod': None, 'BS' = None,
                             'qty': None, 'price_point': None, 'price': None, 
                             'amoint_point': None, 'amount': None, 
                             'qty_cr':None, 'amount_cr_point': None, 'amount_cr': None,
                             'qty_dt':None, 'amount_dt_point': None, 'amount_dt': None,
                             'commision': None, 'date_close': None})
    
    transaction.date = row[0]
    transaction.name = str(row[4])
    transaction.qty = int(row[13])
    transaction.price_poit = float(row[11])
    transaction.price = float(row[9])
    transaction.amount_point = transaction.price_point * transaction.qty
    transaction.amount = transaction.price * transaction.qty
    transaction.commision = float(row[17])
    if row[7] == "Покупка" :
        BS = -1
        transaction.BS = "Buy"
        
        transaction.qty_dt = transaction.qty
        transaction.amount_dt_point = transaction.amount_point
        transaction.amount_dt = transaction.amount
        
        transaction.qty_cr = 0
        transaction.amount_cr_point = 0
        transaction.amount_cr = 0
        
    else :
        BS = 1
        transaction.BS = "Sell"
        
        transaction.qty_dt = 0
        transaction.amount_dt_point = 0
        transaction.amount_dt = 0
        
        transaction.qty_cr = transaction.qty
        transaction.amount_cr_point = transaction.amount_point
        transaction.amount_cr = transaction.amount

    transaction.qty *= BS
    transaction.amount_point *= BS
    transaction.amount *= BS
    
    return transaction
   
    
""""
class deal_transaction:
    def __init__(self, row):
        self.end = 0
        self.date = row[0]
        self.account = row[1]
        self.name = row[4]
        self.kod = row[5]
        amount = float(row[9])*int(row[13])
        amount_point = float(row[11])*int(row[13])
        if row[7] == "Покупка": 
            self.bs = -1
            self.amount_dt = amount #row[16]
            self.amount_dt_point = amount_point
            self.number_dt = int(row[13])
            self.amount_cr = 0
            self.amount_cr_point = 0
            self.number_cr = 0
        else : 
            self.bs = 1
            self.amount_cr = amount #row[16]
            self.amount_cr_point = amount_point
            self.number_cr = int(row[13])
            self.amount_dt = 0
            self.amount_dt_point = 0
            self.number_dt = 0
        self.price = float(row[9])
        self.point_price = float(row[11])
        self.numbers = int(row[13])*self.bs
        self.amount = amount*self.bs
        self.amount_point = amount_point*self.bs
        if row[17] == '' : self.commision = 0
        else : self.commision = float(row[17])
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
"""
        
deals_close = []
deals_open = []

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
            return
        #действия с i
        #действия val
    deals_open.append(add_transaction)
    return
