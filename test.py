# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:49:54 2023

@author: Origo
"""
import pandas as pd
import pytest
from deal_manager import DealManager


def read_test_data_from_xls(file_path, test_case):
    try:
        test_data_df = pd.read_excel(file_path, sheet_name=test_case)

        test_data = [tuple(row)
                     for row in test_data_df.to_records(index=False)]

        return test_data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None


def test_add_deal():
    test_data_file_path = 'test_data/test_data.xls'

    # Чтение тестовых данных для сценария 'open_new_deal'
    open_new_deal_data = read_test_data_from_xls(
        test_data_file_path, 'open_new_deal')

    if open_new_deal_data is None:
        pytest.skip("Ошибка при чтении тестовых данных: файл не найден")

    # Чтение тестовых данных для других сценариев
    # ...

    deal_manager = DealManager()

    # Тестирование для сценария 'open_new_deal'
    for row in open_new_deal_data:
        transaction = deal_manager.deal_transaction(row)
        deal_manager.add_deal(transaction)

        # Проверка результатов
        # ...

    # Тестирование для других сценариев
    # ...
