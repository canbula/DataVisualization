import logging
import numpy as np
import pandas as pd

def is_mutable(x) -> bool:
    """
    Check if the input is mutable or not
    :param x: any
    :return: bool
    """
    mutables = (list, set, dict, np.array, pd.Series, pd.DataFrame)
    immutables = (int, float, bool, complex, str, tuple)
    if isinstance(x, immutables):
        return False
    elif isinstance(x, mutables):
        return True
    else:
        raise TypeError("Type not supported")


class MutabilityTest:
    def __init__(self, start_message="[START]", end_message="[END]"):
        self.start_message = start_message
        self.end_message = end_message
        self.__types = (int, float, str, bool, complex, list, tuple, set, dict, np.array, pd.Series, pd.DataFrame)
        self._tests = [
            {"input": 1, "expected": False, "test_name": "Integer test"},
            {"input": 1.0, "expected": False, "test_name": "Float test"},
            {"input": "1", "expected": False, "test_name": "String test"},
            {"input": True, "expected": False, "test_name": "Boolean test"},
            {"input": 1j, "expected": False, "test_name": "Complex test"},
            {"input": [1, 2, 3], "expected": True, "test_name": "List test"},
            {"input": (1, 2, 3), "expected": False, "test_name": "Tuple test"},
            {"input": {1, 2, 3}, "expected": True, "test_name": "Set test"},
            {"input": {1: 1, 2: 2, 3: 3}, "expected": True, "test_name": "Dict test"},
        ]
    
    def __enter__(self):
        logging.basicConfig(format='%(levelname)s @ %(asctime)s : %(message)s', 
                            datefmt='%d.%m.%Y %H:%M:%S',
                            level=logging.INFO, 
                            force=True,
                            handlers=[logging.FileHandler("mutability.log", mode='w'), logging.StreamHandler()])
        logging.info(self.start_message)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.info(self.end_message)
        return True
    
    def __call__(self, *args, **kwargs):
        for test in self._tests:
            test_str = f"[TEST] {self._tests.index(test)+1:2d} / {len(self._tests):2d} {test['test_name']} :"
            if not isinstance(test["input"], self.__types):
                logging.i(f"{test_str} Type not supported")
                continue
            if not isinstance(test["expected"], bool):
                logging.info(f"{test_str} Expected value not supported")
                continue
            if not isinstance(test["test_name"], str):
                logging.info(f"{test_str} Test name not supported")
                continue
            try:
                assert is_mutable(test["input"]) is test["expected"]
            except Exception as e:
                logging.info(f"{test_str} failed {e}")
            else:
                logging.info(f"{test_str} succeeded")


def main():
    with MutabilityTest() as mutability_test:
        mutability_test._tests.append({"input": 1, "expected": True, "test_name": "Another Integer test"})
        mutability_test._tests.append({"input": 1.0, "expected": 1,    "test_name": "Another Float test"})
        mutability_test._tests.append({"input": "1", "expected": "1",  "test_name": "Another String test"})
        mutability_test._tests.append({"input": True, "expected": True, "test_name": True})
        mutability_test._tests.append({"input": np.array([1, 2, 3]), "expected": True, "test_name": "Numpy test"})
        mutability_test._tests.append({"input": pd.Series([1,2,3]), "expected": True, "test_name": "Pandas Series test"})
        mutability_test._tests.append({"input": pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]}), "expected": True, "test_name": "Pandas DataFrame test"})
        mutability_test()

# TODO
# add Numpy Array, Pandas Series, Pandas DataFrame support

if __name__ == "__main__":
    main()
