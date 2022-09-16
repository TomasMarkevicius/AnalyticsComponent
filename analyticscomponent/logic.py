from pandas import DataFrame, read_csv
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class MalformedDataError(Exception):
    pass


def get_customers(date: str) -> int:
    orders_df = read_csv("../data/orders.csv")
    column_values = list(orders_df.get("created_at"))
    cust_count = len([i for i in column_values if i.startswith(date)])
    return cust_count


def get_order_ids_and_order_lines(date) -> Tuple[list, DataFrame]:
    orders_df = read_csv("../data/orders.csv")
    is_date = map(lambda x: x.startswith(date), orders_df['created_at'])
    discounted_orders = orders_df.loc[is_date]
    order_ids = list(discounted_orders.get("id"))

    order_lines_df = read_csv("../data/order_lines.csv")
    return order_ids, order_lines_df


def get_total_discount_amount(date: str) -> float:
    order_ids, order_lines_df = get_order_ids_and_order_lines(date)
    if not order_ids:
        return 0
    total_discount_amount = 0
    for ord_id in order_ids:
        ord_df = order_lines_df.loc[order_lines_df['order_id'] == ord_id]
        total_discount_amount += ord_df['discounted_amount'].sum()
    return total_discount_amount


def get_items(date: str) -> int:
    order_ids, order_lines_df = get_order_ids_and_order_lines(date)
    if not order_ids:
        return 0
    items = 0
    for ord_id in order_ids:
        ord_df = order_lines_df.loc[order_lines_df['order_id'] == ord_id]
        items += ord_df['quantity'].sum()
    return int(items)


def get_order_column_average(order_ids: list, order_lines_df: DataFrame, column_name: str) -> float:
    avg = 0
    for ord_id in order_ids:
        ord_df = order_lines_df.loc[order_lines_df['order_id'] == ord_id]
        avg += ord_df[column_name].sum()

    order_avg = avg / len(order_ids)
    return order_avg


def get_order_total_avg(date: str) -> float:
    order_ids, order_lines_df = get_order_ids_and_order_lines(date)
    if not order_ids:
        return 0
    order_total_avg = get_order_column_average(order_ids, order_lines_df, "total_amount")
    return order_total_avg


def get_discount_rate_avg(date: str) -> float:
    order_ids, order_lines_df = get_order_ids_and_order_lines(date)
    if not order_ids:
        return 0
    discount_rate_avg = get_order_column_average(order_ids, order_lines_df, "discount_rate")
    return discount_rate_avg


def commissions(date: str) -> dict:
    return {
        "promotions": {
            "1": 0,
            "3": 0,
            "2": 0,
            "5": 0,
            "4": 0
        },
        "total": 0,
        "order_average": 0
    }


def get_report(date: str) -> dict:
    return {
        "customers": get_customers(date),
        "total_discount_amount": get_total_discount_amount(date),
        "items": get_items(date),
        "order_total_avg": get_order_total_avg(date),
        "discount_rate_avg": get_discount_rate_avg(date),
        "commissions": commissions(date),
    }
