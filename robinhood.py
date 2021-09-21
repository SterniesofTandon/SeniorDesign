import robin_stocks as robin
import pandas as pd
# import numpy as np
# import ta as ta
from pandas.plotting import register_matplotlib_converters
# from ta import *
# from misc import *
# from tradingstats import *
from getpass import getpass


USERNAME = None
PASS = None

# Log in to Robinhood
# TODO encrypt USERNAME and PASS in config.py
attempt = 0


def robin_login():
    USERNAME = input("Enter Robinhood Username: ")
    PASS = getpass("Enter Robinhood Password: ")
    try:
        robin.login(USERNAME, PASS, store_session=False)
    except Exception:
        print("Invalid login attempt to Robinhood.")
        print("Attempts left: {}".format((3 - attempt - 1)))


# return by Zero function
def safe_division(n, d):
    return n/d if d else 0


def get_watchlist_symbols():
    """
    Returns: Tickers for stocks on the watchlist
    """
    watchlist_names = []
    tickers = []
    # diction = robin.get_all_watchlists(info=None)
    # specific WatchList to evaluate (can also do all if remove)
    watchlist = 'My First List'

    for name in robin.get_all_watchlists(info="results"):
        watchlist_names.append(name["display_name"])

    # Can iterate through all watchlists, but this is set for a specific
    for name in watchlist_names:
        if name == watchlist:
            print("NAME", name, "------------------------------------------")
            lists = robin.account.get_watchlist_by_name(name)["results"]
            # print("Lists", lists)
            # print("TESTING", lists[1].get('instrument'))
            for item in lists:
                tickers.append(item.get('symbol'))

                # TODO why would I need to do it by url??
                # instrument_data = robin.get_instrument_by_url(
                # item.get('instrument'))
                # symbol = instrument_data['symbol']
                # tickers.append(symbol)
    return tickers


def get_holdings():
    """Returns dictionary of the currently held stocks"""
    my_stocks = robin.build_holdings()
    # stores in dataframe
    df = pd.DataFrame(my_stocks)
    df = df.transpose()
    df['ticker'] = df.index
    df = df.reset_index(drop=True)
    return df


def get_portfolio_symbols():
    """
    Returns: the symbol for each stock in your portfolio as a list of strings
    """
    symbols = []
    data = get_holdings()
    data = data.loc[:, "ticker"]
    symbols = data.tolist()
    return symbols

    # positions_data = robin.build_holdings()
    # for item in positions_data:
    #     if not item:
    #         continue
    #     # TODO why would I need to do it by url??
    #     symbols.append(item.get('symbol'))

    #     # instrument_data = robin.get_instrument_by_url(
    #           item.get('instrument'))
    #     # symbol = instrument_data['symbol']
    #     # symbols.append(symbol)


def get_position_creation_date(symbol, holdings_data):
    """Returns the time at which we bought a certain stock in our portfolio
    Args:
        symbol(str): Symbol of the stock that we are trying to figure out when
                    it was bought
        holdings_data(dict): dict returned by robin.get_open_stock_positions()
    Returns:
        String containing the date and time the stock was bought, or
                "Not found"
    """
    instrument = robin.get_instruments_by_symbols(symbol)
    url = instrument[0].get('url')
    for dict in holdings_data:
        if(dict.get('instrument') == url):
            return dict.get('created_at')
    return "Not found"


def get_modified_holdings():
    """Retrieves same dictionary as with robin.build_holdings but includes
        information when the stock was purchased
        - useful for the read_trade_history() method in tradingstats.py """
    holdings = robin.build_holdings()
    holdings_data = robin.get_open_stock_positions()
    for symbol, dict in holdings.items():
        bought_at = get_position_creation_date(symbol, holdings_data)
        bought_at = str(pd.to_datetime(bought_at))
        holdings[symbol].update({'bought_at': bought_at})
    return holdings


def search_stock(ticker):
    """ Gets historical data and plot for the passed in ticker"""
    stock_data = robin.get_stock_historicals(ticker, span='week',
                                             bounds='regular')
    searched_stock = pd.DataFrame(stock_data)
    print(searched_stock)
    # switching to floats so pyplot can read the numbers
    column_list = ['close_price', 'high_price', 'low_price', 'open_price']
    for ind in column_list:
        searched_stock[ind] = searched_stock[ind].astype(float)
    # plot the stock
    searched_stock['close_price'].plot(legend=True, figsize=(12, 5))


def scan_stock():
    """Main method. First runs a scan of the stocks.
        Gives an analysis of possible stocks to buy and sell """

    print("---- Login ----")
    robin_login()
    print("---- Starting Scan ... ----" + "\n")
    # register datetime, timestamp, etc
    register_matplotlib_converters()

    # get_watchlist_symbols()s
    watchlist_symbols = get_watchlist_symbols()
    print("Watchlist", watchlist_symbols)
    portfolio_symbols = get_portfolio_symbols()
    print("Porfolio")
    print(portfolio_symbols)
    holdings_data = get_modified_holdings()
    print("holdings_data")
    print(holdings_data)

    # check the current stocks held
    # get_holdings()

    # update_trade_history(sells, holdings_data, "tradehistory.txt")
    print("----- Scan over -----\n")

    print("Logged Out")
    robin.authentication.logout()


scan_stock()
