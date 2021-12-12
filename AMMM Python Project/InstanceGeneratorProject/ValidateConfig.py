'''
AMMM P3 Instance Generator v2.0
Config attributes validator.
Copyright 2020 Luis Velasco

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from AMMMGlobals import AMMMException


class ValidateConfig(object):
    # Validate config attributes read from a DAT file.

    @staticmethod
    def validate(data):
        # Validate that mandatory input parameters were found
        paramList = ['V', 'E', 'W', 'F']
        for paramName in paramList:
            if paramName not in data.__dict__:
                raise AMMMException('Parameter(%s) has not been not specified in Configuration' % str(paramName))

        instancesDirectory = data.instancesDirectory
        if len(instancesDirectory) == 0: raise AMMMException('Value for instancesDirectory is empty')

        fileNamePrefix = data.fileNamePrefix
        if len(fileNamePrefix) == 0: raise AMMMException('Value for fileNamePrefix is empty')

        fileNameExtension = data.fileNameExtension
        if len(fileNameExtension) == 0: raise AMMMException('Value for fileNameExtension is empty')

        V = data.V
        if not isinstance(V, int) or (V <= 0):
            raise AMMMException('V(%s) has to be a positive integer value.' % str(V))

        E = data.E
        if not isinstance(E, int) or (E <= 0):
            raise AMMMException('E(%s) has to be a positive integer value.' % str(E))

        W = data.W
        if not isinstance(W, int) or (W <= 0):
            raise AMMMException('W(%s) has to be a positive integer value.' % str(W))

        F = data.F
        if not isinstance(F, int) or (F <= 0):
            raise AMMMException('F(%s) has to be a positive integer value.' % str(F))

        if E < (V-1):
            raise AMMMException('E(%s) has to be >= V-1(%s).' % (str(E), str(V-1)))

        if F < (W-1):
            raise AMMMException('F(%s) has to be >= W-1(%s).' % (str(F), str(W-1)))

        if E > (V*(V - 1)/2):
            raise AMMMException('E(%s) has to be <= (V(V - 1)/2)(%s).' % (str(E), str((V*(V - 1)/2))))

        if F > (W*(W - 1)/2):
            raise AMMMException('F(%s) has to be <= (V(V - 1)/2)(%s).' % (str(F), str((W*(W - 1)/2))))
