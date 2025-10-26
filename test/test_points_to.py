import random
import unittest

from pyDatalog import pyDatalog


# los terminos de datalog solo pueden ser definidos a nivel de modulo :-/
pyDatalog.create_terms("PointsTo, New, Assign, X, Y, O")


class PointsToTester(unittest.TestCase):
    def test_order(self):
        """Chequea que el orden en que se pasan los facts no altera el resultado"""
        facts = [
            "+New('a', 'obj1')",
            "+New('b', 'obj2')",
            "+Assign('b', 'a')",
            "+Assign('a', 'b')",
            "+Assign('c', 'b')",
            "+Assign('c', 'a')"
        ]

        random.seed(123456)
        results = []
        for i in range(10):
            pyDatalog.clear()
            PointsTo(X, O) <= New(X, O)
            PointsTo(X, O) <= Assign(X, Y) & PointsTo(Y, O)
            for fact in random.sample(facts, k=len(facts)):
                eval(fact)
  
            result = set(PointsTo(X, O).data)
            results.append(result)

        # comparamos que todos sean iguales al primero (es decir, todos iguales entre si)
        for i in range(1, 10):
            self.assertEqual(results[0], results[i])


if __name__ == '__main__':
    unittest.main()
