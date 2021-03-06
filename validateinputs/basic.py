from validateinputs import registerplugin
from validateinputs import CheckStatus as status

"""
See README.md for details on the structure of classes here
"""


@registerplugin
class Check_max_level(): 
    name = "max_level"

    def check(self, app):
        max_level = app.inputvars['max_level'].getval()

        checkstatus                = {}   # Dict containing return status
        checkstatus['subname']     = ''   # Additional name info
        if max_level >= 0:
            checkstatus['result']  = status.PASS  
            checkstatus['mesg']    = 'max_level = %i >= 0'%max_level
        else:
            checkstatus['result']  = status.FAIL
            checkstatus['mesg']    = 'max_level = %i < 0'%max_level            
        return [checkstatus]              # Must be a list of dicts

@registerplugin
class Check_dt_cfl(): 
    name = "dt & CFL"

    def check(self, app):
        dt  = app.inputvars['fixed_dt'].getval()
        cfl = app.inputvars['cfl'].getval()

        checkstatus                = {}   # Dict containing return status
        checkstatus['subname']     = ''   # Additional name info
        if (dt<0.0) and (cfl<0.0):
            checkstatus['result']  = status.FAIL
            checkstatus['mesg']    = 'Both dt = %f<0 and cfl=%f < 0'%(dt, cfl)
        else:
            checkstatus['result']  = status.PASS  
            checkstatus['mesg']    = 'DT and CFL OK'
        return [checkstatus]              # Must be a list of dicts
