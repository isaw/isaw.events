# Copyright (c) 2005-2007
# Authors: KSS Project Contributors (see docs/CREDITS.txt)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from kss.core import KSSView, force_unicode, KSSExplicitError, kssaction
from time import time
from random import randint
from persistent.list import PersistentList

class KSSSnake(KSSView):

    MINTOP = 90
    MINLEFT = 90
    MAXTOP = 200
    MAXLEFT = 200
    SCORESTEP = 10

    FOODDIV = '<div class="food"></div>'
    LOSEDIV = '<div class="lose"><div class="gameover">GAME OVER</div>Click to play again.</div>'

    def initialize(self):
        self.removeFoodDiv()
        self.getCommandSet('core').deleteNode('div.lose')
        self.getCommandSet('core').removeClass('div.board', 'boardRed')
        self.request.SESSION['top'] = self.MINTOP
        self.request.SESSION['left'] = self.MINLEFT
        self.request.SESSION['dir'] = 'right'
        self.request.SESSION['score'] = 0
        # initialize snake
        self.getCommandSet('core').setStyle('div.snake', 'top', '%spx' % str(self.request.SESSION.get('top', self.MINTOP)))
        self.getCommandSet('core').setStyle('div.snake', 'left', '%spx' % str(self.request.SESSION.get('left', self.MINLEFT)))
        # initialize playground
        self.getCommandSet('core').setStyle('div.board', 'width', '%spx' % str(self.MAXLEFT))
        self.getCommandSet('core').setStyle('div.board', 'height', '%spx' % str(self.MAXTOP))
        # initialize food
        self.setFoodDiv()
        # set score
        self.getCommandSet('core').replaceInnerHTML('div.scoreField', '%s' % str(self.request.SESSION['score']))
        return self.render()

    def setFoodDiv(self):
        top_rand = randint(0, self.MAXTOP-11) 
        left_rand = randint(0, self.MAXLEFT-10) 
        top_offset = top_rand / 10 * 10
        left_offset = left_rand / 10 * 10
        self.getCommandSet('core').insertHTMLAsLastChild('div.board', self.FOODDIV)
        self.getCommandSet('core').setStyle('div.food', 'top', '%spx' % str(top_offset))
        self.getCommandSet('core').setStyle('div.food', 'left', '%spx' % str(left_offset))
        self.getCommandSet('core').setStyle('div.food', 'display', 'block')
        self.request.SESSION['food_top'] = top_offset
        self.request.SESSION['food_left'] = left_offset

    def removeFoodDiv(self):
        self.getCommandSet('core').deleteNode('div.food')
    
    def increaseScore(self):
        self.request.SESSION['score'] += self.SCORESTEP
        self.getCommandSet('core').replaceInnerHTML('div.scoreField', '%s' % str(self.request.SESSION['score']))

    def loseGame(self):
        self.removeFoodDiv()
        self.getCommandSet('core').addClass('div.board', 'boardRed')
        self.getCommandSet('core').insertHTMLAsLastChild('div.board', self.LOSEDIV)
        self.request.SESSION['dir'] = 'stop'

    def moveSnake(self):
        dir = self.request.SESSION.get('dir', 'stop')
        currentTop = self.request.SESSION.get('top', self.MINTOP)
        currentLeft = self.request.SESSION.get('left', self.MINLEFT)
        if dir == 'stop':
            return self.render()
        if dir == 'right':
            newLeft = currentLeft + 10
            if newLeft >= self.MAXLEFT:
                self.loseGame()
                return self.render()
            self.getCommandSet('core').setStyle('div.snake', 'left', '%spx' % str(newLeft))
            self.request.SESSION['left'] = newLeft
        if dir == 'left':
            newLeft = currentLeft - 10
            if newLeft < 0:
                self.loseGame()
                return self.render()
            self.getCommandSet('core').setStyle('div.snake', 'left', '%spx' % str(newLeft))
            self.request.SESSION['left'] = newLeft
        if dir == 'up':
            newTop = currentTop - 10
            if newTop < 0:
                self.loseGame()
                return self.render()
            self.getCommandSet('core').setStyle('div.snake', 'top', '%spx' % str(newTop))
            self.request.SESSION['top'] = newTop
        if dir == 'down':
            newTop = currentTop + 10
            if newTop >= self.MAXTOP:
                self.loseGame()
                return self.render()
            self.getCommandSet('core').setStyle('div.snake', 'top', '%spx' % str(newTop))
            self.request.SESSION['top'] = newTop
        # check collision
        self.checkCollision()
        return self.render()

    def checkCollision(self):
        if self.request.SESSION.get('top', 0) == self.request.SESSION.get('food_top', 0)+10 and \
           self.request.SESSION.get('left', 0) == self.request.SESSION.get('food_left', 1):
            self.removeFoodDiv()
            self.increaseScore()
            self.setFoodDiv()

    def changeDirection(self, keycode):
        keycode = int(keycode)
        if keycode not in [ord('w'), ord('a'), ord('d'), ord('s')] or self.request.SESSION.get('dir', '') == 'stop':
            return self.render()
        if keycode==ord('w'):
            self.request.SESSION['dir'] = 'up'
        if keycode==ord('a'):
            self.request.SESSION['dir'] = 'left'
        if keycode==ord('s'):
            self.request.SESSION['dir'] = 'down'
        if keycode==ord('d'):
            self.request.SESSION['dir'] = 'right'
        return self.render()

