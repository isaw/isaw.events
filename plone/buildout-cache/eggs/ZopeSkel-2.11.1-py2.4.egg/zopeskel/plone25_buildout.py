import copy
from zopeskel.plone3_buildout import Plone3Buildout
from zopeskel.base import get_var

class Plone25Buildout(Plone3Buildout):
    _template_dir = 'templates/plone2.5_buildout'
    summary = "A buildout for Plone 2.5 projects"
    required_templates = ['plone3_buildout']

    vars = copy.deepcopy(Plone3Buildout.vars)
    get_var(vars, 'plone_version').default = "2.5.5"
