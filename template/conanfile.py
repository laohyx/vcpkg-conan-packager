import os
from conans import ConanFile, CMake, tools
from os import listdir
from os.path import isfile, join
from conans.tools import vcvars_command


class WrapperVcpkgConan(ConanFile):
    """
    - Runs with VS 14.
    - Full integrated with any other conan package
    - Generated libs declaredc, easy liked with CONAN_LIBS
    - Keeps different package for different compiler verions, archs and build_types
    - Binary storage in conan servers
    """
    name = "**NAME**"
    version = "**VERSION**"
    license = "MIT"
    url = "https://github.com/laohyx/vcpkg-conan-packager"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    short_paths = True

    def build(self):
        self.VCPKG_ROOT_FOLDER = os.getenv("VCPKG_ROOT_FOLDER")
        msg = "Cannot find vcpkg root folder: {}".format(str(self.VCPKG_ROOT_FOLDER))
        msg += "\n\nProbably you are trying to build some packages by your self.\n" \
               " Probably it is hard to build without configuring.\n" \
               " Please file an issue at https://github.com/laohyx/vcpkg-conan-packager"
        assert os.path.isdir(self.VCPKG_ROOT_FOLDER), msg
        VCPKG_EXE = os.path.join(self.VCPKG_ROOT_FOLDER, "vcpkg.exe")
        assert os.path.isfile(VCPKG_EXE), "Cannot find vcpkg.exe: {}".format(VCPKG_EXE)

        target = "{}:{}".format(self.name, self._get_triplet())
        self.run("vcpkg.exe remove {}".format(target), cwd=self.VCPKG_ROOT_FOLDER)
        self.run("vcpkg.exe build {}".format(target), cwd=self.VCPKG_ROOT_FOLDER)

    def _get_triplet(self):
        tmp = {"x86_64": "x64-windows",
               "x86": "x86-windows"}
        triplet = tmp[str(self.settings.arch)]
        if self.options.shared is False:
            triplet += "-static"
        return triplet

    def package(self):
        package_folder = os.path.join(self.VCPKG_ROOT_FOLDER, "/packages/%s_%s" % (self.name, self._get_triplet()))

        self.copy("*", src=package_folder + "/include", dst="include", keep_path=True)

        if self.settings.build_type == "Debug":
            package_folder += "/debug"

        # Artifacts from debug o root depending on build_type
        self.copy("*", src=package_folder + "/include", dst="include", keep_path=True)
        self.copy("*", src=package_folder + "/lib", dst="lib", keep_path=True)
        self.copy("*", src=package_folder + "/bin", dst="bin", keep_path=True)
        self.copy("*", src=package_folder + "/share", dst="share", keep_path=True)
        self.copy("*", src=package_folder + "/tools", dst="tools", keep_path=True)

    def package_info(self):
        libpath = os.path.join(self.package_folder, "lib")
        if os.path.exists(libpath):
            onlyfiles = [f for f in listdir(libpath) if isfile(join(libpath, f))]
            self.cpp_info.libs = [libname.split(".")[0] for libname in onlyfiles]
