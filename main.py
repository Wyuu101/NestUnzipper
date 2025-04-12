import zipfile
import os
import shutil

# 判断是否为压缩包文件
def is_zip_file(filename):
    return zipfile.is_zipfile(filename)

# 获取内层压缩包名称以作为解压密码
def get_inner_zip_name(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # 返回第一个 .zip 文件名，不带后缀
        for name in zip_ref.namelist():
            if name.endswith('.zip'):
                # 获取去掉后缀的文件名
                return os.path.splitext(os.path.basename(name))[0]
    return None

# 用密码解压文件
def extract_zip_with_password(zip_path, password, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(path=extract_dir, pwd=password.encode('utf-8'))

# 解压缩包套娃主逻辑
def nested_unzip(start_zip):
    current_zip = start_zip
    current_dir = os.path.dirname(os.path.abspath(start_zip))
    count = 0

    while is_zip_file(current_zip):
        temp_dir = os.path.join(current_dir, f"unzipped_{count}")
        os.makedirs(temp_dir, exist_ok=True)

        # 用内部 zip 文件名作为密码
        password = get_inner_zip_name(current_zip)
        if not password:
            print(f"❌ 无法获取密码，{current_zip} 中未找到 zip 文件")
            break

        print(f"🧩 解压第 {count + 1} 层：{current_zip}，使用密码：{password}")

        try:
            extract_zip_with_password(current_zip, password, temp_dir)
        except RuntimeError as e:
            print(f"❌ 解压失败：{e}")
            break

        # 查找下一个压缩包
        next_zip = None
        for file in os.listdir(temp_dir):
            if file.endswith('.zip'):
                next_zip = os.path.join(temp_dir, file)
                break

        if not next_zip:
            print("✅ 没有发现更多 zip 文件，解压完成！")
            break

        current_zip = next_zip
        count += 1

if __name__ == "__main__":
    start_zip_path = "1.zip"  # 改成你的入口压缩包名
    nested_unzip(start_zip_path)
