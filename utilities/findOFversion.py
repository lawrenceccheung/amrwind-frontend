#!/usr/bin/env python
#
# Copyright (c) 2022, Alliance for Sustainable Energy
#
# This software is released under the BSD 3-clause license. See LICENSE file
# for more details.
#

# Get the location where this script is being run
import sys, os
scriptpath = os.path.dirname(os.path.realpath(__file__))
basepath   = os.path.dirname(scriptpath)

sys.path.insert(1, scriptpath)
sys.path.insert(1, basepath)
import OpenFASTutil as OpenFAST
import upgradeOFmodel
import argparse
from enum import Enum

# list of all allowed versions
allowedversions = [(2, 5),
                   (2, 6),
                   (3, 0),
                   (3, 1),
                   (3, 2),
                   (3, 3),
                   (3, 4),
               ]

def convertversiontoindex(vertuple):
    if vertuple in allowedversions:
        return allowedversions.index(vertuple)
    else:
        return -1

# The list of all version checks is kept and built here
verchecklist = []
def register_versioncheck(f):
    verchecklist.append(f)
    return f

def mergeMatchList(matchlist):
    result    = versionmatch.NOMATCH
    # Check the result
    if matchlist.count(versionmatch.MATCH) == len(matchlist): 
        result = versionmatch.MATCH
    return result

class versionmatch(Enum):
    """
    Define the different check outcomes
    """
    MATCH   = 1
    NOMATCH = 2
    UNKNOWN = 3

def checkIfVarsInFile(fstfile, subfile, varlistorig, 
                      flipbool=False, verbose=False, ignorecase=True):
    """
    Check to see if varlist is in subfile.  
    If subfile is empty string, check to see if varlist is in fstfile.
    """
    if subfile == '':
        probefile = fstfile
    else:
        probefile = OpenFAST.getFileFromFST(fstfile, subfile)
    filedictorig= OpenFAST.FASTfile2dict(probefile)
    if ignorecase:
        varlist = [x.lower() for x in varlistorig]
        filedict = {k.lower():v for k,v in filedictorig.items()}
    else:
        varlist = varlistorig
        filedict = filedictorig
    hasvar     = []
    for var in varlist:
        doesexist = True if var in filedict else False
        hasvar.append(doesexist)
    hasbool = 'contains'
    if flipbool: 
        hasvar = [not x for x in hasvar]
        hasbool = 'does not contain'
    if verbose:
        print(" Checking if "+probefile+" "+hasbool+":")
        for ivar, var in enumerate(varlist):
            print("  %s: %s"%(var, repr(hasvar[ivar])))
    matchresult = versionmatch.UNKNOWN
    # Check the result
    if hasvar.count(True) == len(varlist): matchresult = versionmatch.MATCH
    if hasvar.count(False)== len(varlist): matchresult = versionmatch.NOMATCH
    return matchresult, hasvar

# ==== ADD VERSION CHECK CLASSES HERE ====
# (FROM OLDEST TO NEWEST)

@register_versioncheck
class Check_2_5_0(): 
    name = "v2.5.0"
    version = { 'major':2, 'minor':5, 'patch':0 }

    def check(self, fstfile, verbose=False):
        checkvars = ['CompNTMD','NTMDfile','CompTTMD','TTMDfile']
        match1, l1 = checkIfVarsInFile(fstfile, 'ServoFile', checkvars,
                                       verbose=verbose)
        # Check TwrShadow is not an integer
        probefile = OpenFAST.getFileFromFST(fstfile, 'AeroFile')
        aerodict   = OpenFAST.FASTfile2dict(probefile)
        l2 = aerodict['TwrShadow'].strip().isdigit()
        match2 = versionmatch.NOMATCH if l2 else versionmatch.MATCH
        # Print TwrShadow check
        if verbose:
            print(" Checking if TwrShadow in %s is not an integer"%probefile)
            print("  TwrShadow=%s [%s]"%(aerodict['TwrShadow'],not l2))

        # Check version 2.4 stuff
        checkvars = ['CompAA','AA_InputFile','OLAFInputFileName']
        match3, l3 = checkIfVarsInFile(fstfile, 'AeroFile', checkvars,
                                       verbose=verbose)

        # Combine lists
        match = mergeMatchList([match1, match2, match3])
        l  = l1 + [l2] + l3
        return match, l

@register_versioncheck
class Check_2_6_0(): 
    name = "v2.6.0"
    version = { 'major':2, 'minor':6, 'patch':0 }

    def check(self, fstfile, verbose=False):
        checkvars = ['CompNTMD','NTMDfile','CompTTMD','TTMDfile']
        match1, l1 = checkIfVarsInFile(fstfile, 'ServoFile', checkvars,
                                       verbose=verbose)
        # Check TwrShadow is an integer
        probefile = OpenFAST.getFileFromFST(fstfile, 'AeroFile')
        aerodict   = OpenFAST.FASTfile2dict(probefile)
        l2 = aerodict['TwrShadow'].strip().isdigit()
        # Print TwrShadow check
        if verbose:
            print(" Checking if TwrShadow in %s is integer"%probefile)
            print("  TwrShadow=%s [%s]"%(aerodict['TwrShadow'],l2))
        match2 = versionmatch.MATCH if l2 else versionmatch.NOMATCH

        # Check TwrTI column
        AeroDynFile   = OpenFAST.getFileFromFST(fstfile, 'AeroFile')
        with open(AeroDynFile) as file:
            ADlines = [line.rstrip() for line in file]
        ADfirstword = [x.strip().split()[0].lower() for x in ADlines if len(x.strip().split())>0]
        linestart = ADfirstword.index('twrelev')+3
        NumTwrNds = int(OpenFAST.getVarFromFST(AeroDynFile, 'NumTwrNds'))
        linenums  = [linestart, linestart+NumTwrNds-1]
        nodelines = upgradeOFmodel.extractlines(AeroDynFile, linenums)
        match3    = versionmatch.MATCH
        l3        = True
        for line in nodelines:
            if (len(line.split()) != 4):
                match3 = versionmatch.NOMATCH
                l3     = False
                break
        if verbose:
            print(" Checking if TwrTI column exists in %s"%AeroDynFile)
            print("  TwrTI column: [%s]"%repr(l3))

        # Combine lists
        match = mergeMatchList([match1, match2, match3])
        l  = l1 + [l2] + [l3]
        return match, l

@register_versioncheck
class Check_3_0_0(): 
    name = "v3.0.0"
    version = { 'major':3, 'minor':0, 'patch':0 }

    def check(self, fstfile, verbose=False):
        checkvars = ['NumBStC', 'BStCfiles', 'NumNStC', 'NStCfiles', 
                     'NumTStC', 'TStCfiles', 'NumSStC', 'SStCfiles']
        match, l = checkIfVarsInFile(fstfile, 'ServoFile', checkvars,
                                     verbose=verbose)
        return match, l

@register_versioncheck
class Check_3_1_0(): 
    name = "v3.1.0"
    version = { 'major':3, 'minor':1, 'patch':0 }

    def check(self, fstfile, verbose=False):
        checkvars = ['NumBStC', 'BStCfiles', 'NumNStC', 'NStCfiles', 
                     'NumTStC', 'TStCfiles', 'NumSStC', 'SStCfiles',
                     'AfCmode', 'AfC_Mean',  'AfC_Amp', 'AfC_Phase',
                     'CCmode']
        match1, l1 = checkIfVarsInFile(fstfile, 'ServoFile', checkvars,
                                       verbose=verbose)
        checkvars = ['MHK', 'Gravity', 'AirDens', 'WtrDens', 'KinVisc', 
                     'SpdSound',  'Patm', 'Pvap', 'WtrDpth', 'MSL2SWL']
        match2, l2 = checkIfVarsInFile(fstfile, '', checkvars, verbose=verbose)
        match3, l3 = checkIfVarsInFile(fstfile, 'AeroFile', ['FluidDepth'], 
                                       flipbool=True, verbose=verbose)
        match4, l4 = checkIfVarsInFile(fstfile, 'EDFile', ['Gravity'], 
                                       flipbool=True, verbose=verbose)

        # Combine the lists
        l         = l1 + l2 + l3 + l4
        result    = mergeMatchList([match1, match2, match3, match4])
        return result, l

@register_versioncheck
class Check_3_2_0(): 
    name = "v3.2.0"
    version = { 'major':3, 'minor':2, 'patch':0 }

    def check(self, fstfile, verbose=False):
        l = []
        return versionmatch.UNKNOWN, l


@register_versioncheck
class Check_3_3_0(): 
    name = "v3.3.0"
    version = { 'major':3, 'minor':3, 'patch':0 }

    def check(self, fstfile, verbose=False):
        l = []
        return versionmatch.UNKNOWN, l

@register_versioncheck
class Check_3_4_0(): 
    name = "v3.4.0"
    version = { 'major':3, 'minor':4, 'patch':0 }

    def check(self, fstfile, verbose=False):
        checkADvars = ['Buoyancy', 'VolHub', 'HubCenBx', 'VolNac', 'NacCenB', 
                       'TFinAero', 'TFinFile']
        match1, l1 = checkIfVarsInFile(fstfile, 'AeroFile', checkADvars, 
                                       verbose=verbose)

        l         = l1
        result    = mergeMatchList([match1])
        return result, l


# ========================================================================
def findversion(filename, verbosity=0):
    checkverbose = True if verbosity>=2 else False
    # Run checks in reverse order
    for f in verchecklist[::-1]:
        match, l = f().check(filename, verbose=checkverbose)
        if verbosity>0: print("Done checking: "+f().name+" "+match.name)
        if match == versionmatch.MATCH: 
            return f().version, match
    # no match found, return empty
    return {}, versionmatch.NOMATCH

# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":
    helpstring = """Check to see what version an OpenFAST model is
    """

    # Handle arguments
    parser     = argparse.ArgumentParser(description=helpstring)
    parser.add_argument(
        "fstfile",
        help="OpenFAST fst file",
        type=str,
    )
    parser.add_argument('-v', '--verbose', 
                        action='count', 
                        help="Verbosity level (multiple levels allowed)",
                        default=0)

    # Load the options
    args      = parser.parse_args()
    filename  = args.fstfile
    verbose   = args.verbose

    verinfo, match = findversion(filename, verbosity=verbose)
    print(verinfo, match.name)
