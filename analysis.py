# -*- coding: utf-8 -*-

# rea = {
#     "up": 3,
#     "down": 4,
#     "left": 5,
#     "right": 8,
# }


def analysis_wenhu(filename):
    f = open(filename, "r")
    res = {
        "up": 0,
        "down": 0,
        "left": 0,
        "right": 0,
    }
    file_list = f.readlines()
    # useful_list = [i.split()[-1] if i.split()[-1] in ["Up", "Down", "Right", "Left"] else None for i in file_list]
    # print(useful_list)
    # filter(lambda x: res.update({:res.get(x.split()[-1])}), file_list)
    pass
    # for text in file_list:
    #     tip = text.split()[-1]
    #     if tip.strip() ==  "Up":
    #         score = res.get("up")
    #         score += 1
    #         res.update({
    #             "up": score
    #         })
    #     if tip.strip() == "Down":
    #         score = res.get("down")
    #         score += 1
    #         res.update({
    #             "down": score
    #         })
    #     if tip.strip() == "Right":
    #         score = res.get("right")
    #         score += 1
    #         res.update({
    #             "right": score
    #         })
    #     if tip.strip() == "Left":
    #         score = res.get("left")
    #         score += 1
    #         res.update({
    #             "left": score
    #         })
    # useful_list.append(text.split()[-1])
    return res


if __name__ == '__main__':
    res = analysis_wenhu("E:/py_share/user_logs/8ab04156-2c01-40ee-8a02-8bcc0fa01922.log")
    print(res)
