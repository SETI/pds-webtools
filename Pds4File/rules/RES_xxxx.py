####################################################################################################################################
# rules/RES_xxxx.py
####################################################################################################################################

import pdsfile
import translator
import re

####################################################################################################################################
# Subclass definition
####################################################################################################################################

class RES_xxxx(pdsfile.PdsFile):

    pdsfile.PdsFile.VOLSET_TRANSLATOR = translator.TranslatorByRegex([('RES_xxxx', re.I, 'RES_xxxx')]) + \
                                        pdsfile.PdsFile.VOLSET_TRANSLATOR

####################################################################################################################################
# Update the global dictionary of subclasses
####################################################################################################################################

pdsfile.PdsFile.SUBCLASSES['RES_xxxx'] = RES_xxxx

####################################################################################################################################