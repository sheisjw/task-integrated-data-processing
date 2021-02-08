import sys
import pytest

sys.path.append('shared_functions')
from preprocess import read_file


TEST_FILE_PATH = 'research_notebooks/flair_model/test.tsv'


@pytest.mark.parametrize("path, is_test, expect_output",
                         [(TEST_FILE_PATH, True, ['limit', 'O', 'O']),
                          (TEST_FILE_PATH, False, ['limit', 'O'])])
def test_read_file(path, is_test, expect_output):
    output = read_file(path, is_test)
    assert expect_output == output[0][0]
