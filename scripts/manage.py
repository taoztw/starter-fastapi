import os
import argparse
import shutil


# 创建包结构的命令函数
def create_package_structure(args):
    name = args.name
    base_dir = os.path.join("apis", name)

    if args.type == "folder":
        dirs = ["api", "utils", "schemas", "service"]

        for dir_name in dirs:
            dir_path = os.path.join(base_dir, dir_name)
            os.makedirs(dir_path, exist_ok=True)
            init_path = os.path.join(dir_path, "__init__.py")
            with open(init_path, "w"):
                pass
        with open(os.path.join(base_dir, "__init__.py"), "w"):
            pass
        print(f"包结构 '{name}' 创建成功.")
    elif args.type == "file":
        os.makedirs(base_dir, exist_ok=True)
        files = ["__init__.py", "api.py", "utils.py", "schemas.py", "service.py"]
        for file in files:
            file_path = os.path.join(base_dir, file)
            with open(file_path, "w"):
                pass
        print(f"文件结构 '{name}' 创建成功.")


# 删除 API 目录的命令函数
def delete_api_directory(args):
    name = args.name
    api_dir = os.path.join("apis", name)

    # 检查目录是否存在，然后删除
    if os.path.exists(api_dir):
        shutil.rmtree(api_dir)
        print(f"API 目录 '{api_dir}' 删除成功。")
    else:
        print(f"要删除的 API 目录 '{api_dir}' 不存在。")


# 初始化 argparse 对象和子命令解析器
parser = argparse.ArgumentParser(description="处理用户命令。")
subparsers = parser.add_subparsers(help="支持的命令")

# 创建 'create' 命令的解析器
create_parser = subparsers.add_parser("create", help="创建一个新的包结构")
create_parser.add_argument("name", help="包名")
create_parser.add_argument(
    "type", help="包类型，分别folder 和 file，一般情况下file就足够了，除非是大项目"
)
create_parser.set_defaults(func=create_package_structure)

# 创建 'delete' 命令的解析器
delete_parser = subparsers.add_parser("delete", help="删除一个API目录")
delete_parser.add_argument("name", help="要删除的API目录的包名")
delete_parser.set_defaults(func=delete_api_directory)

# 解析命令行参数
args = parser.parse_args()

# 如果某命令被调用，执行其关联的函数
if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()
