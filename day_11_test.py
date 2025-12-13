import unittest
import day_11 as day

DAY = "11"
test_data = day.read_text_file(f"{DAY}_test.txt")
test_data2 = day.read_text_file(f"{DAY}_test_2.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 5

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 2

        result = day.part_2(test_data2)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()