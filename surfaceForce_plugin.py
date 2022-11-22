from abaqusGui import getAFXApp, Activator, AFXMode
from abaqusConstants import ALL
import os
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
    buttonText='Tools ME|Surface Force', 
    object=Activator(os.path.join(thisDir, 'surfaceForceDB.py')),
    kernelInitString='import createTracForce_kernel',
    messageId=AFXMode.ID_ACTIVATE,
    icon=None,
    applicableModules=['Load'],
    version='1.0',
    author='Matthias Ernst',
    description='Plug-In to apply general force to face region. Supports only face geometry!'\
                 '\nMake sure to confirm face selection (one or multiple faces) with DONE button or middle mouse button. '\
                 '\nAlso check if the chosen step and the other data are correct. '\
                 '\nThe Plug-In calculates the face area and creates a Surface Traction load. See control output in Message Area. '\
                 '\nDelete or edit the Surface Traction if needed. The Load Manager also allows to move the load to another step.'\
                 '\n\nUsage at your own risk.',
    helpUrl='N/A'
)
