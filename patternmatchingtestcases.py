import unittest

from boyermoore import boyermooregalils 

class TestPatternMatching(unittest.TestCase):
    
    def test_run_pattern_matching(self):
        text = "GEEKS FOR GEEKS"
        pattern = "GEEK"
        print(boyermooregalils(text, pattern))
        self.assertEqual(boyermooregalils(text, pattern), [1,11])
        
        text = "ABABDABACDABABCABAB"
        pattern = "ABABCABAB"
        self.assertEqual(boyermooregalils(text, pattern), [11])
        
        text = "AAAAA"
        pattern = "AAA"
        self.assertEqual(boyermooregalils(text, pattern), [1,2,3])
        
        text = "THIS IS A TEST TEXT"
        pattern = "TEST"
        self.assertEqual(boyermooregalils(text, pattern), [11])
        
        text = "dbcdbcdabdbcdabddbcdbcdabcb"
        pattern = "dbc"
        self.assertEqual(boyermooregalils(text, pattern), [1, 4, 10, 17, 20])
        
        text = "aaaaaaaaa"
        pattern = "aaa"
        self.assertEqual(boyermooregalils(text, pattern), [1, 2, 3, 4, 5, 6, 7])
        
        
if __name__ == "__main__":
    unittest.main()