# 脚本运行的管理类
import configparser
from script.photos.script_format_photos import PhotosFormatScript


def main():
    # 创建配置解析器对象
    config = configparser.ConfigParser()

    # 读取配置文件
    config.read('config.ini')
    # 照片文件目录格式化
    formatPhotosFile(config)


def formatPhotosFile(config):  # 格式化照片文件目录
    # 获取配置项的值
    photos_dir = config.get('common', 'photos_dir')
    # 创建格式化脚本对象
    photosFormat = PhotosFormatScript()
    # 文件地址格式化
    photosFormat.formatPhotos(photos_dir)


# 调用主函数作为程序的入口
if __name__ == "__main__":
    main()
