from abaqus import *
from abaqusConstants import *
from caeModules import *

def createForce(
kw_name=None,
kw_step=None,
kw_faces=None,
kw_fx=None,
kw_fy=None,
kw_fz=None,
kw_csys=None,
kw_amplitude=None,
kw_rotation=None,
kw_update=None):

##########################################################################################

	#print '\n*********************'
	#print kw_name, kw_step, kw_faces, kw_fx, kw_fy, kw_fz, kw_csys, kw_amplitude, kw_rotation, kw_update

##########################################################################################

	vps = session.viewports[session.currentViewportName]
	vpname = vps.name
	modelName = session.sessionState[session.currentViewportName]['modelName']
	
	ass = mdb.models[modelName].rootAssembly

##########################################################################################
	# check if step is valid
   
#	if len(mdb.models[modelName].steps) < 2:
#		print '\nError: No Step defined!'
#		getWarningReply(message='Can\'t use Initial step.\n\nCreate valid step!', buttons=(CANCEL,))
#		return

##########################################################################################

##########################################################################################
	# check if selection is valid
   
	if kw_faces == None:
		#print '\nError: Select face(s) and confirm selection before pressing Apply or OK'
		getWarningReply(message='No faces selected or confirmed!', buttons=(CANCEL,))
		return

##########################################################################################
	# check if values are valid
   
	if kw_fx == 0. and kw_fy == 0. and kw_fz == 0.:
		#print '\nError: All force components are zero!'
		getWarningReply(message='All force components are zero!', buttons=(CANCEL,))
		return

##########################################################################################
## Check existing names and define new one
	
	loadnames = mdb.models[modelName].loads.keys()
	
	if kw_name not in loadnames:
		lname = kw_name
	else:
		c = 2
		while c > 1:
			lname = kw_name+'-'+str(c)
			if lname not in loadnames:
				c = 0
			else:
				c = c + 1
	
##########################################################################################
## Region

	facetuple = kw_faces
	
	facetemp = ass.instances[facetuple[0].instanceName].faces[0:0]
	for x in facetuple:
		i = x.index
		j = x.instanceName
		facetemp = facetemp + ass.instances[j].faces[i:i+1]
	
	faceregion = regionToolset.Region(faces=facetemp,)

##########################################################################################
## Area

	massprop = ass.getMassProperties(regions=faceregion, relativeAccuracy=MEDIUM, miAboutCenterOfMass=False)
	farea = massprop['area']
	
	#print 'Area:', farea

##########################################################################################
## Calculate force

	fx = float(kw_fx)
	fy = float(kw_fy)
	fz = float(kw_fz)

	fres = sqrt(fx**2 + fy**2 + fz**2)
	strac = fres/farea

	#Normalizing force vector
	fxn = fx/fres
	fyn = fy/fres
	fzn = fz/fres
	
	#print 'forces: ', fx, fy, fz
	#print 'fres: ', fres
	#print 'direction: ',fxn, fyn, fzn
	#print 'traction: ', strac


##########################################################################################
## Amplitude

	if kw_amplitude == '(default)':
		famp = UNSET
	else:
		famp = kw_amplitude

##########################################################################################
## Follower

	if kw_rotation == True:
		follow = ON
	else:
		follow = OFF

##########################################################################################
## Resultant

	if kw_update == True:
		res = OFF
	else:
		res = ON

##########################################################################################
## for CSYS printing

	if kw_csys == None:
		pcsys = 'global'
	else:
		pcsys = 'local'

##########################################################################################
## Create Surface Traction
	
	fregion=regionToolset.Region(side1Faces=facetemp)
	
	mdb.models[modelName].SurfaceTraction(name=lname, createStepName=kw_step, 
		region=fregion, magnitude=strac, amplitude=famp, directionVector=((0.0, 0.0, 0.0), (fxn, 
		fyn, fzn)), distributionType=UNIFORM, field='', localCsys=kw_csys, 
		traction=GENERAL, follower=follow, resultant=res)
	
	print '\n'+80*'*'
	print 'Created a Surface Traction named: %s' % (lname)
	print 'Entered Forces: (%.4f, %.4f, %.4f) || F-Magnitude: %.4f || Area: %.4f || SurfTrac Mag: %f || Direction: (%.5f, %.5f,%.5f)' % (fx, fy, fz, fres, farea, strac, fxn, fyn, fzn)
	print 'Step: %s || Amplitude: %s || CSYS: %s' % (kw_step, kw_amplitude, pcsys)