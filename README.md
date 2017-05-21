# Vcpkg Conan packager

This project is forked from [lasote/vcpkg](https://github.com/lasote/vcpkg). But different from lasote's, this packager
uses `vcpkg`'s own build script and upload all ports to `conan.io`.

For each port, the packager will build such triplets:

```
<port>:x86-windows
<port>:x86-windows-static
<port>:x64-windows
<port>:x64-windows-static
```

All of them have both release and debug build.


## How to build on your own

1. Configure environment variables:
```bash
set VCPKG_ROOT_FOLDER=D:\path\to\vcpkg
set CONAN_USER=laohyx
set CONAN_CHANNEL=vcpkg
set CONAN_PASSWORD=password
```
2. Optionally, you can specify what packages to build:

In `run.py`

```python
    to_upload, failed = process_ports(['boost', 'protobuf'])
    upload_packages(to_upload)
```


3. Run the script
`python run.py`