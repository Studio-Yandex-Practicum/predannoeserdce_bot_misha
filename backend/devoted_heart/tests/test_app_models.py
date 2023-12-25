from django.test import TestCase
from app.models import FAQ, Customer, Messages


class FAQModelTest(TestCase):

    def test_str_representation(self):
        faq = FAQ(
            question="Test Question", answer="Test Answer", order=1
        )
        self.assertEqual(str(faq), "Test Question")


class CustomerModelTest(TestCase):

    def test_str_representation(self):
        customer = Customer(
            name="John Doe", email="john@example.com",
            tg_id="123", phone="123456789"
        )
        self.assertEqual(str(customer), "Имя: John Doe")


class MessagesModelTest(TestCase):

    def test_str_representation(self):
        customer = Customer(
            name="John Doe", email="john@example.com",
            tg_id="123", phone="123456789"
        )
        message = Messages(
            customer=customer, text="Test Message", selected=True
            )
        self.assertEqual(str(message), "Имя: John Doe - None")
