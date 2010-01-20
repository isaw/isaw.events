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

class KSSDynamicTableDemo(KSSView):

    def getPersons(self):
        persons = self.request.SESSION.get('persons', PersistentList())
        if not persons or not isinstance(persons, PersistentList):
            persons = self.request.SESSION['persons'] = PersistentList()
        return persons

    def cleanPersons(self):
        self.request.SESSION['persons'] = PersistentList()
        self.getCommandSet('core').replaceHTML('table#personTable tbody', '<tbody></tbody>')
        return self.render()

    def addPerson(self, name, address, city, country, telephone):
        """ adds a person"""
        persons = self.getPersons()
        person = {
            'pid' : str(time()).replace('.',''),
            'name' : name,
            'address' : address,
            'city' : city,
            'country' : country,
            'telephone' : telephone
        }
        persons.append(person)
        html = self.renderPersonAsTr(person)
        self.getCommandSet('core').insertHTMLAsLastChild('table#personTable tbody', html)
        return self.render()
    

    def removePerson(self, pid):
        persons = self.getPersons()
        for p in persons:
            if p['pid'] == pid:
                persons.remove(p)
        self.getCommandSet('core').deleteNode('tr#pid%s' % pid)
        return self.render()


    def moveUp(self, pid):
        persons = self.getPersons()
        for i in range(1, len(persons)):
            pid1 = persons[i]['pid']
            pid2 = persons[i-1]['pid']
            if pid==pid1:
                self.switchPersons(pid1, pid2)
                break
        return self.render()

    def moveDown(self, pid):
        persons = self.getPersons()
        for i in range(0, len(persons)-1):
            pid1 = persons[i]['pid']
            pid2 = persons[i+1]['pid']
            if pid==pid1:
                self.switchPersons(pid1, pid2)
                break
        return self.render()

    def toTop(self, pid):
        persons = self.getPersons()
        firstPid = persons[0]['pid']
        if firstPid == pid:
            return self.render()
        self.getCommandSet('core').moveNodeBefore('tr#pid%s' % pid, 'pid%s' % firstPid)
        for p in persons:
            if p['pid'] == pid:
                persons.remove(p)
                persons.insert(0, p)
                break
        return self.render()

    def toBottom(self, pid):
        persons = self.getPersons()
        lastPid = persons[-1]['pid']
        if lastPid == pid:
            return self.render()
        self.getCommandSet('core').moveNodeAfter('tr#pid%s' % pid, 'pid%s' % lastPid)
        for p in persons:
            if p['pid'] == pid:
                persons.remove(p)
                persons.append(p)
                break
        return self.render()


    def switchPersons(self, pid1, pid2):
        persons = self.getPersons()
        p1 = None
        i1 = None
        p2 = None
        i2 = None
        for i in range(0, len(persons)):
            if persons[i]['pid'] == pid1:
                p1 = persons[i]
                i1 = i
            if persons[i]['pid'] == pid2:
                p2 = persons[i]
                i2 = i
        if p1 and p2:
            self.getCommandSet('core').replaceHTML('tr#pid%s' % p2['pid'], '<tr class="placeholder"></tr>')
            self.getCommandSet('core').replaceHTML('tr#pid%s' % p1['pid'], self.renderPersonAsTr(p2))
            self.getCommandSet('core').replaceHTML('tr.placeholder', self.renderPersonAsTr(p1))
            persons[i1] = p2
            persons[i2] = p1



    def renderPersonAsTr(self, person):
        pid = person['pid']
        buttons = '''
                    <input type="button" class="button remove kssattr-pid-%(pid)s" value="Remove">
                    <input type="button" class="button moveUp kssattr-pid-%(pid)s" value="Up">
                    <input type="button" class="button moveDown kssattr-pid-%(pid)s" value="Down">
                    <input type="button" class="button toTop kssattr-pid-%(pid)s" value="Top">
                    <input type="button" class="button toBottom kssattr-pid-%(pid)s" value="Bottom">
                ''' % {'pid' : pid}
        html = """<tr id="pid%(pid)s"><td>%(name)s</td><td>%(address)s</td><td>%(city)s</td><td>%(country)s</td><td>%(telephone)s</td><td>%(buttons)s</td></tr>""" % {
                'pid' : person['pid'],
                'name' : person['name'],
                'address' : person['address'],
                'city' : person['city'],
                'country' : person['country'],
                'telephone' : person['telephone'],
                'buttons' : buttons
        }
        return html


