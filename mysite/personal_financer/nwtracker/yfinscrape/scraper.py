import logging
import yfinance as yf

class YFinScraper:
    def get_general_stock_info(self, ticker: str):
        print('loading gen_info: ', ticker)
        stock_data = yf.Ticker(ticker).info
        if 'shortName' not in stock_data.keys():
            logging.error(f"{ticker} is not a valid ticker. Unable to load")
            raise ValueError
        else:
            print('loaded gen_info: ', ticker, stock_data['shortName'],
                  stock_data['regularMarketPrice'], stock_data['currency'])
        return stock_data

    def find_hist_price(self, ticker_list: [str]) -> dict:
        print('loading hist stock info: ', ' '.join(ticker_list))
        hist_all = yf.download(' '.join(ticker_list), interval='1d', period='max')
        hist_price_dict = {}
        for ticker in ticker_list:
            if len(ticker_list) > 1:
                ticker_hist = hist_all['Close'][ticker]
            else:
                ticker_hist = hist_all['Close']

            hist_dict = ticker_hist.to_dict()
            hist_sorted_list = [(k.to_pydatetime(), v) for k,v in hist_dict.items()]
            hist_price_dict[ticker] = hist_sorted_list
        return hist_price_dict
