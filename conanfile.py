# HTACG HTML Tidy Conan package
# Dmitriy Vetutnev, Odant 2020

from conan import ConanFile, tools
import os

class ConanPackage(ConanFile):
    name = "tidy"
    version = "5.8.0+0"
    license = "https://raw.githubusercontent.com/htacg/tidy-html5/5.7.28/README/LICENSE.md"
    description = "libtidy is the library version of HTML Tidy. "
    url = "https://github.com/odant/conan-tidy"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
        "ninja": [True, False]
    }
    default_options = {
        "fPIC": True,
        "ninja": True
    }
    exports_sources = "src/*", "rm_pkgconfig.patch", "rm_install_pdb.patch", "msvc_vsnprintf_macro.patch", "fix_cmake_version.patch"
    no_copy_source = True
    build_policy = "missing"
    package_type = "static-library"
    
    def layout(self):
        tools.cmake.cmake_layout(self, src_folder="src")

    def configure(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def build_requirements(self):
        if self.options.ninja:
            self.build_requires("ninja/[>=1.12.1]")

    def source(self):
        tools.files.patch(self, patch_file="rm_pkgconfig.patch")
        tools.files.patch(self, patch_file="rm_install_pdb.patch")
        tools.files.patch(self, patch_file="msvc_vsnprintf_macro.patch")
        tools.files.patch(self, patch_file="fix_cmake_version.patch")
        
    def generate(self):
        benv = tools.env.VirtualBuildEnv(self)
        benv.generate()
        if tools.microsoft.is_msvc(self):
            vc = tools.microsoft.VCVars(self)
            vc.generate()
        cmakeGenerator = "Ninja" if self.options.ninja else None
        tc = tools.cmake.CMakeToolchain(self, generator=cmakeGenerator)
        tc.variables["BUILD_SHARED_LIB"] = "OFF"
        tc.variables["SUPPORT_CONSOLE_APP"] = "OFF"
        if self.settings.get_safe("compiler.runtime") == "static":
            tc.variables["USE_STATIC_RUNTIME"] = "ON"
        tc.generate()

    def build(self):
        cmake = tools.cmake.CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = tools.cmake.CMake(self)
        cmake.install()
        tools.files.copy(self, "*/tidy*static*.pdb", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"), keep_path=False)

    def package_id(self):
        self.info.options.ninja = "any"

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Tidy")
        self.cpp_info.set_property("cmake_target_name", "Tidy::Tidy")
        # Libraries
        self.cpp_info.libs = tools.files.collect_libs(self)
        # Defines
        if self.settings.os == "Windows":
            self.cpp_info.defines.append("TIDY_STATIC")


