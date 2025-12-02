import unittest
import day_02 as day

DAY = "02"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 1227775554

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 4174379265

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

    def test_2_1(self):
        cases = [
            ("11-22", 11+22),
            ("99-115", 99+111),
            ("998-1012", 999+1010),
        ]

        for test_data, expected in cases:
            with self.subTest(test_data=test_data, expected=expected):
                result = day.part_2(test_data)
                self.assertEqual(result, expected)

    def test_part2_invalid(self):
        cases = [
            ("11", True),
            ("12", False),
            ("22", True),
            ("99", True),
            ("111", True),
            ("100", False),
            ("101", False),
            ("102", False),
            ("103", False),
            ("104", False),
            ("110", False),
        ]

        for test_data, expected in cases:
            with self.subTest(test_data=test_data, expected=expected):
                result = day.test_ID_invalid(test_data)
                self.assertEqual(result, expected)



if __name__ == '__main__':
    unittest.main()