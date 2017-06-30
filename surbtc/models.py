import math
from collections import namedtuple
from datetime import datetime


def parse_datetime(datetime_str):
    return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')


class Amount(
    namedtuple('amount', [
        'amount',
        'currency',
    ])
):

    @classmethod
    def create_from_json(cls, amount):
        if amount:
            amount = cls(
                amount=float(amount[0]),
                currency=amount[1],
            )
        return amount


class PagesMeta(
    namedtuple('meta', [
        'current_page',
        'total_count',
        'total_pages',
    ])
):

    @classmethod
    def create_from_json(cls, meta):
        if meta:
            return cls(
                current_page=meta['current_page'],
                total_count=meta['total_count'],
                total_pages=meta['total_pages']
            )
        return meta


class Market(
    namedtuple('market', [
        'id',
        'name',
        'base_currency',
        'quote_currency',
        'minimum_order_amount',
    ]),
):

    @classmethod
    def create_from_json(cls, market):
        return cls(
            id=market['id'],
            name=market['name'],
            base_currency=market['base_currency'],
            quote_currency=market['quote_currency'],
            minimum_order_amount=Amount.create_from_json(
                market['minimum_order_amount']
            ),
        )


class Ticker(
    namedtuple('ticker', [
        'last_price',
        'min_ask',
        'max_bid',
        'volume',
        'price_variation_24h',
        'price_variation_7d'
    ])
):

    @classmethod
    def create_from_json(cls, ticker):
        return cls(
            last_price=Amount.create_from_json(ticker['last_price']),
            min_ask=Amount.create_from_json(ticker['min_ask']),
            max_bid=Amount.create_from_json(ticker['max_bid']),
            volume=Amount.create_from_json(ticker['volume']),
            price_variation_24h=float(ticker['price_variation_24h']),
            price_variation_7d=float(ticker['price_variation_7d']),
        )


class Quotation(
    namedtuple('quotation', [
        'amount',
        'base_balance_change',
        'base_exchanged',
        'fee',
        'incomplete',
        'limit',
        'order_amount',
        'quote_balance_change',
        'quote_exchanged',
        'type',
    ])
):

    @classmethod
    def create_from_json(cls, quotation):
        return cls(
            amount=Amount.create_from_json(
                quotation['amount']),
            base_balance_change=Amount.create_from_json(
                quotation['base_balance_change']),
            base_exchanged=Amount.create_from_json(
                quotation['base_exchanged']),
            fee=Amount.create_from_json(
                quotation['fee']),
            incomplete=quotation['incomplete'],
            limit=Amount.create_from_json(
                quotation['limit']),
            order_amount=Amount.create_from_json(
                quotation['order_amount']),
            quote_balance_change=Amount.create_from_json(
                quotation['quote_balance_change']),
            quote_exchanged=Amount.create_from_json(
                quotation['quote_exchanged']),
            type=quotation['type'],
        )


class OrderBookEntry(
    namedtuple('book_entry', [
        'price',
        'amount',
    ])
):

    @classmethod
    def create_from_json(cls, book_entry):
        return cls(
            price=float(book_entry[0]),
            amount=float(book_entry[1]),
        )


class OrderBook(
    namedtuple('order_book', [
        'asks',
        'bids',
    ])
):

    @classmethod
    def create_from_json(cls, order_book):
        return cls(
            asks=[OrderBookEntry.create_from_json(entry)
                  for entry in order_book['asks']],
            bids=[OrderBookEntry.create_from_json(entry)
                  for entry in order_book['bids']],
        )


class FeePercentage(
    namedtuple('fee_percentage', [
        'value',
    ])
):

    @classmethod
    def create_from_json(cls, fee_percentage):
        return cls(
            value=float(fee_percentage['value']),
        )


class Balance(
    namedtuple('balance', [
        'id',
        'account_id',
        'amount',
        'available_amount',
        'frozen_amount',
        'pending_withdraw_amount',
    ])
):

    @classmethod
    def create_from_json(cls, balance):
        return cls(
            id=balance['id'],
            account_id=balance['account_id'],
            amount=Amount.create_from_json(
                balance['amount']),
            available_amount=Amount.create_from_json(
                balance['available_amount']),
            frozen_amount=Amount.create_from_json(
                balance['frozen_amount']),
            pending_withdraw_amount=Amount.create_from_json(
                balance['pending_withdraw_amount']),
        )


class Order(
    namedtuple('order', [
        'id',
        'account_id',
        'amount',
        'created_at',
        'fee_currency',
        'limit',
        'market_id',
        'original_amount',
        'paid_fee',
        'price_type',
        'state',
        'total_exchanged',
        'traded_amount',
        'type',
    ])
):

    @classmethod
    def create_from_json(cls, order):
        return cls(
            id=order['id'],
            account_id=order['account_id'],
            amount=Amount.create_from_json(order['amount']),
            created_at=parse_datetime(order['created_at']),
            fee_currency=order['fee_currency'],
            limit=Amount.create_from_json(order['limit']),
            market_id=order['market_id'],
            original_amount=Amount.create_from_json(order['original_amount']),
            paid_fee=Amount.create_from_json(order['paid_fee']),
            price_type=order['price_type'],
            state=order['state'],
            total_exchanged=Amount.create_from_json(order['total_exchanged']),
            traded_amount=Amount.create_from_json(order['traded_amount']),
            type=order['type'],
        )


class OrderPages(
    namedtuple('order_pages', [
        'orders',
        'meta',
    ])
):

    @classmethod
    def create_from_json(cls, orders, pages_meta):
        return cls(
            orders=[Order.create_from_json(order)
                    for order in orders],
            meta=PagesMeta.create_from_json(pages_meta),
        )


class BalanceEvent(
    namedtuple('balance_event', [
        'id',
        'account_id',
        'created_at',
        'currency',
        'event',
        'event_ids',
        'new_amount',
        'new_available_amount',
        'new_frozen_amount',
        'new_frozen_for_fee',
        'new_pending_withdraw_amount',
        'old_amount',
        'old_available_amount',
        'old_frozen_amount',
        'old_frozen_for_fee',
        'old_pending_withdraw_amount',
        'transaction_type',
        'transfer_description',
    ])
):

    @classmethod
    def create_from_json(cls, event):
        return cls(
            id=event['id'],
            account_id=event['account_id'],
            created_at=parse_datetime(event['created_at']),
            currency=event['currency'],
            event=event['event'],
            event_ids=event['event_ids'],
            new_amount=event['new_amount'],
            new_available_amount=event['new_available_amount'],
            new_frozen_amount=event['new_frozen_amount'],
            new_frozen_for_fee=event['new_frozen_for_fee'],
            new_pending_withdraw_amount=event['new_pending_withdraw_amount'],
            old_amount=event['old_amount'],
            old_available_amount=event['old_available_amount'],
            old_frozen_amount=event['old_frozen_amount'],
            old_frozen_for_fee=event['old_frozen_for_fee'],
            old_pending_withdraw_amount=event['old_pending_withdraw_amount'],
            transaction_type=event['transaction_type'],
            transfer_description=event['transfer_description'],
        )


class BalanceEventPages(
    namedtuple('event_pages', [
        'balance_events',
        'meta',
    ])
):

    @classmethod
    def create_from_json(cls, events, total_count, page):
        return cls(
            balance_events=[BalanceEvent.create_from_json(event)
                            for event in events],
            meta=PagesMeta(
                current_page=page or 1,
                total_count=total_count,
                total_pages=math.ceil(total_count / len(events))),
        )


class TradeTransaction(
    namedtuple('trade_transaction', [
        'id',
        'market_id',
        'created_at',
        'updated_at',
        'amount_sold',
        'price_paid',
        'ask_order',
        'bid_order',
        'triggering_order',
    ])
):

    @classmethod
    def create_from_json(cls, transaction):
        return cls(
            id=transaction['id'],
            market_id=transaction['market_id'],
            created_at=parse_datetime(transaction['created_at']),
            updated_at=parse_datetime(transaction['updated_at']),
            amount_sold=Amount.create_from_json(
                [transaction['amount_sold'],
                 transaction['amount_sold_currency']]),
            price_paid=Amount.create_from_json(
                [transaction['price_paid'],
                 transaction['price_paid_currency']]),
            ask_order=Order.create_from_json(transaction['ask']),
            bid_order=Order.create_from_json(transaction['bid']),
            triggering_order=Order.create_from_json(
                transaction['triggering_order']),
        )

class WithdrawalData(
    namedtuple('withdrawal',[
        'target_address',
        'tx_hash',
        'type'
    ])
):

    @classmethod
    def create_from_json(cls, withdrawal):

        return cls(
            target_address=withdrawal['target_address'],
            tx_hash=withdrawal['tx_hash'],
            type=withdrawal['type']
        )

class SimulateWithdrawal(
    namedtuple('withdrawal',[
        'id',
        'created_at',
        'currency',
        'withdrawal_data',
        'amount',
        'fee',
        'state'
    ])
):

    @classmethod
    def create_from_json(cls, withdrawal):

        created_at = None
        if withdrawal['created_at']:
            created_at = parse_datetime(withdrawal['created_at'])

        return cls(
            id=withdrawal['id'],
            created_at=created_at,
            currency=withdrawal['currency'],
            withdrawal_data=WithdrawalData.create_from_json(withdrawal['withdrawal_data']),
            amount=Amount.create_from_json(withdrawal['amount']),
            fee=Amount.create_from_json(withdrawal['fee']),
            state=withdrawal['state']
        )

class AveragePrices(
    namedtuple('reports',[
        'datetime',
        'amount'
    ])
):

    @classmethod
    def create_from_json(cls, reports):

        return cls(
            datetime=reports[0],
            amount=reports[1]
        )

class Candlestick(
    namedtuple('reports',[
        'datetime',
        'open',
        'high',
        'low',
        'close',
        'volume'
    ])
):

    @classmethod
    def create_from_json(cls, reports):

        return cls(
            datetime=reports[0],
            open=reports[1],
            high=reports[2],
            low=reports[3],
            close=reports[4],
            volume=reports[5],
        )