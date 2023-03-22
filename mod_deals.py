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

    def accumulate_deal(self, deal, add_transaction):
        deal['qty'] += add_transaction['qty']
        deal['amount'] += add_transaction['amount']
        deal['amount_point'] += add_transaction['amount_point']
        deal['commision'] += add_transaction['commision']
        deal['amount_dt'] += add_transaction['amount_dt']
        deal['amount_dt_point'] += add_transaction['amount_dt_point']
        deal['qty_dt'] += add_transaction['qty_dt']
        deal['amount_cr'] += add_transaction['amount_cr']
        deal['amount_cr_point'] += add_transaction['amount_cr_point']
        deal['qty_cr'] += add_transaction['qty_cr']
        if (add_transaction['date_time'] > deal['deal_date_time_close']):
            deal['deal_date_time_close'] = add_transaction['date_time']
        return deal

    def split_accumulation_deal(self, deal, add_transaction):
        close_transaction = add_transaction.copy()
        close_transaction['qty'] = deal['qty'] * (-1)
        close_transaction['amount'] = add_transaction['amount'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['amount_point'] = add_transaction['amount_point'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['commision'] = add_transaction['commision'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['amount_dt'] = add_transaction['amount_dt'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['amount_dt_point'] = add_transaction['amount_dt_point'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['qty_dt'] = add_transaction['qty_dt'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['amount_cr'] = add_transaction['amount_cr'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['amount_cr_point'] = add_transaction['amount_cr_point'] / \
            add_transaction['qty'] * abs(deal['qty'])
        close_transaction['qty_cr'] = add_transaction['qty_cr'] / \
            add_transaction['qty'] * abs(deal['qty'])

        self.accumulate_deal(deal, close_transaction)
        if deal['qty'] == 0:  # это условие всегда выполняется в данной точке
            self.transfer_deal(deal)

        add_transaction['qty'] -= close_transaction['qty']
        add_transaction['amount'] -= close_transaction['amount']
        add_transaction['amount_point'] -= close_transaction['amount_point']
        add_transaction['commision'] -= close_transaction['commision']
        add_transaction['amount_dt'] -= close_transaction['amount_dt']
        add_transaction['amount_dt_point'] -= close_transaction['amount_dt_point']
        add_transaction['qty_dt'] -= close_transaction['qty_dt']
        add_transaction['amount_cr'] -= close_transaction['amount_cr']
        add_transaction['amount_cr_point'] -= close_transaction['amount_cr_point']
        add_transaction['qty_cr'] -= close_transaction['qty_cr']

        return add_transaction

    def add_transaction(self, add_transaction):
        name = add_transaction['name']
        if name not in self.open_deals['name'].values:
            # если инструмент не найден, то открытие сделки и выход
            self.open_deals = pd.concat(
                [self.open_deals, add_transaction.to_frame().T], ignore_index=True)
            return

        # дальше, если инструмент найден
        deal = self.open_deals.loc[self.open_deals['name'] == name].iloc[0]
        if add_transaction['BS'] == deal['BS']:
            # если направление совпадает, то накопление и к выходу
            self.accumulate_deal(deal, add_transaction)
            return

        if abs(add_transaction['qty']) <= abs(deal['qty']):
            # если меньше или равно, накопить
            self.accumulate_deal(deal, add_transaction)
            if deal['qty'] == 0:
                self.transfer_deal(deal)
        else:
            # в это точке, в транзакции больше, чем нужно для закрытия сделки
            # делим транзакцию, на закрытие сделки и остаток
            # остаток идет на открытие новой сделки

            self.split_accumulation_deal(deal, add_transaction)
            self.open_deals = pd.concat(
                [self.open_deals, add_transaction.to_frame().T], ignore_index=True)

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
