'''
Created on Apr 5, 2018

@author: gasilos
'''

import glob
import os

class WalkCTdirs():
    '''
    Walks in the directory structure and creats list of paths to CT folders
    Determines flats before/after
    and checks that foltders contain only tiff files 
    '''

    def __init__(self, inpath, fol, verb = True):
        self.lvl0 = os.path.abspath(inpath)
        self.ctdirs = []
        self.types = []
        self.ctsets = []
        self.typ = []
        self.total = 0 
        self.good = 0
        self.verb = verb
        self._fol = fol
    
    def print_tree(self):
        print 'We start in {}'.format(self.lvl0) 
        
    def findCTdirs(self):
        for root, dirs, files in os.walk(self.lvl0):
            for name in dirs:
                if name == self._fol[2]:
                    self.ctdirs.append(root)
        self.ctdirs = list(set(self.ctdirs))
        
        
    def checkCTdirs(self):
        for ctdir in self.ctdirs:
            if ( os.path.exists(os.path.join(ctdir, self._fol[1])) \
                     and os.path.exists(os.path.join(ctdir, self._fol[0])) \
                     and (not os.path.exists(os.path.join(ctdir, self._fol[3])) \
                            or self._fol[1]==self._fol[3]) ):
                self.typ.append(3)
            elif ( os.path.exists(os.path.join(ctdir, self._fol[1])) \
                     and os.path.exists(os.path.join(ctdir, self._fol[0])) \
                     and os.path.exists(os.path.join(ctdir, self._fol[3])) ):
                self.typ.append(4)
            else:
                print os.path.basename(ctdir)
                self.typ.append(0)
    
    def checkCTfiles(self):
        for i, ctdir in enumerate(self.ctdirs):
            if ( self.typ[i] == 3 and \
                    self._checkTifs(os.path.join(ctdir, self._fol[1])) and \
                    self._checkTifs(os.path.join(ctdir, self._fol[0])) and \
                    self._checkTifs(os.path.join(ctdir, self._fol[2])) ):
                continue
            elif  ( self.typ[i] == 4 and \
                    self._checkTifs(os.path.join(ctdir, self._fol[1])) and \
                    self._checkTifs(os.path.join(ctdir, self._fol[0])) and \
                    self._checkTifs(os.path.join(ctdir, self._fol[2]))and \
                    self._checkTifs(os.path.join(ctdir, self._fol[3])) ):
                continue
            else: 
                self.typ[i] = 0
    
    def _checkTifs(self, tmpath):
        for i in os.listdir(tmpath):
            if os.path.isdir(i):
                return 0
            if i.split('.')[-1] != 'tif':
                return 0
        return 1
            
    def SortBadGoodSets(self):
        #reduces typ of all directories to either
        #good with flats 2 (1) or good without flats2 (0) or bad (<0)
        self.total = len(self.ctdirs)
        self.ctsets = sorted(zip(self.ctdirs, self.typ), key=lambda s:s[0])
        self.total = len(self.ctsets)
        self.good = [int(y)>2 for x,y in self.ctsets].count(True)

        tmp = len(self.lvl0)
        if self.verb:
            print 'Total folders {}, good folders {}'.format(self.total, self.good)
            print '{:>20}\t{}'.format("Path to CT set", "Typ: 0 bad, 3 no flats2, 4 with flats2")
            for ctdir in self.ctsets:
                msg1=ctdir[0][tmp:]
                print '{:>20}\t{}'.format(msg1, ctdir[1])

        #keep pathes to directories with good ct data only:
        self.ctsets = [q for q in self.ctsets if int(q[1]>0)]
    
    def Getlvl0(self):
        return self.lvl0
    
    
        
            
            
            
            
            
