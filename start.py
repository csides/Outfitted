import numpy as np
import csv
import random
import warnings

warnings.simplefilter('ignore', np.RankWarning)

class TraitSpace:
    
    def __init__(self, names):
        self.names = names
        self.dim_num = len(names)

    def listOfTraits(self, v):
        out = []
        for i in range(len(v)):
            if v[i]:
                out.append(self.names[i])
        return out
    
    def index(self, trait):
        return self.names.index(trait)
    

class outfit:
    
    def __init__(self, tspace, name, values):
        if len(values) != tspace.dim_num:
            assert IndexError
        self.tspace = tspace
        self.values = np.array(values)
        self.name = name
    
    def stepwise_distance(self, other):
        if self.tspace != other.tspace:
            return np.nan
        return sum(self.values ^ other.values)
    
    def __str__(self):
        return self.name + ':' + str(self.values)

def getcolors(d):
    out = []
    if d['Color'] == '11':
        for num in [str(n) for n in range(1,10)]:
            try:
                if d['Color '+num] != '':
                    out.append('color'+d['Color '+num])
                    out.append('color'+d['Color '+num]+'-'+d['Shade '+num])
                    if num!='1':
                        out.append(num+'colors')
            except:
                pass
    else:
        out.append('color'+d['Color'])
        try:
            out.append('color'+d['Color']+'-'+d['Shade'])
        except KeyError:
            out.append('color'+d['Color']+'-'+d['Shade 1'])
    return out

def dict_to_traitlist(d):
    out = []
    out += getcolors(d)
    out.append('length'+d['Length'])
    out.append('style'+d['Style'])
    out.append('neckline'+d['Neckline'])
    out.append('back'+d['Back'])
    out.append('strap'+d['Strap'])
    if d['Print'] != '0' and d['Print'] != '8':
        out.append('print'+d['Print'])
    if d['Hemline'] == '1':
        out.append('hemline')
    if d['Pockets'] == '1':
        out.append('pockets')
    if d['Embroidery'] == '1':
        out.append('embroidery')
    if d['Sequins'] == '1':
        out.append('sequins')
    if d['Cut-outs'] == '1':
        out.append('cutouts')
    if d['metallic shine'] == '1':
        out.append('metallicshine')
    return out

def dict_to_vector(d, tspace):
    out = []
    traitlist = dict_to_traitlist(d)
    for trait in tspace.names:
        out.append(trait in traitlist)
    return out

def has_diff_vals(x):
    last = x[0]
    for i in range(1,len(x)):
        if x[i] != last:
            return True
        last = x[i]
    return False

def trait_importance(outfits, likes, trait):
    #outfits is list of outfits, likes is nparray of bools corresponding to outfits
    tspace = outfits[0].tspace
    tindex = tspace.index(trait)
    x = [int(o.values[tindex]) for o in outfits]
    if has_diff_vals(x):
        linreg = np.polyfit([int(o.values[tindex]) for o in outfits], likes, 1)
        return linreg[0]
    else:
        return np.nan

def score(trainingset, likes, outfit):
    trait_evaluations = [trait_importance(trainingset, likes, trait) for trait in outfit.tspace.names]
    out = 0.
    for i in range(len(outfit.values)):
        if np.isnan(trait_evaluations[i]):
            continue
        if outfit.values[i]:
            out += trait_evaluations[i]
        else:
            out -= trait_evaluations[i]
    return out / sum([abs(x) for x in trait_evaluations if not np.isnan(x)])

def get_tspace_and_outfits():
    with open('key.txt','rb') as f:
        key = f.read().split(', ')
    tspace = TraitSpace(key)
    
    dicts = []
    with open('Tagging1.csv','rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            #print row
            dicts.append(row)
    with open('tagging 2 (fedora).csv','rU') as f:
        reader = csv.DictReader(f)
        for row in reader:
            #print row
            dicts.append(row)
    
    outfits = []
    for d in dicts:
        outfits.append(outfit(tspace, d['URL'], dict_to_vector(d,tspace)))
    return tspace, outfits



