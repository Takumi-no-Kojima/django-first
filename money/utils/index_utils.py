def calc_month_pay(money):
    total = 0
    for m in money:
        total += m.cost
    return total

def format_date(money):
    for m in money:
        date = str(m.use_date).split(' ')[0]
        m.use_date = '/'.join(date.split('-')[1:3])
    return None

def get_next(year, month):
    year = int(year)
    month = int(month)
    if month == 12:
        return str(year + 1), '1'
    else:
        return str(year), str(month + 1)

def get_prev(year, month):
    year = int(year)
    month = int(month)
    if month == 1:
        return str(year - 1), '12'
    else:
        return str(year), str(month - 1)

def draw_graph(year, month):
    money = Money.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
    last_day = calendar.monthrange(int(year), int(month))[1] + 1
    day = [i for i in range(1, last_day)]
    cost = [0 for i in range(len(day))]
    for m in money:
        cost[int(str(m.use_date).split('-')[2])-1] += int(m.cost)
    plt.figure()
    plt.bar(day, cost, color='#00bfff', edgecolor='#0000ff')
    plt.grid(True)
    plt.xlim([0, 31])
    plt.xlabel('日付', fontsize=16)
    plt.ylabel('支出額(円)', fontsize=16)
    plt.savefig('money/static/images/bar_{}_{}.svg'.format(year, month), transparent=True)
    return None