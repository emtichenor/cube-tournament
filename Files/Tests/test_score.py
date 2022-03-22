import pytest
from Files.Score import Score
def test_print_ao5_times():
    assert Score.print_ao5_times(['DNF' for _ in range(5)]) == "[(DNF), (DNF), DNF, DNF, DNF]"
    assert Score.print_ao5_times([30.0, 50.1, 42.3, 34.3, 35.3]) == "[(30.0), (50.1), 42.3, 34.3, 35.3]"
    assert Score.print_ao5_times(['DNF', 50.1, 42.3, 34.3, 35.3]) == "[(DNF), 50.1, 42.3, (34.3), 35.3]"
    isChanged = [30.0, 50.1, 42.3, 34.3, 35.3]
    Score.print_ao5_times(isChanged)
    assert isChanged == [30.0, 50.1, 42.3, 34.3, 35.3]