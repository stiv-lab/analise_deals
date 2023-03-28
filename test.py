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
        expected_results = test_data.iloc[-1][['open_len', 'open_qty', 'open_amount_point', 'open_amount',
                                               'close_len', 'close_qty', 'close_amoun_point', 'close_amount']]

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

    # Тестирование для текущего сценария
    for i, row in test_data.iterrows():
        transaction = deal_manager.deal_transaction(row[1:22])
        deal_manager.add_deal(transaction)

    # Проверка результатов с ожидаемыми значениями
    for col, expected_result in expected_results.iteritems():
        if not pd.isna(expected_result):
            if col.endswith('_len'):
                # Убираем '_len' из имени столбца, чтобы получить имя DataFrame (open или close)
                data_frame_name = col[:-4]
                result = len(getattr(deal_manager, f"deals_{data_frame_name}"))
            else:
                # Разделяем имя столбца на имя DataFrame и имя столбца
                data_frame_name, column_name = col.split('_', 1)
                result = getattr(deal_manager, f"deals_{data_frame_name}")[
                    column_name].sum()

            assert result == expected_result, f"Ошибка сценария {test_case} в прое {col}: ожидалось {expected_result}, получено {result}"

    """
    # Проверка результатов с ожидаемыми значениями
    for col, expected_result in expected_results.iteritems():
        if not pd.isna(expected_result):
            result = getattr(deal_manager, col)
            assert result == expected_result, f"Ошибка сценария {test_case} в прое {col}: ожидалось {expected_result}, получено {result}"
    """

    print(f"Test case {test_case}: ок")


def main():
    test_add_deal('split_accumulation_short_2_3')


if __name__ == '__main__':
    main()
