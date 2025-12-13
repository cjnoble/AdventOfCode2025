import unittest
import day_10 as day
import numpy as np

DAY = "10"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 7

        result = day.part_1(test_data)

        self.assertEqual(result, expected)

    def test_1_simple(self):

        expected = 1

        result = day.part_1([r"[##] (0) (1) (0,1) {}"])

        self.assertEqual(result, expected)

    def test_1_simple_2(self):

        expected = 3

        result = day.part_1([r"[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"])

        self.assertEqual(result, expected)

    def test_2(self):

        expected = 33

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

    def test_test_x_candidate(self):

        M = np.array([
            [1, 1, 0],  # equation 0
            [0, 1, 1],  # equation 1
        ])

        target_vector = np.array([3, 4])
        x_candidate = (1, 2, 2)

        result = day.test_x_candidate(M, target_vector, x_candidate)

        self.assertEqual(result, sum(x_candidate))


if __name__ == '__main__':
    unittest.main()