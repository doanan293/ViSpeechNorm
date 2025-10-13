from vietnam_number.number2word.hundreds import n2w_hundreds
from vietnam_number.number2word.utils.base import chunks


def n2w_large_number(numbers: str):
    """Hàm chuyển đổi các số có giá trị lớn.

    Hàm chuyển đổi các số có giá trị lớn từ 999 đến 999.999.999.999

    Args:
        numbers (str): Chuỗi số đầu vào.

    Returns:
        Chuỗi chữ số đầu ra.

    """
    # Chúng ta cần duyệt chuổi số đầu vào từ phải sang trái nhằm phân biệt các giá trị từ nhỏ đến lớn.
    # tương tự như khi chúng ta xữ lý cho hàm n2w_hundreds
    temp = numbers
    for v in temp:
        if v == '0':
            numbers = numbers[1:]
        else:
            break
    reversed_large_number = numbers[::-1]

    # Chia chuỗi số đầu vào thành các nhóm con có 3 phần tử.
    # vì cứ 3 phần tử số lại tạo thành một lớp giá trị, như lớp trăm, lớp nghìn, lớp triệu...
    reversed_large_number = chunks(reversed_large_number, 3)

    total_number = []
    for e in range(0, len(reversed_large_number)):
        if e == 0:
            value_of_hundred = reversed_large_number[e][::-1]

            if value_of_hundred not in ['000','00','0']: 
                total_number.append(n2w_hundreds(value_of_hundred))
        elif (e-1) % 3 == 0:
            value_of_thousand = reversed_large_number[e][::-1]

            if value_of_thousand not in ['000','00','0']: 
                total_number.append(n2w_hundreds(value_of_thousand) + ' nghìn ')
        elif (e+1) % 3 == 0:
            value_of_million = reversed_large_number[e][::-1]

            if value_of_million not in ['000','00','0']: 
                total_number.append(n2w_hundreds(value_of_million) + ' triệu ')
        elif (e) % 3 == 0:
            value_of_billion = reversed_large_number[e][::-1]

            if value_of_billion not in ['000','00','0']: 
                total_number.append(n2w_hundreds(value_of_billion) + ' tỷ ')
            elif e >= 3:
                total_number.append('tỷ ')

    return ''.join(total_number[::-1]).strip()


if __name__ == '__main__':

    number = '4680000000'
    print(n2w_large_number(number))
