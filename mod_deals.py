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
        transaction = pd.Series({'date_time': None, 'name': None,
                                 'kod': None, 'BS': None,
                                 'qty': None, 'price_point': None, 'price': None,
                                 'amount_point': None, 'amount': None,
                                 'qty_cr': None, 'amount_cr_point': None, 'amount_cr': None,
                                 'qty_dt': None, 'amount_dt_point': None, 'amount_dt': None,
                                 'commision': None, 'deal_date_time_close': None})

        transaction['date_time'] = transaction['deal_date_time_close'] = row[0]
        transaction['name'] = str(row[4])
        transaction['qty'] = int(row[13])
        transaction['price_point'] = float(row[11])
        transaction['price'] = float(row[9])
        transaction['amount_point'] = transaction['price_point'] * \
            transaction['qty']
        transaction['amount'] = transaction['price'] * transaction['qty']
        transaction['commision'] = float(row[17])
        if row[7] == "Покупка":
            BS = -1
            transaction['BS'] = "Buy"

            transaction['qty_dt'] = transaction['qty']
            transaction['amount_dt_point'] = transaction['amount_point']
            transaction['amount_dt'] = transaction['amount']

            transaction['qty_cr'] = 0
            transaction['amount_cr_point'] = 0
            transaction['amount_cr'] = 0

        else:
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

    def accumulate_deal(self, deal_index, add_tr):
        deal = self.deals_open.loc[deal_index]
        self.deals_open.at[deal_index, 'qty'] += add_tr['qty']
        self.deals_open.at[deal_index, 'amount'] += add_tr['amount']
        self.deals_open.at[deal_index,
                           'amount_point'] += add_tr['amount_point']
        self.deals_open.at[deal_index, 'commision'] += add_tr['commision']
        self.deals_open.at[deal_index, 'amount_dt'] += add_tr['amount_dt']
        self.deals_open.at[deal_index,
                           'amount_dt_point'] += add_tr['amount_dt_point']
        self.deals_open.at[deal_index, 'qty_dt'] += add_tr['qty_dt']
        self.deals_open.at[deal_index, 'amount_cr'] += add_tr['amount_cr']
        self.deals_open.at[deal_index,
                           'amount_cr_point'] += add_tr['amount_cr_point']
        self.deals_open.at[deal_index, 'qty_cr'] += add_tr['qty_cr']
        if (add_tr['date_time'] > deal['deal_date_time_close']):
            self.deals_open.at[deal_index,
                               'deal_date_time_close'] = add_tr['date_time']
        return deal

    def transfer_deal(self, deal_index):
        self.deals_close = pd.concat(
            [self.deals_close, self.deals_open.loc[deal_index].to_frame().T], ignore_index=True)
        self.deals_open = self.deals_open.drop(deal_index)
        self.deals_open = self.deals_open.reset_index(drop=True)
        return

    def split_accumulation_deal(self, deal_index, add_tr):
        # транзакция приходт с qty больше чем в deal и противоположного направления
        # закрываем сделку на сумму отстатка в deal и
        # на остаток открываем новую сделку
        deal = self.deals_open.loc[deal_index]
        close_tr = add_tr.copy()
        close_tr['qty'] = deal['qty'] * (-1)
        close_tr['amount'] = add_tr['amount'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['amount_point'] = add_tr['amount_point'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['commision'] = add_tr['commision'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['amount_dt'] = add_tr['amount_dt'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['amount_dt_point'] = add_tr['amount_dt_point'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['qty_dt'] = add_tr['qty_dt'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['amount_cr'] = add_tr['amount_cr'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['amount_cr_point'] = add_tr['amount_cr_point'] / \
            add_tr['qty'] * abs(deal['qty'])
        close_tr['qty_cr'] = add_tr['qty_cr'] / \
            add_tr['qty'] * abs(deal['qty'])

        self.accumulate_deal(deal_index, close_tr)
        # это условие всегда выполняется в данной точке
        if self.deals_open.loc[deal_index]['qty'] == 0:
            self.transfer_deal(deal_index)

        add_tr['qty'] -= close_tr['qty']
        add_tr['amount'] -= close_tr['amount']
        add_tr['amount_point'] -= close_tr['amount_point']
        add_tr['commision'] -= close_tr['commision']
        add_tr['amount_dt'] -= close_tr['amount_dt']
        add_tr['amount_dt_point'] -= close_tr['amount_dt_point']
        add_tr['qty_dt'] -= close_tr['qty_dt']
        add_tr['amount_cr'] -= close_tr['amount_cr']
        add_tr['amount_cr_point'] -= close_tr['amount_cr_point']
        add_tr['qty_cr'] -= close_tr['qty_cr']

        return add_tr

    def add_deal(self, add_tr):
        name = add_tr['name']
        if self.deals_open.empty or name not in self.deals_open['name'].values:
            # если инструмент не найден, то открытие сделки и выход
            self.deals_open = pd.concat(
                [self.deals_open, add_tr.to_frame().T], ignore_index=True)
            return

        # дальше, если инструмент найден
        deal_index = self.deals_open.loc[self.deals_open['name']
                                         == name].index[0]
        if add_tr['BS'] == self.deals_open.at[deal_index, 'BS']:
            # если направление совпадает, то накопление и к выходу
            self.accumulate_deal(deal_index, add_tr)
            return

        if abs(add_tr['qty']) <= abs(self.deals_open.at[deal_index, 'qty']):
            # если меньше или равно, накопить
            self.accumulate_deal(deal_index, add_tr)
            if self.deals_open.at[deal_index, 'qty'] == 0:
                self.transfer_deal(deal_index)
        else:
            # в это точке, в транзакции больше, чем нужно для закрытия сделки
            # делим транзакцию, на закрытие сделки и остаток
            # остаток идет на открытие новой сделки

            add_tr = self.split_accumulation_deal(deal_index, add_tr)
            self.deals_open = pd.concat(
                [self.deals_open, add_tr.to_frame().T], ignore_index=True)

        return


"""
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
            return

        self.deals_open = pd.concat([self.deals_open, add_transaction.to_frame().T], ignore_index=True)
        return
"""
