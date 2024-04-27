from ANET import ANET
from game_nim import GameNim
from MCT import mct
import numpy as np
from agent_human import AgentHuman
import torch
import os
class rl_system:
    #def __init__(self, net:ANET, tree: mct, game: GameNim) -> None:
    def __init__(self, game: GameNim) -> None:
        self.net = None
        self.tree = None
        self.game = game
        self.state = None
        pass

    def train(self, saveI, number_games, number_sim, eps):
        #RBUF = np.array([]) #this is sketchy, just use list?
        RBUF = []
        self.net= ANET(numInput=2, numOutput=2)
        for game in range(number_games):
            print(f'its in new game {game}')
            #RBUF = []
            self.game.reset(gameVariables=[2,2])
            self.state=[0,0]
            self.state[0], self.state[1] = self.game.getBoardState()
            print(f"s_init: {self.state}")
            self.tree = mct(state=self.state, game = self.game, network=self.net)
            #print(f"eps: {eps/(game+1)}")
            #print(f"tree root before while: {self.tree.root.boardState}")
            while self.game.isFinalState(self.state[0], self.state[1]) == None: #Trenge ikke ta inn parametre
                #print('ITS IN WHILE')
                for sim in range(number_sim):
                    self.tree.sim(eps=eps/(game+1))
                    #print(eps/(sim+1))
                #print(f'sim is done for {game}')
                D = self.tree.distribution()
                #print(f'Distribution : {D}')
                #print(f"RBUF: {RBUF}")
                RBUF.append([[self.tree.root.boardState[0], self.tree.root.player], D])
                action = np.argmax(D)
                #print(f"IT GETS HERE")
                #self.tree.print_tree(self.tree.root)
                #print(action)
                self.state = self.game.actionOnState(action, self.state[0], self.state[1])
                self.tree.root = self.tree.root.children[action] #not here
                #break
            print(f"RBUF: {RBUF}")
            self.net.train(RBUF)
            #RBUF=[]
            if game % saveI == 0:
                #save ANET for tournament play
                torch.save(self.net, f"code/networks/network_{game}")
                pass
        with open('output.txt', 'w') as file:
            # Iterate over the list and write each element to the file
            for item in RBUF:
                file.write(f"{item}" + '\n') 
       # print(f"data: {RBUF}")
        return self.net

def playGame(game: GameNim, network: ANET, verbose=True):
        agent = AgentHuman(2)
        while game.PlayerHasWon() == 0:
            if verbose:
                game.printGameState()
            moves = game.getMoves()
            state=[0,0]
            state[0], state[1] = game.getBoardState()
            if game.playerTurn == 1:
                netState= [state[0][0], 1]
                #print(f"state: {network.forward(netState, moves=moves)}")
                action = torch.argmax(network.forward(netState))
                game.update(moves[action], verbose=verbose)
            else:
                move = agent.makeMove(game, moves)
                game.update(move, verbose=verbose)
        if verbose:
            print(f"Player {game.PlayerHasWon()} won!")
        return game.PlayerHasWon()

def playGamesAI(numberGames: int, player1: ANET, player2: ANET, verbose=True):
        wincount = [0,0]
        for i in range(numberGames):
            game = GameNim(gameVariables=[5,2])
            if i % 2 == 0:
                while game.PlayerHasWon() == 0:
                    if verbose:
                        game.printGameState()
                    moves = game.getMoves()
                    state=[0,0]
                    state[0], state[1] = game.getBoardState()
                    if game.playerTurn == 1:
                        netState= [state[0][0], 1]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player1.forward(netState))
                        game.update(moves[action], verbose=verbose)
                    else:
                        netState= [state[0][0], 2]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player2.forward(netState))
                        game.update(moves[action], verbose=verbose)
                if verbose:
                    print(f"Player {game.PlayerHasWon()} won!")
                wincount[game.PlayerHasWon()-1]+=1
            else:
                while game.PlayerHasWon() == 0:
                    if verbose:
                        game.printGameState()
                    moves = game.getMoves()
                    state=[0,0]
                    state[0], state[1] = game.getBoardState()
                    if game.playerTurn == 1:
                        netState= [state[0][0], 1]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player2.forward(netState))
                        game.update(moves[action], verbose=verbose)
                    else:
                        netState= [state[0][0], 2]
                        #print(f"state: {network.forward(netState, moves=moves)}")
                        action = torch.argmax(player1.forward(netState))
                        game.update(moves[action], verbose=verbose)
                if verbose:
                    print(f"Player {game.PlayerHasWon()} won!")
                if game.PlayerHasWon() ==1:
                    wincount[1]+=1
                else:
                    wincount[0]+=1
        return wincount

def testNetworks():
    #test all networks against eachother, tournament code 
    pass
    
def main():
    print("RUN BEGINS")
    """networks_dir = os.path.join(os.path.dirname(__file__), 'networks')
    print(networks_dir)"""
    
    game = GameNim(gameVariables=[5,2])
    system = rl_system(game)
    net = system.train(saveI=5, number_games=11, number_sim=3, eps=1)
    #net.plot()
    #testgame = GameNim(gameVariables=[5,2])
    #winner = playGame(testgame, net)
    
    playerN = ANET()
    print(playerN.simpleForward([2, 1]))
    
    player0 = ANET()
    player0 = torch.load('code/networks/network_0')
    print(f'code/networks/network_0 {player0.simpleForward([2, 1])}')

    player5 = ANET()
    player5 = torch.load('code/networks/network_5')
    print(f'code/networks/network_5 {player5.simpleForward([2, 1])}')

    player200 = ANET()
    player200 = torch.load('code/networks/network_200')
    print(f'code/networks/network_200 {player200.simpleForward([2, 1])}')
    # winner = playGamesAI(1000, player1=player1, player2=player2, verbose=True)
    # print(winner)
    



main()