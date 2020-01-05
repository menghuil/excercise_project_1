from celery.schedules import crontab

from common.tasks import send_mail
from dashboard.celery import app
from product.models import Shop


@app.task(name='send_shop_sale_statistics_mail')
def send_shop_sale_statistics_mail():
    statistics = Shop.objects.get_sale_statistics()
    code_to_name = {
        'code': '館別',
        'sale_amount': '總銷售金額',
        'sale_volume': '總銷售數量',
        'order_count': '總訂單數量',
    }
    content = ''
    for record in statistics:
        content += ', '.join([
            f'{code_to_name[field]}: {value}'
            for field, value in record.items()
        ])
        content += '\n'
    title = '各館別銷售統計'
    send_mail(subject=title, message=content)


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily task
    sender.add_periodic_task(crontab(hour=0, minute=0),
                             send_shop_sale_statistics_mail.s(),
                             name='Send daily product information')
