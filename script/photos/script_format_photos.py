import os
import shutil
from datetime import datetime


def format_month(month):
    monthNum = int(month)  # 将月份转换为整数类型
    return f'{monthNum:02d}'


def handle_error(error):
    print(f"遇到错误: {error}")


class PhotosFormatScript:
    def __init__(self):  # 初始化一个属性r（不要忘记self参数，他是类下面所有方法必须的参数）
        # 允许的文件扩展名
        self.allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.avi']

    # 格式化照片文件
    def formatPhotos(self, directory):
        print(f"Photos format start  dir = {directory} ")
        # 建立一个字典对象用于存储数据
        need_operator_photos = {}

        # 递归遍历文件夹
        for root, dirs, files in os.walk(directory, onerror=handle_error):
            # 遍历当前文件夹下的文件
            for file in files:
                # 拼接文件的完整路径
                file_path = os.path.join(root, file)

                # 判断路径是否为文件
                if os.path.isfile(file_path):
                    # 获取文件扩展名
                    _, ext = os.path.splitext(file_path)
                    ext = ext.lower()

                    # 如果文件扩展名是图片或视频类型
                    if ext in self.allowed_extensions:
                        # 获取文件的修改时间
                        mtime = os.path.getmtime(file_path)
                        modified_date = datetime.fromtimestamp(mtime)

                        #偶尔会存在修改时间和实际时间不一致,这时候需要比对一下file上的名字
                        '''仅仅支持标准的名字XXX_20220801_XXX这种'''
                        parts = file_path.split("_")
                        if len(parts) == 3:
                            day = parts[1]
                            # 并且第二个名字位数=8
                            if len(day) == 8 and day.isdigit():
                                date_obj = datetime.strptime(str(day), "%Y%m%d")
                                if date_obj < modified_date:
                                    modified_date = date_obj


                        # 构建目标文件夹路径
                        destination_folder = os.path.join(directory, str(modified_date.year),
                                                          format_month(modified_date.month))

                        # 获取当前文件所在的文件夹路径
                        current_folder = os.path.dirname(file_path)

                        # 判断当前文件夹路径与目标文件夹路径是否相同
                        if current_folder != destination_folder:
                            # 将文件对象和目标文件夹地址添加到字典中
                            need_operator_photos[file_path] = destination_folder

        # 遍历字典，进行文件移动操作
        for file_path, destination_folder in need_operator_photos.items():
            # 检查目标文件夹是否存在，如果不存在则创建
            if not os.path.exists(destination_folder):
                os.makedirs(destination_folder)

            try:
                # 移动文件到目标文件夹
                shutil.move(file_path, destination_folder)
                print(f"文件 {os.path.basename(file_path)} 已移动到 {destination_folder}")
            except Exception as e:
                print(f"移动文件 {os.path.basename(file_path)} 失败: {str(e)}")
                continue

        print(f"Photos format over !")
