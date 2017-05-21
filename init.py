import os

VCPKG_ROOT_FOLDER = os.getenv("VCPKG_ROOT_FOLDER", os.path.abspath("vcpkg"))
VCPKG_PORTS_FOLDER = os.path.join(VCPKG_ROOT_FOLDER, "ports")
VCPKG_TRIPLETS_FOLDER = os.path.join(VCPKG_ROOT_FOLDER, "triplets")
VCPKG_GIT_FOLDER = os.path.join(VCPKG_ROOT_FOLDER, ".git")
folders = {
    "root": VCPKG_ROOT_FOLDER,
    "ports": VCPKG_PORTS_FOLDER,
    "triplets": VCPKG_TRIPLETS_FOLDER,
    "git": VCPKG_GIT_FOLDER,
}

for key, value in folders.iteritems():
    assert os.path.isdir(value), "Cannot find vcpkg {} folder: {}".format(key, value)

CONAN_USER = os.getenv("CONAN_USER", "laohyx")
CONAN_CHANNEL = os.getenv("CONAN_CHANNEL", "vcpkg")
