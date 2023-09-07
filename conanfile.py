from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout, CMakeDeps
from conan.tools.files import collect_libs, copy
from conan.tools.env import Environment
from conan.tools import CppInfo
from conan.tools.env import VirtualRunEnv
import os

class TraactPackageCmake(object):
    """
    Base class for all traact libraries
    """        

    def traact_env_items(self):
        lib_paths = []
        for require, dependency in self.dependencies.items():
            dep = dependency.ref.name
            if dep.startswith('traact') and (not dep.startswith('traact_core') and not dep.startswith('traact_base')):
                if self.settings.os == "Windows":
                    lib_paths.extend(dependency.cpp_info.bindirs)
                else:
                    lib_paths.extend(dependency.cpp_info.libdirs)

        return lib_paths

    def is_editable(self):
        return self.plugin_build_folder.startswith(self.package_folder)

    def layout(self):        
        cmake_layout(self)

    def generate(self):        

        tc = CMakeToolchain(self)

        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            tc.variables[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)
        self._configure_toolchain(tc)
        tc.generate()
        deps = CMakeDeps(self)
        self._configure_cmakedeps(deps)
        deps.generate()        
        
        runenv = VirtualRunEnv(self)
        runenv.generate()  

        self.plugin_build_folder = self.build_folder            

        self._extend_generate()            

    def build(self):
        cmake = CMake(self)
        self._before_configure()
        cmake.configure()
        self._before_build(cmake)
        cmake.build()
        self._after_build()        

    def package(self):
        cmake = CMake(self)
        self._before_package(cmake)
        cmake.install()
        self._after_package()

    def package_info(self):
        self.cpp_info.libs = collect_libs(self)
        # add lib/bin folder to plugin env variable, try to detect if the package is in editable mode
        if self.name.startswith('traact') and (not self.name.startswith('traact_core') and not self.name.startswith('traact_base')):
            if self.is_editable():
                self.runenv_info.append_path("TRAACT_PLUGIN_PATHS", self.plugin_build_folder)
            else:
                if self.settings.os == "Windows":
                    self.runenv_info.append_path("TRAACT_PLUGIN_PATHS", os.path.join(self.package_folder, self.cpp_info.bindir))                
                else:
                    self.runenv_info.append_path("TRAACT_PLUGIN_PATHS", os.path.join(self.package_folder, self.cpp_info.libdir))
                
            
        self._after_package_info()

    def _configure_toolchain(self, tc):
        pass

    def _configure_cmakedeps(self, deps):
        pass

    def _extend_generate(self):
        pass

    def _before_configure(self):
        pass

    def _before_build(self, cmake):
        pass

    def _after_build(self):
        pass

    def _before_package(self, cmake):
        pass

    def _after_package(self):
        pass

    def _after_package_info(self):
        pass


class TraactGeneratorPackage(ConanFile):
    name = "traact_base"
    version = "0.0.0"
    url = "https://github.com/traact/traact_base.git"
    license = "MIT"
    description = "conan base for traact libraries with some utils for conan and cmake setup"
    
    no_copy_source = True    
    exports_sources = "include/*"

    def build(self):
        pass

    def package(self):
        copy(self, "*.cmake", src=self.source_folder, dst=self.package_folder)

    def package_info(self):
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
    