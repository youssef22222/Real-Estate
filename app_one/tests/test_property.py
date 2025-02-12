from odoo.tests.common import TransactionCase
from odoo import fields

class TestProperty(TransactionCase):

    def setUp(self,*args,**kwargs):
        super().setUp()

        self.property_01_record = self.env["property"].create({
            'ref':'PRT001',
            'name':'Property 1',
            'description':'Property 1 description',
            'postcode':'1001',
            'date_availability':fields.date.today(),
            'bedrooms':2,
            'expected_price':10000,
            'garden':True,
        })

    def test_01_property_values(self):

        self.assertRecordValues(self.property_01_record,[{
            'ref': 'PRT001',
            'name': 'Property 1',
            'description': 'Property 1 description',
            'postcode': '1001',
            'date_availability': fields.date.today(),
            'bedrooms': 2,
            'expected_price': 10000,
            'garden': True,
        }])