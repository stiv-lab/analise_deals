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
        expected_results = test_data.iloc[-1][['open_len', 'open-qty', 'open-amount_point', 'open-amount',
                                               'close-len', 'close-qty', 'close-amoun_point', 'close-amount']]

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


def main():
    test_add_deal()


if __name__ == '__main__':
    main()
