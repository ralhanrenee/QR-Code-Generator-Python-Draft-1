from utils.qr_code_text_utils import is_numeric, is_alphanumeric, encode
def test_is_numeric():
    assert is_numeric("0123456789") == True
    assert is_numeric("123ABC") == False
    assert is_numeric("") == True     

def test_is_alphanumeric():
    assert is_alphanumeric("HELLO WORLD 123") == True
    assert is_alphanumeric("hello") == False
    assert is_alphanumeric("!@#") == False
    assert is_alphanumeric("") == True  

def test_encode():
    assert encode("0") == 0
    assert encode("9") == 9
    assert encode("A") == 10
    assert encode("Z") == 35
    assert encode("$") == 36
    assert encode("%") == 37
    assert encode("*") == 38
    assert encode("+") == 39
    assert encode("-") == 40
    assert encode(".") == 41
    assert encode("/") == 42
    assert encode(":") == 43
    assert encode("!") is None