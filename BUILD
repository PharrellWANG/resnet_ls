package(default_visibility = [":internal"])

licenses(["notice"])  # Apache 2.0

exports_files(["LICENSE"])

package_group(
    name = "internal",
    packages = [
        "//resnet/...",
    ],
)

filegroup(
    name = "py_srcs",
    data = glob([
        "**/*.py",
    ]),
)

py_library(
    name = "resnet_model",
    srcs = ["resnet_model.py"],
)

py_binary(
    name = "resnet_main",
    srcs = [
        "resnet_main.py",
    ],
    deps = [
        ":data_input",
        ":resnet_model",
    ],
)

py_library(
    name = "data_input",
    srcs = ["data_input.py"],
)
