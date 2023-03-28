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
        expected_results = test_data.iloc[-1][['результат1', 'результат2', 'результат3', 'результат4',
                                               'результат5', 'результат6', 'результат7', 'результат8']]

        return test_data, expected_results
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None


@pytest.mark.parametrize("test_case", [
    'open_new_long',
    'accumulate_long',
    'close_long',
    'accumulate_short',
    'close_short',
    'split_accumulation_long_1_2',
    'split_accumulation_long_2_3',
    'split_accumulation_short_1_2',
    'split_accumulation_short_2_3'
])
def test_add_deal(test_case):
    test_data_file_path = 'test_data/test_data.xls'
    deal_manager = DealManager()

    # Чтение тестовых данных для текущего сценария
    test_data, expected_results = read_test_data_from_xls(
        test_data_file_path, test_case)

    # ...

    # Тестирование для текущего сценария
    for i, row in test_data.iterrows():
        transaction = deal_manager.deal_transaction(row)
        deal_manager.add_deal(transaction)

    # Проверка результатов с ожидаемыми значениями
    for col, expected_result in expected_results.iteritems():
        if not pd.isna(expected_result):
            result = getattr(deal_manager, col)
            assert result == expected_result, f"Ошибка сценария {test_case} в прое {col}: ожидалось {expected_result}, получено {result}"

    print(f"Test case {test_case}: ок")


"""
def test_add_deal():
    test_data_file_path = 'test_data/test_data.xls'
    test_cases = ['open_new_long',
                  'accumulate_long',
                  'close_long',
                  'accumulate_short',
                  'close_short',
                  'split_accumulation_long_1_2',
                  'split_accumulation_long_2_3',
                  'split_accumulation_short_1_2',
                  'split_accumulation_short_2_3']


    # Чтение тестовых данных для текущего сценария
    test_data, expected_results = read_test_data_from_xls(
        test_data_file_path, test_case)

    if test_data is None:
        pytest.skip("Ошибка при чтения файл не найден")
    if len(test_data) == 0:
        pytest.skip(
            f"Ошибка при чтении тестовых данных для сценария '{test_case}': данные для сценария не найдены")

    # Тестирование для текущего сценария
    for i, row in test_data.iterrows():
        transaction = deal_manager.deal_transaction(row)
        deal_manager.add_deal(transaction)

    # Проверка результатов с ожидаемыми значениями
    results_mapping = {
        'open-len': len(deal_manager.deals_open),
        'open-qty': deal_manager.deals_open.iloc[0]['qty'] if not deal_manager.deals_open.empty else None,
        'open-amount_point': deal_manager.deals_open.iloc[0]['amoint_point'] if not deal_manager.deals_open.empty else None,
        'open-amount': deal_manager.deals_open.iloc[0]['amoint'] if not deal_manager.deals_open.empty else None,
        'close-len': len(deal_manager.deals_close),
        'close-qty': deal_manager.deals_close.iloc[0]['qty'] if not deal_manager.deals_close.empty else None,
        'close-amount_point': deal_manager.deals_close.iloc[0]['amoint_point'] if not deal_manager.deals_close.empty else None,
        'close-amount': deal_manager.deals_close.iloc[0]['amoint'] if not deal_manager.deals_close.empty else None
    }

    for col, expected_result in expected_results.iteritems():
        if not pd.isna(expected_result):
            result = results_mapping[col]
            assert result == expected_result, f"Ошибка сценария {test_case}: ожидалось {expected_result}, получено {result}"

    print(f"Test case {test_case}: ок")

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

        elif test_case == 'accumulate_short':
            assert len(
                deal_manager.deals_open) == 1, f"Ошибка сценария {test_case}"
            assert deal_manager.deals_open.iloc[0]['qty'] == 2, f"Ошибка сценария {test_case}"

        elif test_case == 'close_short':
            assert len(
                deal_manager.deals_open) == 0, f"Ошибка сценария {test_case}"
            assert len(
                deal_manager.deals_close) == 1, f"Ошибка сценария {test_case}"
        
        print(f"Test case {test_case}: ок")
    # Тестирование для других сценариев
    # ...
"""


def main():
    test_add_deal()


if __name__ == '__main__':
    main()
