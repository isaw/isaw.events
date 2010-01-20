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
from persistent.list import PersistentList

class KSSTypewriterDemo(KSSView):

    def displayedKeys(self):
        keys = [
            [113, 119, 101, 114, 116, 122, 117, 105, 111, 112],
            [97, 115, 100, 102, 103, 104, 106, 107, 108],
            [121, 120, 99, 118, 98, 110, 109],
            [32]
        ]
        return keys
    
    def setCurrentLesson(self, title):
        text = self.getLessons()[title].strip()
        self.request.SESSION['typewriter'] = text
        self.getCommandSet('core').replaceInnerHTML('div#pattern', text)
        self.getCommandSet('core').setAttribute('input#field', 'value', '')
        self.getCommandSet('core').removeClass('input.lesson', 'active')
        self.getCommandSet('core').addClass('input#lesson_%s' % self.getLessonTitles().index(title), 'active')
        return self.render()


    def loadInitialPattern(self):
        lessonText = self.getLessons()[self.getLessonTitles()[0]]
        self.request.SESSION['typewriter'] = lessonText
        return lessonText



    def getLessons(self):
        lessons = {
            'Lesson 1'      : 'This is our first lesson at the SnowSprint',
            'Lesson 2'      : 'KSS is a generic javascript AJAX framework',
        }
        return lessons

    def getLessonTitles(self):
        titles = self.getLessons().keys()
        titles.sort()
        return titles

    
    def keydown(self, keycode):
        keycode = int(keycode)
        if keycode == 16:
            self.getCommandSet('core').addClass('div#key_16', 'active')
            for key in range(97, 97+26):
                self.getCommandSet('core').replaceInnerHTML('div#key_%s' % key, chr(key).upper())
        elif keycode in range(97, 97+26) + range(65, 65+26) + [32]:
            smallKeycode = keycode
            if keycode in range(65, 65+26):
                smallKeycode += 32
            self.getCommandSet('core').addClass('div#key_%s' % smallKeycode, 'active')
            currentText = self.request.SESSION['typewriter']
            if len(currentText)>0 and currentText[0]==chr(keycode):
                currentText = currentText[1:]
                self.request.SESSION['typewriter'] = currentText
                if len(currentText)==0:
                    currentText = 'please select another lesson'
                    self.getCommandSet('core').removeClass('input.lesson', 'active')
                self.getCommandSet('core').replaceInnerHTML('div#pattern', currentText.replace(' ', '&nbsp;'))
        return self.render()

    def keyup(self, keycode):
        keycode = int(keycode)
        if keycode == 16:
            for key in range(97, 97+26):
                self.getCommandSet('core').replaceInnerHTML('div#key_%s' % key, chr(key))
            self.getCommandSet('core').removeClass('div#key_16', 'active')
        elif keycode in range(97, 97+26) + range(65, 65+26) + [32]:
            smallKeycode = keycode
            if keycode in range(65, 65+26):
                smallKeycode += 32
            self.getCommandSet('core').removeClass('div#key_%s' % smallKeycode, 'active')
        return self.render()

    def mousedown(self, content):
        if content.strip()=='Shift':
            if self.request.SESSION.get('typewriter_shift', False):
                self.request.SESSION['typewriter_shift'] = False
                return self.keyup(16)
            else:
                self.request.SESSION['typewriter_shift'] = True
                return self.keydown(16)
        try:
            keycode = ord(content.strip())
        except:
            keycode = 32
        return self.keydown(keycode)

    def mouseup(self, content, fieldValue):
        if content.strip()=='Shift':
            return self.render()
        try:
            keycode = ord(content.strip())
        except:
            keycode = 32
            content = ' '
        if self.request.SESSION.get('typewriter_shift', False):
            self.keyup(16)
        if keycode in range(97, 97+26) + range(65, 65+26) + [32]:
            self.getCommandSet('core').setAttribute('input#field', 'value', fieldValue + content)
            self.getCommandSet('core').focus('input#field')
        return self.keyup(keycode)
