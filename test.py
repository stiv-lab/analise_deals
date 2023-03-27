# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:49:54 2023

@author: Origo
"""
import pandas as pd
import pytest
from mod_deals import DealManager


def read_test_data_from_xls(file_path, test_case):
    try:
        data = pd.read_excel(file_path)

        test_data = data[data['test_case'] == test_case]

        return test_data
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None


def test_add_deal():
    test_data_file_path = 'test_data/test_data.xls'
    test_cases = ['open_new_long_deal',
                  'accumulate_deal_long',
                  'close_deal_long',
                  'accumulate_deal_short',
                  'close_deal_short',
                  'split_accumulation_lond_deal',
                  'split_accumulation_short_deal']

    for test_case in test_cases:
        deal_manager = DealManager()

        # Чтение тестовых данных для текущего сценария
        test_data = read_test_data_from_xls(test_data_file_path, test_case)

        if test_data is None:
            pytest.skip("Ошибка при чтения файл не найден")
            continue
        if len(test_data) == 0:
            pytest.skip(
                f"Ошибка при чтении тестовых данных для сценария '{test_case}': данные для сценария не найдены")
            continue

        # удаляем первый столбец с наз тестов, что бы df соответствовал рабочему файлу
        test_data = test_data.drop(columns=test_data.columns[0])

        # Тестирование для текущего сценария
        for i, row in test_data.iterrows():
            transaction = deal_manager.deal_transaction(row)
            deal_manager.add_deal(transaction)

        # 1. накопление первой транзации "Покупка"
        if test_case == 'open_new_long_deal':
            assert len(
                deal_manager.deals_open) == 1, f"Ошибка сценария {test_case}"
            assert deal_manager.deals_open.iloc[0]['qty'] == - \
                1, f"Ошибка сценария {test_case}"
        # 2.
        elif test_case == 'accumulate_deal_long':
            assert len(
                deal_manager.deals_open) == 1, f"Ошибка сценария {test_case}"
            assert deal_manager.deals_open.iloc[0]['qty'] == - \
                2, f"Ошибка сценария {test_case}"
        # 3.
        elif test_case == 'close_deal_long':
            assert len(
                deal_manager.deals_open) == 0, f"Ошибка сценария {test_case}"
            assert len(
                deal_manager.deals_close) == 1, f"Ошибка сценария {test_case}"

    # Тестирование для других сценариев
    # ...


def main():
    test_add_deal()


if __name__ == '__main__':
    main()
