import unittest
import day_09 as day

DAY = "09"
test_data = day.read_text_file(f"{DAY}_test.txt")

class TestMethods(unittest.TestCase):

    def test_1(self):

        expected = 50

        result = day.part_1(test_data)

        self.assertEqual(result, expected)


    def test_1_additional(self):

        expected = 101
        data = ["100, 0", "0, 0"]

        result = day.part_1(data)

        self.assertEqual(result, expected)

    def test_1_24(self):

        expected = 24
        data = ["2,5", "9,7"]

        result = day.part_1(data)

        self.assertEqual(result, expected)

    def test_1_50(self):

        expected = 50
        data = ["2,5", "11, 1"]

        result = day.part_1(data)

        self.assertEqual(result, expected)

    def test_1_50_2(self):

        expected = 50
        data = ["5,2", "1, 11"]

        result = day.part_1(data)

        self.assertEqual(result, expected)


    def test_rectangle_intersects_polygon(self):
        expected = False

        points = [day.Point.from_input(row) for row in test_data]

        h_edges, v_edges = day.classify_polygon_edges(points)

        result = day.rectangle_intersects_polygon(day.Point(9, 5), day.Point(2, 3), h_edges, v_edges)

        self.assertEqual(result, expected)


    def test_2(self):

        expected = 24

        result = day.part_2(test_data)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()