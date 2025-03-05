def count_commas_in_line(filename, line_number=10):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 读取所有行
            lines = file.readlines()

            # 检查文件是否有足够的行数
            if len(lines) < line_number:
                return f"文件只有 {len(lines)} 行，不足 {line_number} 行"

            # 获取第十行内容 (索引从0开始，所以第十行是索引9)
            target_line = lines[line_number - 1]

            # 计算逗号数量
            comma_count = target_line.count(',')

            return f"第 {line_number} 行共有 {comma_count} 个逗号"

    except FileNotFoundError:
        return "文件不存在"
    except Exception as e:
        return f"发生错误: {str(e)}"


# 使用示例
filename = "pace0.txt"  # 替换为你的文件路径
result = count_commas_in_line(filename)
print(result)
