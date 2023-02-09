import pytest
import ipytest
from main import take_input
ipytest.autoconfig()

#@pytest.mark.parametrize("day_time", ['tuesday, 10 am'])
def test_input1():
    result = take_input('tuesday, 10 am')
    assert sorted(result) == sorted([5, 38, 41, 49, 18, 19]), "Test Failed"

#@pytest.mark.parametrize("day_time", ['monday, 5:30 pm'])
def test_input2():
    result = take_input('monday, 5:30 pm')
    assert sorted(result) == sorted([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51]), "Test Failed"

#@pytest.mark.parametrize("day_time", ['friday, 7:30 am'])
def test_input3():
    result = take_input('friday, 7:30 am')
    assert result == 'No Restaurants Open on the given day and time', "Test Failed, there is no open restaurant in the data at the given time"
    
#@pytest.mark.parametrize("day_time", ['sunday, 1:30 am'])
def test_input4():
    result = take_input('sunday, 1:30 am')
    assert sorted(result) == sorted([25, 28]), "Test Failed"