import unittest
import xmlrunner


from logic.class_example import Calculator as cal

class TestCalculator (unittest.TestCase):
    """
    Test calculator def
    """

    def test_sum (self):
        """
        Test sum
        """
        validator = cal()
        
        self.assertEqual(validator.sum(5,5),10)



if __name__ == '__main__':
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        # these make sure that some options that are not applicable
        # remain hidden from the help menu.
        failfast=False, buffer=False, catchbreak=False)