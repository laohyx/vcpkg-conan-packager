from conans import ConanFile, CMake
import os


class VcpkgwrapperTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "**NAME**/**VERSION**@**USER**/**CHANNEL**"
    generators = "cmake"

    @property
    def port(self):
        return "**NAME**"

    @property
    def port_example(self):
        possibles = [os.path.join("port_examples", "%s.cpp" % self.port),
                     os.path.join("port_examples", "%s.c" % self.port), ]
        for filename in possibles:
            if os.path.exists(os.path.join(self.conanfile_directory, filename)):
                return filename.replace("\\", "\\\\")
        return None

    def build(self):
        cmake = CMake(self.settings)
        if self.port_example:
            self.run(
                'cmake "%s" %s -DTEST_FILENAME=%s' % (self.conanfile_directory, cmake.command_line, self.port_example))
            self.run("cmake --build . %s" % cmake.build_config)
        else:
            self.output.warn("NOT TEST PROGRAM PREPARED FOR PORT %s" % self.port)

    def imports(self):
        self.copy("*.dll", "bin", "bin")
        self.copy("*.dylib", "bin", "bin")

    def test(self):
        if self.port_example:
            os.chdir("bin")
            self.run(".%stest_exe.exe" % os.sep)
