#  _____         _    
# |_   _|___ ___| |___
#   | | / _ | _ \ (_-<
#   |_| \___|___/_/__/
#

import os.path
import hwwinfo

#---
def confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.
    
    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.
    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True
    """
    
    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s]|%s: ' % (prompt, 'y', 'n')
    else:
        prompt = '%s [%s]|%s: ' % (prompt, 'n', 'y')
        
    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print 'please enter y or n.'
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

#---
def filterSamples( samples, voc ):
    
    filtered = {}

    # convert the vocabulary, which is a mixture of strings and 2d tuples, into a dictionary
    fullvoc = dict([ e if isinstance(e,tuple) else (e,e) for e in voc])
    for proc,label in fullvoc.iteritems():
#         print proc,label

        if label not in samples: continue

        filtered[proc] = samples[label]

    return filtered


def getChain( sample, mass, path, tag='Data2011', tname='latino' ):
    import ROOT
    files = []
    try:
        all = hwwinfo.samples(mass, tag)
        files = all[sample]
    except Exception as e:
        print 'Exception',e
        return None

    chain = ROOT.TChain(tname)
    for f in files: chain.Add(os.path.join(path,f))
    
    return chain

    
#---
def loadOptDefaults(parser,pycfg=None,quiet=False):
    '''
    Load the default options from the configuation file.
    The new defaults options shall be written in python, as they are interpreted
    '''

    if not pycfg:
        import sys
        import re
        try:
            # pre-parse the python cfg location
            pyexp = re.compile('--pycfg(=)+')
            j = max([i for i,a in enumerate(sys.argv) if pyexp.match(a) ])
            dummy = [sys.argv[j]]
            try:
                dummy += [sys.argv[i+1]]
            except IndexError:
                pass

        except:
            dummy = []
        (opt,args) = parser.parse_args(dummy)

        pycfg = opt.pycfg 

    if os.path.exists(pycfg):
        handle = open(pycfg,'r')
        vars = {}
        exec(handle,vars)
        handle.close()


        for opt_name, opt_value in vars.iteritems():
            if opt_name[0] == '-': continue
            opt_longname = '--'+opt_name
            if not parser.has_option(opt_longname): continue

            o = parser.get_option(opt_longname)
            o.default = opt_value
            parser.defaults[opt_name] = opt_value

            if not quiet: print ' - new default value:',opt_name,'=',opt_value
        return


#---
class list_maker:
    def __init__(self, var ):
        self._var = var

    def __call__(self,option, opt_str, value, parser):
        if not hasattr(parser.values,self._var):
               setattr(parser.values,self._var,[])

        try:
           array = value.split(',')
           setattr(parser.values, self._var, array)

        except:
           print 'Malformed option (comma separated list expected):',value


# def make_cat_list(option, opt_str, value, parser):

#     if not hasattr(parser.values,'cats'):
#         setattr(parser.values,'cats',[])

#     try:
#         cats = value.split(',')
#         parser.values.cats = cats

#     except:
#         print 'Malformed option (comma separated list expected):',value


def addOptions(parser):
    parser.add_option('-l', '--lumi'     , dest='lumi'        , help='Luminosity'                            , default=None   , type='float'   )
    parser.add_option('-v', '--variable' , dest='variable'    , help='variable'                              , default=None )
    parser.add_option('-m', '--mass'     , dest='mass'        , help='run on one mass point only '           , default=0      , type='int'     )
    parser.add_option('-d', '--debug'    , dest='debug'       , help='Debug level'                           , default=0      , action='count' )
    parser.add_option('-c', '--chans'    , dest='chans'       , help='list of channels'                      , default=['0j'] , type='string' , action='callback' , callback=list_maker('chans'))
    parser.add_option('--pycfg'          , dest='pycfg'       , help='configuration file (default=%default)' , default='shape.py')

