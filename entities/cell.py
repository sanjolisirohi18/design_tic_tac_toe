from enums.symbol import Symbol

class Cell:
    def __init__(self):
        self._symbol = Symbol.EMPTY
    
    @property
    def symbol(self) -> Symbol:
        return self._symbol
    
    def is_empty(self) -> bool:
        return self._symbol == Symbol.EMPTY
    
    @symbol.setter
    def symbol(self, value: Symbol):
        self._symbol = value