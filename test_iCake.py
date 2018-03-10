import unittest
import iCake
import database

class TestICake(unittest.TestCase):
    
    def setUp(self):
       self.order1  = database.Order(order_number = 1)
       self.order2  = database.Order(order_number = 2)
       self.orders = []
       self.orders.append(self.order1)
       self.orders.append(self.order2)
        
        
    def test_find_order_by_id2(self):
        self.assertEqual(iCake.find_order_by_id2(self.orders,1),self.order1)


if __name__ == '__main__':
    unittest.main()