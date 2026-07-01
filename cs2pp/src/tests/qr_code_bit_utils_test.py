from utils.qr_code_bit_utils import get_bit, get_bits, append_bits 
def test_append_bits():
    bits = []
    append_bits(bits, 5, 3)  # 101
    assert bits == [1,0,1]
    append_bits(bits, 2, 3)  # 010
    assert bits == [1,0,1,0,1,0]

def test_get_bit():
    assert get_bit(5, 0) == True
    assert get_bit(5, 1) == False
    assert get_bit(5, 2) == True
    assert get_bit(5, 3) == False   

def test_get_bits():
    assert get_bits(5, 3) == [1,0,1]
    assert get_bits(2, 3) == [0,1,0]



