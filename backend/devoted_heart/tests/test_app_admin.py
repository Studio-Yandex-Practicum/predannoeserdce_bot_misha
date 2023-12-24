from django.test import TestCase  # RequestFactory
from app.admin import FAQAdmin, CustomerAdmin, MessagesAdmin
from app.models import FAQ, Customer, Messages


class FAQAdminTest(TestCase):

    def test_list_display(self):
        faq_admin = FAQAdmin(FAQ, None)
        self.assertEqual(faq_admin.list_display, ('pk', 'question', 'order'))


class CustomerAdminTest(TestCase):

    def test_list_display(self):
        customer_admin = CustomerAdmin(Customer, None)
        self.assertEqual(
            customer_admin.list_display,
            ('pk', 'name', 'email', 'tg_id', 'phone')
        )


class MessagesAdminTest(TestCase):

    def test_list_display(self):
        messages_admin = MessagesAdmin(Messages, None)
        self.assertEqual(
            messages_admin.list_display,
            ('text', 'image', 'selected')
        )
