class State:
    def __init__(self):
        self.playfield = [[' ', ' ', ' '],
                          [' ', ' ', ' '],
                          [' ', ' ', ' ']]
        self.current_player = ' '

    def digest(self, message):
        if message['msg'] == 'new':
            for row in range(3):
                for col in range(3):
                    self.playfield[row][col] = ' '
            self.current_player = 'X'

        elif message['msg'] == 'set_mark':
            self.playfield[message['row']][message['col']] = self.current_player
            if self.current_player == 'X':
                self.current_player = 'O'
            else:
                self.current_player = 'X'

        elif message['msg'] == 'info':
            pass

        else:
            assert False, 'unknown message %r' % message['msg']

    def get_winner(self):
        for i in range(3):
            if ' ' != self.playfield[i][0] == self.playfield[i][1] == self.playfield[i][2]:
                return self.playfield[i][0]
            if ' ' != self.playfield[0][i] == self.playfield[1][i] == self.playfield[2][i]:
                return self.playfield[0][i]

        if ' ' != self.playfield[0][0] == self.playfield[1][1] == self.playfield[2][2]:
            return self.playfield[0][0]
        if ' ' != self.playfield[0][2] == self.playfield[1][1] == self.playfield[2][0]:
            return self.playfield[0][2]

        if not any(square == ' ' for row in self.playfield for square in row):
            return 'tie'


class Game:
    def __init__(self, playerX, playerO):
        self.state = State()
        self.players = {'X': playerX, 'O': playerO}

    def new_game(self):
        yield {'msg': 'new'}

    def turn(self):
        while True:
            answer = yield {'msg': 'ask', 'player': self.state.current_player}
            row = answer.get('row', None)
            col = answer.get('col', None)
            if row in (0, 1, 2) and col in (0, 1, 2):
                if self.state.playfield[row][col] == ' ':
                    break
        yield {'msg': 'set_mark', 'row': row, 'col': col}

    def game(self):
        yield from self.new_game()
        while True:
            yield from self.turn()
            winner = self.state.get_winner()
            if winner in ('X', 'O'):
                yield {'msg': 'info', 'text': '%s wins' % winner}
                break
            elif winner == 'tie':
                yield {'msg': 'info', 'text': 'game ends with a tie'}
                break

    def loop(self):
        while True:
            yield from self.game()

    def run(self):
        answer = None
        loop = iter(self.loop())
        while True:
            message = loop.send(answer)
            if message['msg'] == 'ask':
                answer = self.players[message['player']].digest(message)
            else:
                answer = None
                self.state.digest(message)
                for player in self.players.values():
                    player.digest(message)

class LocalPlayer:
    def __init__(self, token):
        self.token = token
        self.state = State()

    def digest(self, message):
        if message['msg'] == 'ask':
            print (' | '.join(self.state.playfield[0]))
            print ('--+---+--')
            print (' | '.join(self.state.playfield[1]))
            print ('--+---+--')
            print (' | '.join(self.state.playfield[2]))
            while True:
                row = input('%s, which row?' % self.token)
                col = input('%s, which column?' % self.token)
                try:
                    row = int(row)
                    col = int(col)
                except ValueError:
                    pass
                else:
                    return {'row': row, 'col': col}

        elif message['msg'] == 'info':
            print ('%s: %s' % (self.token, message['text']))

        else:
            self.state.digest(message)

if __name__ == '__main__':
    Game(LocalPlayer('X'), LocalPlayer('O')).run()
