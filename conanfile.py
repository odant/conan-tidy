# HTACG HTML Tidy Conan package
# Dmitriy Vetutnev, Odant 2020


from conans import ConanFile, CMake, tools


class ConanPackage(ConanFile):
    name = "tidy"
    version = "5.7.47+1"
    license = "https://raw.githubusercontent.com/htacg/tidy-html5/5.7.28/README/LICENSE.md"
    description = "libtidy is the library version of HTML Tidy. "
    url = "https://github.com/odant/conan-tidy"
    settings = {
        "os": ["Windows", "Linux"],
        "compiler": ["Visual Studio", "gcc"],
        "build_type": ["Debug", "Release"],
        "arch": ["x86", "x86_64", "mips", "armv7"]
    }
    options = {
        "fPIC": [True, False],
        "ninja": [True, False]
    }
    default_options = {
        "fPIC": True,
        "ninja": True
    }
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "rm_pkgconfig.patch", "rm_install_pdb.patch", "FindTidy.cmake"
    no_copy_source = True
    build_policy = "missing"

    def configure(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build_requirements(self):
        if self.options.ninja:
            self.build_requires("ninja/[>=1.9.0]")

    def source(self):
        tools.patch(patch_file="rm_pkgconfig.patch")
        tools.patch(patch_file="rm_install_pdb.patch")

    def build(self):
        cmake = CMake(self, msbuild_verbosity='normal')
        cmake.verbose = True
        cmake.definitions["BUILD_SHARED_LIB"] = "OFF"
        cmake.definitions["SUPPORT_CONSOLE_APP"] = "OFF"
        if self.settings.get_safe("compiler.runtime") in ("MT", "MTd"):
            cmake.definitions["USE_STATIC_RUNTIME"] = "ON"
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy("FindTidy.cmake", dst=".", keep_path=False)
        self.copy("*/tidy-static.pdb", dst="bin", keep_path=False)

    def package_id(self):
        self.info.options.ninja = "any"

    def package_info(self):
        # Libraries
        self.cpp_info.libs = tools.collect_libs(self)
        # Defines
        if self.settings.os == "Windows":
            self.cpp_info.defines.append("TIDY_STATIC")


