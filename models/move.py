class Move:
    def __init__(self, moveFrom, moveTo, removed, endGame, restartGame):
        self.moveFrom = moveFrom
        self.moveTo = moveTo
        self.removed = removed
        self.endGame = endGame
        self.restartGame = restartGame
    
    @classmethod
    def decode(self, json):
        moveFrom = json['moveFrom'] if 'moveFrom' in json else None
        moveTo =  json['moveTo'] if 'moveTo' in json else None
        removed = json['removed'] if 'removed' in json else None
        endGame = json['endGame'] if 'endGame' in json else None
        restartGame = json['restartGame'] if 'restartGame' in json else None
        return Move(moveFrom, moveTo, removed, endGame, restartGame)
    
    @classmethod
    def executeMove(self, original_move):
        new_move =  original_move
        return new_move