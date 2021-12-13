from celery import Task
from django.core.mail import send_mail
from .models import Order

@Task
def order_created(order_id):
    """
    Tarefa para enviar uma notificação por email quando um pedido for criado com sucesso.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order_id}'
    message = f'Dear {order.first_name}, \n\n You have sucessfuly placed an order. You order ID is {order.id}.'
    mail_sent = send_mail(subject=subject, message=message, from_email='admin@myshop.com', recipient_list=[order.email])
    return mail_sent