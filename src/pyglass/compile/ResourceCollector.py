# ResourceCollector.py
# (C)2013
# Scott Ernst

import sys
import os
import shutil
import py_compile
import requests.utils

from pyaid.ArgsUtils import ArgsUtils
from pyaid.OsUtils import OsUtils
from pyaid.debug.Logger import Logger
from pyaid.file.FileUtils import FileUtils
from pyaid.string.StringUtils import StringUtils

from pyglass.compile.WidgetUiCompiler import WidgetUiCompiler
from pyglass.app.PyGlassEnvironment import PyGlassEnvironment

#___________________________________________________________________________________________________ ResourceCollector
class ResourceCollector(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, compiler, **kwargs):
        """Creates a new instance of ResourceCollector."""
        self._log        = Logger(self)
        self._verbose    = ArgsUtils.get('verbose', False, kwargs)
        self._compiler   = compiler

        if OsUtils.isWindows():
            self._targetPath = self._compiler.getBinPath('resources', isDir=True)
        elif OsUtils.isMac():
            self._targetPath = self._compiler.getBinPath('resources', 'resources', isDir=True)

        if os.path.exists(self._targetPath):
            shutil.rmtree(self._targetPath)

        if not os.path.exists(self._targetPath):
            os.makedirs(self._targetPath)

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ run
    def run(self):
        """Doc..."""
        resources = self._compiler.resources

        #-------------------------------------------------------------------------------------------
        # APP RESOURCES
        #       If no resource folders were specified copy the entire contents of the resources
        #       folder. Make sure to skip the local resources path in the process.
        if not resources:
            for item in os.listdir(PyGlassEnvironment.getRootResourcePath(isDir=True)):
                itemPath = PyGlassEnvironment.getRootResourcePath(item)
                if os.path.isdir(itemPath) and not item == 'local':
                    resources.append(item)

        for container in resources:
            parts = container.replace('\\', '/').split('/')
            self._copyResourceFolder(
                PyGlassEnvironment.getRootResourcePath(*parts, isDir=True), parts
            )

        #-------------------------------------------------------------------------------------------
        # PYGLASS RESOURCES
        #       Copy the resources from the PyGlass
        resources = []
        for item in os.listdir(PyGlassEnvironment.getPyGlassResourcePath('..', isDir=True)):
            itemPath = PyGlassEnvironment.getPyGlassResourcePath('..', item)
            if os.path.isdir(itemPath):
                resources.append(item)

        for container in resources:
            self._copyResourceFolder(
                PyGlassEnvironment.getPyGlassResourcePath('..', container), [container]
            )

        #-------------------------------------------------------------------------------------------
        # CLEANUP
        if self._verbose:
            self._log.write('CLEANUP: Removing unwanted destination files.')
        self._cleanupFiles(self._targetPath)

        self._copyPythonStaticResources()

        if self._verbose:
            self._log.write('COMPLETE: Resource Collection')

        return True

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _copyResourceFolder
    def _copyResourceFolder(self, sourcePath, parts):
        targetPath = FileUtils.createPath(self._targetPath, *parts, isDir=True)
        WidgetUiCompiler(sourcePath).run()

        if self._verbose:
            self._log.write('COPYING: %s -> %s' % (sourcePath, targetPath))
        results = FileUtils.mergeCopy(sourcePath, targetPath)



#___________________________________________________________________________________________________ _copyPythonStaticResources
    def _copyPythonStaticResources(self):
        sourcePath = requests.utils.DEFAULT_CA_BUNDLE_PATH
        parts      = sourcePath[len(sys.exec_prefix):].strip(os.sep).split(os.sep)
        destPath   = FileUtils.createPath(self._targetPath, 'pythonRoot', *parts, isFile=True)
        folder     = os.path.dirname(destPath)
        if not os.path.exists(folder):
            os.makedirs(folder)
        shutil.copy(sourcePath, destPath)

#___________________________________________________________________________________________________ _compilePythonFiles
    def _compilePythonFiles(self, rootPath):
        os.path.walk(rootPath, self._compileInFolder, dict())

#___________________________________________________________________________________________________ _compileInFolder
    def _compileInFolder(self, arg, dirname, names):
        for name in names:
            if name.endswith('.py'):
                py_compile.compile(FileUtils.createPath(dirname, name, isFile=True))

#___________________________________________________________________________________________________ _cleanupFiles
    def _cleanupFiles(self, targetPath):
        os.path.walk(targetPath, self._cleanupInFolder, dict())

#___________________________________________________________________________________________________ _cleanupInFolder
    def _cleanupInFolder(self, arg, dirname, names):
        for name in names:
            if StringUtils.ends(name, self._compiler.ignoreExtensions):
                os.remove(FileUtils.createPath(dirname, name, isFile=True))

                # Deletes python (.py) files associated with ui files so only .pyc files remain.
                if name.endswith('.ui'):
                    pyName     = name.rsplit('.', 1)[0] + '.py'
                    pyNamePath = FileUtils.createPath(dirname, pyName, isFile=True)
                    if os.path.exists(pyNamePath):
                        os.remove(pyNamePath)

#===================================================================================================
#                                                                               I N T R I N S I C

#___________________________________________________________________________________________________ __repr__
    def __repr__(self):
        return self.__str__()

#___________________________________________________________________________________________________ __unicode__
    def __unicode__(self):
        return unicode(self.__str__())

#___________________________________________________________________________________________________ __str__
    def __str__(self):
        return '<%s>' % self.__class__.__name__


