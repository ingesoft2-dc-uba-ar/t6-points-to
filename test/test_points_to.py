import random
import unittest

from pyDatalog import pyDatalog
from src.points_to import PointsToAnalyzer

JAVA_SNIPPET = """
class T {
  void m() {
    A x = new A();
    A y = new A();
    x.f = y;
    A z = x.f;
    A xx;
    xx = y;
  }
}
"""


class PointsToTester(unittest.TestCase):
    def test_extract_facts(self):
        with open('test.java', 'w') as f:
            f.write(JAVA_SNIPPET)

        pta = PointsToAnalyzer()
        new_facts, assign_facts, store_facts, load_facts = pta.extract_facts('test.java')

        self.assertEqual([('x', 'Obj0'), ('y', 'Obj1')], new_facts)
        self.assertEqual([('xx', 'y')], assign_facts)
        self.assertEqual([('x', 'f', 'y')], store_facts)
        self.assertEqual([('z', 'x', 'f')], load_facts)


if __name__ == '__main__':
    unittest.main()
