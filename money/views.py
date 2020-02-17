import calendar
import datetime
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
import matplotlib.pyplot as plt
import pytz
from .models import Money
from .forms import SpendingForm
from .utils import index_utils
plt.rcParams['font.family'] = 'IPAPGothic'
TODAY = str(timezone.now()).split('-')
class MainView(View):
    def get(self, request, year=TODAY[0], month=TODAY[1]):
        money = Money.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
        total = index_utils.calc_month_pay(money)
        index_utils.format_date(money)
        form_add = SpendingForm()
        #form_delete = DeleteForm()
        next_year, next_month = index_utils.get_next(year, month)
        prev_year, prev_month = index_utils.get_prev(year, month)
        context = {'year' : year,
                'month' : month,
                'prev_year' : prev_year,
                'prev_month' : prev_month,
                'next_year' : next_year,
                'next_month' : next_month,
                'money' : money,
                'total' : total,
                'form_add' : form_add,
               # 'form_delete' : form_delete,
                }
        self.draw_graph(year, month)
        return render(request, 'money/index.html', context)
    def post(self, request, year=TODAY[0], month=TODAY[1]):
        data = request.POST
        if 'add' in data.keys():
            self.register_payment(data)
        elif 'delete' in data.keys():
            self.delete_payment(data)
        return redirect(to='/money/{}/{}'.format(year, month))
    def register_payment(self, data):
        use_date = data['use_date']
        cost = data['cost']
        detail = data['detail']
        category = data['category']
        use_date = timezone.datetime.strptime(use_date, "%Y/%m/%d")
        tokyo_timezone = pytz.timezone('Asia/Tokyo')
        use_date = tokyo_timezone.localize(use_date)
        use_date += datetime.timedelta(hours=9)
        Money.objects.create(
                use_date = use_date,
                detail = detail,
                cost = int(cost),
                category = category,
                )
        return None
    def delete_payment(self, data):
        year = data['year']
        use_date = data['use_date']
        detail = data['detail']
        cost = data['cost']
        use_date = '/'.join([year, use_date])
        use_date = timezone.datetime.strptime(use_date, '%Y/%m/%d')
        use_date = use_date.date()
        Money.objects.filter(
                use_date__iexact=use_date,
                detail__iexact=detail,
                cost__iexact=cost
                ).delete()
        return None
    #描画に関連する部分
    def draw_graph(self, year, month):
        money = Money.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
        last_day = calendar.monthrange(int(year), int(month))[1] + 1
        day = [i for i in range(1, last_day)]    #日付
        cost = [0 for i in range(len(day))]    #支出
        for m in money:
            #1日の支出を計算していく
            cost[int(str(m.use_date).split('-')[2])-1] += int(m.cost)
        #文字列に変換してカンマでつなげる
        text_day = ','.join(list(map(str, day)))
        text_cost = ','.join(list(map(str, cost)))
        #JSONテンプレート
        json_template = """var json = {
            type: 'bar',
            data: {
                labels: [
        """ + str(text_day) + """    
                ],
                datasets: [{
                    label: '支出',
                    data: [
        """ + str(text_cost) + """ 
                    ],
                    borderWidth: 2,
                    strokeColor: 'rgba(0,0,255,1)', 
                    backgroundColor: 'rgba(0,191,255,0.5)' 
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero:true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '日付',
                            fontsize: 18
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            beginAtZero:true
                        },
                        scaleLabel: {
                            display: true,
                            labelString: '支出額 (円)',
                            fontsize: 18
                        }
                    }]
                },
                responsive: true
            }
        }
        """
        with open('money/static/money/js/data.js', 'w') as f:    #data.jsを開いて書き込む
            f.write(json_template)