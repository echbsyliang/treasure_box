import itchat
import os
import math
import PIL.Image as Image

# 好友头像缓存路径
IMG_DIR = os.getcwd() + '/img/'
# 合成矩阵图保存路径
MERGE_PNG = '/heiheipiupiupiu.png'
MERGE_PATH = '/Users/ton/Downloads' + MERGE_PNG
# 用户头像压缩(数字越大，合成图像质量越高)
HEAD_IMG_WIDTH = 80
HEAD_IMG_HEIGHT = 80


# 下载好友头像
def download_imgs(firends):
    num = 1
    try:
        for firend in firends:
            img_name = str(num) + '.jpg'
            img = itchat.get_head_img(userName=firend['UserName'])
            with open(IMG_DIR + img_name, 'wb') as file:
                file.write(img)
            print(u'已下载：%d' % num)
            num += 1
        return num
    except FileNotFoundError:
        os.mkdir(IMG_DIR)
        return download_imgs(firends)


# 加工头像列表信息
def process_imgs():
    # 头像列表
    img_list = []

    for root, dirs, files in os.walk(IMG_DIR):
        for file in files:
            if "jpg" in file and os.path.getsize(os.path.join(root, file)) > 0:
                img_list.append(os.path.join(root, file))

    img_num = len(img_list)

    max_column = int(math.sqrt(img_num))
    max_row = int(math.sqrt(img_num))

    return img_list, img_num, max_column, max_row


# 合成好友头像矩阵图
def merge_imgs():
    img_list, img_num, max_column, max_row = process_imgs()
    print(max_column, max_row, img_num)

    num = 0
    imgs_count = max_column * max_row

    # 创建空白画板
    white_board = Image.new('RGBA', (HEAD_IMG_WIDTH * max_column, HEAD_IMG_HEIGHT * max_row))

    # 逐行列绘制好友头像
    for i in range(0, max_row):
        for j in range(0, max_column):

            head_img = Image.open(img_list[num])
            # 等比例压缩头像
            temp_head_img = head_img.resize((HEAD_IMG_WIDTH, HEAD_IMG_HEIGHT))
            # 绘画位置
            place = (int(j % max_row * HEAD_IMG_WIDTH), int(i % max_row * HEAD_IMG_HEIGHT))
            # 绘制粘贴
            white_board.paste(temp_head_img, place)

            num = num + 1
            if num >= len(img_list):
                break

        if num >= imgs_count:
            break

    print(white_board.size)
    white_board.save(MERGE_PATH)


# 清除好友头像缓存
def clean_imgs(path):
    for img in os.listdir(path):
        i = os.path.join(path, img)
        if os.path.isfile(i):
            os.remove(i)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)
    # 好友列表
    firends = itchat.get_friends(update=True)
    print('[···开始下载好友头像···]')
    num = download_imgs(firends)
    count = num - 1
    print(u'[···头像下载完成，总计下载数量为：%d···]' % count)

    print('[···开始合成好友头像···]')
    merge_imgs()
    print('[···合成好友头像完成···]')

    print('[···开始清除好友头像缓存···]')
    clean_imgs(IMG_DIR)
    print('[···清除缓存完成···]')
