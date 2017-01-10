# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-

import os
import snapcraft
from snapcraft.plugins import nodejs

class GruntPlugin(snapcraft.plugins.nodejs.NodePlugin):

    @classmethod
    def schema(cls):
        schema = super().schema()

        schema['properties']['gruntfile'] = {
            'type': 'string',
        }

        # Inform Snapcraft of the properties associated with building. If these
        # change in the YAML Snapcraft will consider the build step dirty.
        schema['build-properties'].append('gruntfile')

        return schema

    def build(self):
        super().build()
        if self.options.gruntfile:
            self.run(['npm', 'install', '-g', 'grunt-cli'])
            self.run([os.path.join(self.installdir, 'bin', 'grunt'), "--gruntfile", os.path.join(self.builddir, self.options.gruntfile)])
            # self.run([os.path.join(self.installdir, 'bin', 'grunt'), "--gruntfile", os.path.join(self.builddir, self.options.gruntfile), "install", "--install-dir", self.installdir])
        # Copy built min files
        self.run(["cp", "-r", os.path.join(self.builddir, "dist"), os.path.join(self.installdir, "lib/node_modules/min")])
        self.run(["cp", os.path.join(self.builddir, "main.build.js"), os.path.join(self.installdir, "lib/node_modules/min")])
