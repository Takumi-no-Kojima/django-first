import datetime
from django.urls import resolve
from django.utils import timezone
from django.test import TestCase
from money.models import Money
from money.views import index
#...
class TestURL(TestCase):
    def test_URL_resolve(self):
        url = resolve('/money/')
        self.assertEqual(url.func, index)    #上のURLでindexが呼ばれるか
        url = resolve('/money/2018/11')
        self.assertEqual(url.func, index)    #上のURLでindexが呼ばれるか