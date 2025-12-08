import unittest
import day_08 as day

DAY = "08"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 40

        result = day.part_1(test_data, 10)

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 25272

        result = day.part_2(test_data)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()