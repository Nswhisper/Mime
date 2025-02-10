# -*- coding=utf-8 -*-
"""
    功能：按序修改MarkDown文件中的随机生成的图片名为数字序号
    作者：N's whisper
    版本：2024-09-13
"""
import os
import re
import shutil


def remd():
    current_directory = os.getcwd()
    files = os.listdir(current_directory)
    folder_name = ["img", "image", "uploads", "upload", "imgs", "images"]
    pic_dir = [name for name in files if name in folder_name]  # 列表推导式
    print("[*] 当前图片目录为 ", current_directory + "\\" + pic_dir[0], "注意确认")
    md_files = [file for file in files if file.endswith(".md")]
    print("[+] 搜索到 markdown 文件 ", md_files[0])
    md_file = current_directory + "\\" + md_files[0]
    pic_dir = current_directory + "\\" + pic_dir[0]

    with open(md_file, encoding="u8") as f:
        read_content = f.readlines()

    pic_index = 1
    processed_images = []
    tempfile = current_directory + "temp.md"
    with open(tempfile, "a", encoding="u8") as f:
        for line in read_content:
            pattern = re.compile(
                r"(upload_|image-)[a-z\d]{8,}"
            )  # 正则表达式，寻找以 upload_ 、 image- 为开头的图片名所在行
            match = re.search(pattern, line)
            if match:
                # 确定图片是否重复引用，以索引值确定修改后的文件名
                for index, pic_name in enumerate(processed_images):
                    if match.group() == pic_name:
                        print("    发现图片重复引用", match.group())
                        shutil.copy(
                            f"{pic_dir}/{str(index+1)}.png",
                            f"{pic_dir}/{str(pic_index)}.png",
                        )
                        print(
                            f"    复制文件{str(index+1)}.png为{str(pic_index)}.png"
                        )  # 将已处理过的文件复制，直接重命名，以免重复命名导致报错
                        new_line_content = re.sub(pattern, str(pic_index), line)
                        f.write(new_line_content)
                        pic_index += 1
                if match.group() not in processed_images:
                    new_line_content = re.sub(
                        pattern, str(pic_index), line
                    )  # 替换原文件中的图片名，生成临时文件内容
                    f.write(new_line_content)  # 将修改后的内容写入临时文件
                    os.rename(
                        f"{pic_dir}/{match.group()}.png",
                        f"{pic_dir}/{str(pic_index)}.png",
                    )  # 将图片目录下的图片文件同步重命名
                    print("   ", pic_index, " - ", match.group())
                    processed_images.append(match.group())  # 将修改后的图片名加入列表
                    pic_index += 1
            else:
                f.write(line)
        f.close()
    print(f"[+] {len(processed_images)}张图片重命名完成")
    os.remove(md_file)  # 删除原文件
    os.rename(tempfile, md_file)  # 将临时文件修改为原文件


if __name__ == "__main__":
    remd()
