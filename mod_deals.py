# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 10:48:45 2023

@author: Origo
"""
import pandas as pd

class DealManager:
    def __init__(self):
        self.deals_close = pd.DataFrame()
        self.deals_open = pd.DataFrame()

    def deal_transaction(self, row):
        transaction = pd.Series({'date_time':None, 'name': None, 
                                 'kod': None, 'BS' : None,
                                 'qty': None, 'price_point': None, 'price': None, 
                                 'amount_point': None, 'amount': None, 
                                 'qty_cr':None, 'amount_cr_point': None, 'amount_cr': None,
                                 'qty_dt':None, 'amount_dt_point': None, 'amount_dt': None,
                                 'commision': None,'deal_date_time_close': None })
        
        transaction['date_time'] = transaction['deal_date_time_close'] =row[0]
        transaction['name'] = str(row[4])
        transaction['qty'] = int(row[13])
        transaction['price_point'] = float(row[11])
        transaction['price'] = float(row[9])
        transaction['amount_point'] = transaction['price_point'] * transaction['qty']
        transaction['amount'] = transaction['price'] * transaction['qty']
        transaction['commision'] = float(row[17])
        if row[7] == "Покупка" :
            BS = -1
            transaction['BS'] = "Buy"
            
            transaction['qty_dt'] = transaction['qty']
            transaction['amount_dt_point'] = transaction['amount_point']
            transaction['amount_dt'] = transaction['amount']
            
            transaction['qty_cr'] = 0
            transaction['amount_cr_point'] = 0
            transaction['amount_cr'] = 0
            
        else :
            BS = 1
            transaction['BS'] = "Sell"
            
            transaction['qty_dt'] = 0
            transaction['amount_dt_point'] = 0
            transaction['amount_dt'] = 0
            
            transaction['qty_cr'] = transaction['qty']
            transaction['amount_cr_point'] = transaction['amount_point']
            transaction['amount_cr'] = transaction['amount']
    
        transaction['qty'] *= BS
        transaction['amount_point'] *= BS
        transaction['amount'] *= BS
        
        return transaction
   
    def add_deal(self, add_transaction):
        for i, deal in self.deals_open.iterrows():
            if add_transaction['name'] == deal['name']:
                deal['qty'] += add_transaction['qty']
                deal['amount'] += add_transaction['amount']
                deal['amount_point'] += add_transaction['amount_point']
                deal['commision'] += add_transaction['commision']
                if (add_transaction['date_time'] > deal['deal_date_time_close']):
                    deal['deal_date_time_close'] = add_transaction['date_time']
                if add_transaction['BS'] == 'Buy':
                    deal['amount_dt'] += add_transaction['amount_dt']
                    deal['amount_dt_point'] += add_transaction['amount_dt_point']
                    deal['qty_dt'] += add_transaction['qty_dt']
                else:
                    deal['amount_cr'] += add_transaction['amount_cr']
                    deal['amount_cr_point'] += add_transaction['amount_cr_point']
                    deal['qty_cr'] += add_transaction['qty_cr']
 
            if deal['qty'] == 0:
                self.deals_close = pd.concat([self.deals_close, deal.to_frame().T], ignore_index=True)
                self.deals_open = self.deals_open.drop(i)
                self.deals_open = self.deals_open.reset_index(drop=True)
            return
    
        self.deals_open = pd.concat([self.deals_open, add_transaction.to_frame().T], ignore_index=True)
        return
