# FindTidy.cmake for Conan cityhash package
# Dmitriy Vetutnev, Odant, 2020


# Find include path
find_path(Tidy_INCLUDE_DIR
    NAMES tidy.h
    PATHS ${CONAN_INCLUDE_DIRS_TIDY}
    NO_DEFAULT_PATH
)

# Find library
find_library(Tidy_LIBRARY
    NAMES tidy tidy_static tidy_staticd tidys tidysd
    PATHS ${CONAN_LIB_DIRS_TIDY}
    NO_DEFAULT_PATH
)

# Set version
set(Tidy_VERSION_MAJOR 5)
set(Tidy_VERSION_MINOR 8)
set(Tidy_VERSION_PATCH 0)
set(Tidy_VERSION_STRING "${Tidy_VERSION_MAJOR}.${Tidy_VERSION_MINOR}.${Tidy_VERSION_PATCH}")
set(Tidy_VERSION ${Tidy_VERSION_STRING})

# Check variables
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Tidy
    REQUIRED_VARS Tidy_INCLUDE_DIR Tidy_LIBRARY
    VERSION_VAR Tidy_VERSION
)

# Add imported target
if(Tidy_FOUND AND NOT TARGET Tidy::Tidy)
    add_library(Tidy::Tidy UNKNOWN IMPORTED)
    set_target_properties(Tidy::Tidy PROPERTIES
        IMPORTED_LOCATION ${Tidy_LIBRARY}
        INTERFACE_INCLUDE_DIRECTORIES ${Tidy_INCLUDE_DIR}
        INTERFACE_COMPILE_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_TIDY}"
    )

    set(Tidy_INCLUDE_DIRS ${Tidy_INCLUDE_DIR})
    set(Tidy_LIBRARIES ${Tidy_LIBRARY})
    mark_as_advanced(Tidy_INCLUDE_DIR Tidy_LIBRARY)
    set(Tidy_DEFINITIONS "${CONAN_COMPILE_DEFINITIONS_TIDY}")
endif()
