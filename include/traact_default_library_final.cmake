



target_include_directories(${TARGET_NAME} PRIVATE
$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/src>
)

if(WITH_CUDA)
        target_include_directories(${TARGET_NAME} PUBLIC ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})
        set_target_properties(${TARGET_NAME} PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
        target_compile_options(
                ${TARGET_NAME}
                BEFORE
                INTERFACE
                $<$<COMPILE_LANGUAGE:CUDA>:--extended-lambda -Xcompiler=-Wall,-Wextra,-Wfatal-errors>
)
endif()        

install(TARGETS ${TARGET_NAME}
        ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
        )
