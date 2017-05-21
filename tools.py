import os
import tempfile
import shutil
from init import *
from log import logger
from conans.client.runner import ConanRunner

def process_port(port, tmp_folder, visual_version, arch, build_type, is_link_dynamic):
    try:
        logger.info("Processing... %s:%s" % (port.source, port.version))
        tmp_folder = os.path.join(tmp_folder, port.name)     
        try:
            shutil.rmtree(tmp_folder)
        except Exception:
            pass   
        new_template_to(port.name, port.version, tmp_folder)
        runner = ConanRunner()
        command = 'conan test_package -s compiler="Visual Studio" ' \
                  '-s compiler.version=%s -s arch=%s -s build_type=%s -o %s:shared=%s' \
                  % (visual_version, arch, build_type, port.name, str(is_link_dynamic))
        logger.info(command)
        ret = runner(command, output=True, log_filepath=None, cwd=tmp_folder)
        return ret == 0
    except Exception as exc:
        logger.error("Error in processing %s: Error '%s'" % (port.name, str(exc)))
        return False

def temp_folder():
    return tempfile.mkdtemp(suffix='vcpkg_conanizer')

def replace_in_file(file_path, search, replace):
    with open(file_path, 'rt') as content_file:
        content = content_file.read()
        content = content.replace(search, replace)
    with open(file_path, 'wt') as handle:
        handle.write(content)


def new_template_to(name, version, dest_dir):
    shutil.copytree(os.path.abspath("./template"), dest_dir)

    for file_path in ("conanfile.py", "test_package/conanfile.py"):
        replace_in_file(os.path.join(dest_dir, file_path), "**NAME**", name)
        replace_in_file(os.path.join(dest_dir, file_path), "**VERSION**", version)
        replace_in_file(os.path.join(dest_dir, file_path), "**USER**", CONAN_USER)
        replace_in_file(os.path.join(dest_dir, file_path), "**CHANNEL**", CONAN_CHANNEL)
