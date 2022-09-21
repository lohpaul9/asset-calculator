import json

from rest_framework.test import APIRequestFactory
from django.test import TestCase
from .. import views
from .. import models

class TestUserAuthToken(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory(HELLO="FALSE")
        self.new_user_1 = {"username": "paul3",
                    "password": "12345"}
        request = self.factory.post("signup", self.new_user_1, format='json')
        view = views.UserSignUp.as_view()
        self.user_1_token = view(request).data["token"]
        self.authentication_string = "Token " + self.user_1_token

        self.new_user_2 = {"username": "paul4",
                           "password": "12345"}

        self.cash_entry_data_1 = {
            "date": "2022-01-01",
            "single_entries": [
                {
                    "currency": "USD",
                    "quantity": 1.0
                },
                {
                    "currency": "SGD",
                    "quantity": 2.0
                },
                {
                    "currency": "HKD",
                    "quantity": 3.0
                }
            ]
        }

        self.cash_entry_data_2 = {
            "date": "2022-01-02",
            "single_entries": [
                {
                    "currency": "USD",
                    "quantity": 4.0
                },
                {
                    "currency": "SGD",
                    "quantity": 5.0
                },
                {
                    "currency": "HKD",
                    "quantity": 6.0
                }
            ]
        }

        self.stocktrxn_data_1 = {
            "date": "2022-01-01",
            "ticker": "BABA",
            "quantity": 100,
            "price": 101,
            "type": "b"
        }

        self.stocktrxn_data_2 = {
            "date": "2022-01-02",
            "ticker": "D05.SI",
            "quantity": 200,
            "price": 201,
            "type": "b"
        }

        self.analysis_dates = {
            "date_bef":"2022-1-1",
            "date_aft":"2022-1-2",
            "currency":"HKD"
        }

    def test_signup_login_with_token(self):
        request = self.factory.post("signup", self.new_user_2, format='json')
        view = views.UserSignUp.as_view()
        token1 = view(request).data

        request = self.factory.post("login", self.new_user_2, format='json')
        view = views.ObtainAuthToken.as_view()
        token2 = view(request).data

        self.assertEqual(token1, token2)

    def test_access_user_view_with_token(self):
        request_test_logged_in = self.factory.get("", HTTP_AUTHORIZATION=self.authentication_string)
        user_login_view = views.FullUserDetail.as_view()
        response = user_login_view(request_test_logged_in)
        self.assertEqual(200, response.status_code)

    def test_access_stocktrxn_view_with_token(self):
        request_test_logged_in = self.factory.get("/stocktrxn/", HTTP_AUTHORIZATION=self.authentication_string)
        stock_trxn_view = views.StockTrxnList.as_view()
        response = stock_trxn_view(request_test_logged_in)
        self.assertEqual(200, response.status_code)

    def test_access_cashentry_view_with_token(self):
        request_test_logged_in = self.factory.get("/cashentries/", HTTP_AUTHORIZATION=self.authentication_string)
        cash_entry_view = views.CashEntryList.as_view()
        response = cash_entry_view(request_test_logged_in)
        self.assertEqual(200, response.status_code)

    def test_post_cashentry_view_with_token(self):
        request_test_logged_in = self.factory.post("/cashentries/", self.cash_entry_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_view = views.CashEntryList.as_view()
        response = cash_entry_view(request_test_logged_in)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(models.CashEntry.objects.all()))

    def test_put_cashentry_view_with_token(self):
        request_post_logged_in = self.factory.post("/cashentries/", self.cash_entry_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_view = views.CashEntryList.as_view()
        post_response = cash_entry_view(request_post_logged_in)
        new_id = post_response.data['id']

        request_put_logged_in = self.factory.put(f"/cashentries/{new_id}", self.cash_entry_data_2,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_detail_view = views.CashEntryDetail.as_view()
        put_response = cash_entry_detail_view(request_put_logged_in, pk=new_id)
        self.assertEqual(200, put_response.status_code)
        self.assertEqual(1, len(models.CashEntry.objects.all()))

    def test_delete_cashentry_view_with_token(self):
        request_post_logged_in = self.factory.post("/cashentries/", self.cash_entry_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_view = views.CashEntryList.as_view()
        post_response = cash_entry_view(request_post_logged_in)
        new_id = post_response.data['id']

        request_del_logged_in = self.factory.delete(f"/cashentries/{new_id}",
                                                   HTTP_AUTHORIZATION=self.authentication_string)
        cash_entry_detail_view = views.CashEntryDetail.as_view()
        del_response = cash_entry_detail_view(request_del_logged_in, pk=new_id)
        self.assertEqual(204, del_response.status_code)
        self.assertEqual(0, len(models.CashEntry.objects.all()))

    def test_access_stocktrxn_view_with_token(self):
        request_test_logged_in = self.factory.get("/stocktrxn/", HTTP_AUTHORIZATION=self.authentication_string)
        stocktrxn_view = views.StockTrxnList.as_view()
        response = stocktrxn_view(request_test_logged_in)
        self.assertEqual(200, response.status_code)

    def test_post_stocktrxn_view_with_token(self):
        request_post_logged_in = self.factory.post("/stocktrxn/", self.stocktrxn_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_view = views.StockTrxnList.as_view()
        response = stocktrxn_view(request_post_logged_in)
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, len(models.StockTrxn.objects.all()))

    def test_put_cashentry_view_with_token(self):
        request_post_logged_in = self.factory.post("/stocktrxn/", self.stocktrxn_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_view = views.StockTrxnList.as_view()
        post_response = stocktrxn_view(request_post_logged_in)
        self.assertEqual(201, post_response.status_code)
        new_id = post_response.data['id']

        request_put_logged_in = self.factory.put(f"/stocktrxn/{new_id}", self.stocktrxn_data_2,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_detail_view = views.StockTrxnDetail.as_view()
        put_response = stocktrxn_detail_view(request_put_logged_in, pk=new_id)
        self.assertEqual(200, put_response.status_code)
        self.assertEqual(1, len(models.StockTrxn.objects.all()))

    def test_delete_cashentry_view_with_token(self):
        request_post_logged_in = self.factory.post("/stocktrxn/", self.stocktrxn_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_view = views.StockTrxnList.as_view()
        post_response = stocktrxn_view(request_post_logged_in)
        self.assertEqual(201, post_response.status_code)
        new_id = post_response.data['id']

        request_del_logged_in = self.factory.delete(f"/stocktrxn/{new_id}",
                                                 HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_detail_view = views.StockTrxnDetail.as_view()
        del_response = stocktrxn_detail_view(request_del_logged_in, pk=new_id)
        self.assertEqual(204, del_response.status_code)
        self.assertEqual(0, len(models.StockTrxn.objects.all()))

    def test_user_view_with_token(self):
        request_post_stock_logged_in = self.factory.post("/stocktrxn/", self.stocktrxn_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_view = views.StockTrxnList.as_view()
        post_stock_response = stocktrxn_view(request_post_stock_logged_in)
        self.assertEqual(201, post_stock_response.status_code)
        self.assertEqual(1, len(models.StockTrxn.objects.all()))
        new_stock_id = post_stock_response.data['id']

        request_post_cash_logged_in = self.factory.post("/cashentries/", self.cash_entry_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_view = views.CashEntryList.as_view()
        post_cash_response = cash_entry_view(request_post_cash_logged_in)
        self.assertEqual(201, post_cash_response.status_code)
        self.assertEqual(1, len(models.CashEntry.objects.all()))
        new_cash_id = post_cash_response.data['id']

        request_user_logged_in = self.factory.get(f"/", HTTP_AUTHORIZATION=self.authentication_string, format='json')
        user_get_view = views.FullUserDetail.as_view()
        user_get_response = user_get_view(request_user_logged_in)

        self.assertEqual(new_stock_id, user_get_response.data[0]["stocktrxns"][0])
        self.assertEqual(new_cash_id, user_get_response.data[0]["cashentries"][0])

    def test_analysis_across_time(self):
        request_post_stock_logged_in = self.factory.post("/stocktrxn/", self.stocktrxn_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        stocktrxn_view = views.StockTrxnList.as_view()
        post_stock_response = stocktrxn_view(request_post_stock_logged_in)
        self.assertEqual(201, post_stock_response.status_code)
        self.assertEqual(1, len(models.StockTrxn.objects.all()))
        new_stock_id = post_stock_response.data['id']

        request_post_cash_logged_in = self.factory.post("/cashentries/", self.cash_entry_data_1,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        cash_entry_view = views.CashEntryList.as_view()
        post_cash_response = cash_entry_view(request_post_cash_logged_in)
        self.assertEqual(201, post_cash_response.status_code)
        self.assertEqual(1, len(models.CashEntry.objects.all()))
        new_cash_id = post_cash_response.data['id']

        request_get_analysis = self.factory.post("/acrosstime/", self.analysis_dates,
                                                   HTTP_AUTHORIZATION=self.authentication_string, format='json')
        analysis_view = views.AnalysisAcrossTime.as_view()
        post_analysis_response = analysis_view(request_get_analysis)
        analysis_data = post_analysis_response.data
        self.assertEqual(0, analysis_data["raw_total_growth"])
        self.assertEqual(0, analysis_data["percent_total_growth"])
        self.assertEqual(0, analysis_data["raw_portfolio_growth"])
        self.assertEqual(0, analysis_data["raw_profit_and_loss"])
        self.assertEqual(0, analysis_data["raw_non_market_growth"])


