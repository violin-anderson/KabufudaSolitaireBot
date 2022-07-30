#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from copy import deepcopy
import time

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
STACKS = 8
STARTSPOTS = 1
MAXSPOTS = 4
UNIQUECARDS = 10
DUPES = 4

DEBUG = 0

class collapsed:
    def __init__(self, card):
        self.card = card
    
    def __hash__(self):
        return self.card.__hash__() * 37
    
    def __eq__(self, other):
        return isinstance(other, collapsed) and self.card == other.card
    
    def __str__(self):
        return str(DUPES) + 'x' + self.card

class stack:
    def __init__(self, cards):
        self.cards = cards
    
    def isCollapsed(self):
        return len(self.cards) == 1 and isinstance(self.cards[0], collapsed)
    
    def isEmpty(self):
        return self.cards == []

    def isSolved(self):
        return self.isCollapsed() or self.isEmpty()

    def getGroups(self):
        if self.isCollapsed() or self.isEmpty():
            return []
        lastCard = self.cards[-1]
        groups = [[lastCard]]
        for i in range(2, len(self.cards)+2):
            if i > len(self.cards) or self.cards[-i] != lastCard:
                return [[lastCard] * (i-1)]
        return groups

    def canFit(self, group):
        return not self.isCollapsed() and (self.isEmpty() or self.cards[-1] == group[0])
    
    def removeGroup(self, group):
        assert(not self.isCollapsed())
        assert(group[0] == self.cards[-1])
        assert(len(group) <= len(self.cards))
        assert(group[0] == self.cards[len(self.cards)-len(group)])
        self.cards = self.cards[:-len(group)]
    
    def addGroup(self, group):
        assert(not self.isCollapsed())
        assert(self.isEmpty() or group[0] == self.cards[-1])
        self.cards += group
        if len(self.cards) == DUPES and all([c == self.cards[0] for c in self.cards]):
            self.cards = [collapsed(self.cards[0])]
            return True
        return False
    
    def __hash__(self):
        return sum([self.cards[i].__hash__() for i in range(len(self.cards))])
    
    def __eq__(self, other):
        if not isinstance(other, stack):
            return False
        if self.isCollapsed() or other.isCollapsed():
            return self.isCollapsed() and other.isCollapsed() and self.cards[0].card == other.cards[0].card
        return len(other.cards) == len(self.cards) and all([other.cards[i] == self.cards[i] for i in range(len(self.cards))])
    
    def getCardsForString(self):
        if self.isCollapsed():
            return [str(DUPES), 'x', self.cards[0].card]
        if self.isEmpty():
            return ['E']
        return self.cards

class spot:
    def __init__(self):
        self.card = None
    
    def isCollapsed(self):
        return isinstance(self.card, collapsed)
    
    def isEmpty(self):
        return self.card is None

    def isSolved(self):
        return self.isCollapsed() or self.isEmpty()

    def getGroups(self):
        if self.isEmpty() or self.isCollapsed():
            return []
        return [[self.card]]
    
    def canFit(self, group):
        return self.isEmpty() and (len(group) == 1 or len(group) == DUPES)
    
    def removeGroup(self, group):
        assert(self.card == group[0])
        assert(len(group) == 1)
        self.card = None
    
    def addGroup(self, group):
        assert(self.isEmpty())
        assert(len(group) == 1 or len(group) == DUPES)
        if (len(group) == 1):
            self.card = group[0]
        else:
            self.card = collapsed(group[0])
        return False

    def __hash__(self):
        return self.card.__hash__()
    
    def __eq__(self, other):
        return isinstance(other, spot) and self.card == other.card
    
    def __repr__(self):
        return str(self.card)

class game:
    def __init__(self, cards):
        self.stacks = [stack(list(card)) for card in cards]
        self.spots = [spot() for _ in range(STARTSPOTS)]
        self.parent = None
        self.fromAction = None
        self.toAction = None
    
    def getChild(self):
        child = deepcopy(self)
        child.parent = self
        return child
    
    def __deepcopy__(self, memo):
        c = game([])
        c.stacks = deepcopy(self.stacks, memo)
        c.spots = deepcopy(self.spots, memo)
        return c
    
    def isSolved(self):
        return all([s.isSolved() or s.isEmpty() for s in self.stacks]) and all([s.isSolved() or s.isEmpty() for s in self.spots])
    
    def removeGroup(self, stack, group):
        for i, newstack in enumerate(self.stacks):
            if newstack == stack:
                newstack.removeGroup(group)
                self.fromAction = ('stack', i, len(stack.cards) - len(group))
                return
        
        for i, newstack in enumerate(self.spots):
            if newstack == stack:
                newstack.removeGroup(group)
                self.fromAction = ('spot', i)
                return
        
        assert(False)

    def addGroup(self, stack, group):
        for i, newstack in enumerate(self.stacks):
            if newstack == stack:
                newSpot = newstack.addGroup(group)
                if newSpot and len(self.spots) < MAXSPOTS:
                    self.spots.append(spot())
                self.toAction = ('stack', i, len(stack.cards))
                return
        
        for i, newstack in enumerate(self.spots):
            if newstack == stack:
                newSpot = newstack.addGroup(group)
                self.toAction = ('spot', i)
                return
        
        assert(False)
    
    def getMoves(self):
        newGames = []
        for stack in self.stacks + self.spots:
            for group in stack.getGroups():
                for stack2 in self.stacks + self.spots:
                    if stack != stack2 and stack2.canFit(group):
                        newGame = self.getChild()
                        newGame.removeGroup(stack, group)
                        newGame.addGroup(stack2, group)
                        newGames.append(newGame)
        return newGames
    
    def hasAncestor(self, newGame):
        return self == newGame or (not self.parent is None and self.parent.hasAncestor(newGame))
    
    def getDepth(self):
        if self.parent is None:
            return 1
        return 1 + self.parent.getDepth()

    def __hash__(self):
        return sum([i.__hash__() for i in self.stacks]) * 3 + sum([i.__hash__() for i in self.spots]) * 13
    
    def __eq__(self, other):
        return all([self.stacks.count(s) == other.stacks.count(s) for s in self.stacks]) and all([self.spots.count(s) == other.spots.count(s) for s in self.spots])
    
    def __str__(self):
        out = 'spots:\n'
        out += str(self.spots)
        out += '\nstacks:\n'
        stackLists = [s.getCardsForString() for s in self.stacks]
        for i in range(max([len(s) for s in stackLists])):
            for l in stackLists:
                if i < len(l):
                    out += l[i]
                else:
                    out += ' '
                out += ' '
            out += '\n'
        
        return out[:-1]

def verifyGame(gameList):
    assert(len(gameList) == STACKS)
    allList = list(''.join(gameList))
    unique = set(allList)
    assert(len(unique)) == UNIQUECARDS
    for c in unique:
        assert(allList.count(c) == DUPES)
        pass

def main():
    gl = [
        'ywtrd',
        'ot8xy',
        'txppr',
        'okxow',
        '8r8kd',
        'ypkyd',
        'dtwrk',
        '8wxpo'
    ]

    startTime = time.time()

    sln = solveGame(gl)

    endTime = time.time()
    print("\n\nFINAL SOLUTION:")
    slnString = str(sln)
    parent = sln.parent
    while parent is not None:
        slnString = str(parent) + '\n\n' + slnString
        parent = parent.parent
    print(slnString)
    print('Depth: ' + str(sln.getDepth()))
    print('Time: ' + str(endTime - startTime))

def solveGame(gl):
    verifyGame(gl)
    g = game(gl)

    stack = [g]
    found = {g}
    best = None
    startTime = time.time()

    while len(stack) > 0 and (time.time() - startTime < 0 or best is None):
        g = stack.pop()
        if DEBUG >= 2:
            print('\nStarting game board with parent:')
            print(g.parent)
            print('Current board:')
            print(g)

        if g.isSolved():
            print("Solution Found")
            print('Current Depth: ' + str(g.getDepth()) + ' Stack Length: ' + str(len(stack)))
            if best is None or g.getDepth() < best.getDepth():
                best = g
        
        moves = g.getMoves()
        for m in moves:
            if not m in found:
                found.add(m)
                stack.append(m)

        if DEBUG >= 1:
            print('Current Depth: ' + str(g.getDepth()) + ' Stack Length: ' + str(len(stack)))

    return best

if __name__ == '__main__':
    main()
