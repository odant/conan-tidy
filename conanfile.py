# HTACG HTML Tidy Conan package
# Dmitriy Vetutnev, Odant 2020


from conans import ConanFile, CMake, tools


class CityHashConan(ConanFile):
    name = "tidy"
    version = "5.7.28+0"
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
        "ninja": [True, False]
    }
    default_options = {
        "ninja": True
    }
    generators = "cmake"
    exports_sources = "src/*", "CMakeLists.txt", "rm_pkgconfig.patch", "FindTidy.cmake"
    no_copy_source = True
    build_policy = "missing"

    def build_requiments(self):
        if self.options.ninja:
            self.build_requires("ninja/1.9.0")

    def source(self):
        tools.patch(patch_file="rm_pkgconfig.patch")

    def build(self):
        build_type = "RelWithDebInfo" if self.settings.build_type == "Release" else "Debug"
        gen = "Ninja" if self.options.ninja == True else None
        cmake = CMake(self, build_type=build_type, generator=gen, msbuild_verbosity='normal')
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
        self.copy("*/tidys.pdb", dst="bin", keep_path=False)

    def package_id(self):
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

