import sys, os
import pytest
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from compiler import Compiler

@pytest.fixture
def cmp():
    return Compiler()

def test_main(capsys, cmp):
    cmp.compileFile("example/main.lola")
    expected = '''66 69 72
B E H
d 102
108
-5'''
    
    captured = capsys.readouterr()
    assert captured.out == expected

def test_gugudan(capsys, cmp):
    cmp.compileFile("example/gugudan.lola")
    expected = '''4 * 1 = 4
4 * 2 = 8
4 * 3 = 12
4 * 4 = 16
4 * 5 = 20
4 * 6 = 24
4 * 7 = 28
4 * 8 = 32
4 * 9 = 36
'''
    captured = capsys.readouterr()
    assert captured.out == expected

def test_function(capsys, cmp):
    cmp.compileFile("example/function.lola")
    expected = '''150
1
2
3
4
'''
    captured = capsys.readouterr()
    assert captured.out == expected

def test_hello(capsys, cmp):
    cmp.compileFile("example/hello.lola")
    expected = '''Hello world\n'''
    captured = capsys.readouterr()
    assert captured.out == expected

def test_exception(capsys, cmp):
    cmp.compileFile("example/exception.lola")
    expected = '''4번째 적이 전장을 지배하고 있습니다!!\n'''
    captured = capsys.readouterr()
    assert captured.out == expected

def test_if(capsys, cmp):
    cmp.compileFile("example/if.lola")
    expected = '''4'''
    captured = capsys.readouterr()
    assert captured.out == expected

def test_while(capsys, cmp):
    cmp.compileFile("example/while.lola")
    expected = '''2345678910'''
    captured = capsys.readouterr()
    assert captured.out == expected