# -*- coding: utf8 -*-


class Apriori():

    def __init__(self, data, min_support, min_confidence):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.fre_list = list()

        self.data = data

        self.apriori = []

        self.record_list = list()
        self.record_dict = dict()
        self.get_c1()

        # 不断进行自连接和剪枝，直到得到最终的频繁集为止;终止条件是，如果自连接得到的已经不再是频繁集
        # 那么取最后一次得到的频繁集作为结果
        while True:
            self.record_list = self.fre_list
            new_list = self.get_candidateset()
            judge_dict = self.judge(new_list)
            if len(judge_dict) == 0:
                break
            else:
                self.record_dict = judge_dict
        # print("The final frequency set is:")
        # print(self.record_list)

        print("support----------------------------------------------------------------")
        for x in self.apriori:
            print(x)

        # 根据频繁集计算关联规则
        print("confidence----------------------------------------------------------------")
        self.cal_associative_rule(self.record_list)

    def get_c1(self):
        self.record_list = list()
        self.record_dict = dict()
        new_dict = dict()
        for row in self.data:
            for item in row:
                if item not in self.fre_list:
                    self.fre_list.append(item)
                    new_dict[item] = 1
                else:
                    new_dict[item] = new_dict[item] + 1
        self.fre_list.sort()
        # print("candidate set:")
        # self.print_dict(new_dict)
        for key in self.fre_list:
            if new_dict[key] < self.min_support:
                del new_dict[key]
        # print("after pruning:")
        # self.print_dict(new_dict)
        self.get_all_apriori(new_dict)
        self.record_list = self.fre_list
        self.record_dict = self.record_dict

    def get_candidateset(self):
        new_list = list()
        # 自连接
        for i in range(0, len(self.fre_list)):
            for j in range(0, len(self.fre_list)):
                if i == j:
                    continue
                # 如果两个k项集可以自连接，必须保证它们有k-1项是相同的
                if self.has_samesubitem(self.fre_list[i], self.fre_list[j]):
                    curitem = self.fre_list[i] + ',' + self.fre_list[j]
                    curitem = curitem.split(",")
                    curitem = list(set(curitem))
                    curitem.sort()
                    curitem = ','.join(curitem)
                    # 如果一个k项集要成为候选集，必须保证它的所有子集都是频繁的
                    if self.has_infresubset(curitem) is False and self.already_constains(curitem, new_list) is False:
                        new_list.append(curitem)
        new_list.sort()
        return new_list

    def has_samesubitem(self, str1, str2):
        str1s = str1.split(",")
        str2s = str2.split(",")
        if len(str1s) != len(str2s):
            return False
        nums = 0
        for items in str1s:
            if items in str2s:
                nums += 1
                str2s.remove(items)
        if nums == len(str1s) - 1:
            return True
        else:
            return False

    def judge(self, candidatelist):
        # 计算候选集的支持度
        new_dict = dict()
        for item in candidatelist:
            new_dict[item] = self.get_support(item)
        # print("candidate set:")
        # self.print_dict(new_dict)
        # 剪枝
        # 频繁集的支持度要大于最小支持度
        new_list = list()
        for item in candidatelist:
            if new_dict[item] < self.min_support:
                del new_dict[item]
                continue
            else:
                new_list.append(item)
        self.fre_list = new_list
        # print("after pruning:")
        # self.print_dict(new_dict)
        self.get_all_apriori(new_dict)
        return new_dict

    def has_infresubset(self, item):
        # 由于是逐层搜索的，所以对于Ck候选集只需要判断它的k-1子集是否包含非频繁集即可
        subset_list = self.get_subset(item.split(","))
        for item_list in subset_list:
            if self.already_constains(item_list, self.fre_list) is False:
                return True
        return False

    def get_support(self, item, splitetag=True):
        if splitetag:
            items = item.split(",")
        else:
            items = item.split("--")
        support = 0
        for row in self.data:
            tag = True
            for curitem in items:
                if curitem not in row:
                    tag = False
                    continue
            if tag:
                support += 1
        return support

    def get_fullpermutation(self, arr):
        if len(arr) == 1:
            return [arr]
        else:
            newlist = list()
            for i in range(0, len(arr)):
                sublist = self.get_fullpermutation(arr[0:i] + arr[i + 1:len(arr)])
                for item in sublist:
                    curlist = list()
                    curlist.append(arr[i])
                    curlist.extend(item)
                    newlist.append(curlist)
            return newlist

    def get_subset(self, arr):
        newlist = list()
        for i in range(0, len(arr)):
            arr1 = arr[0:i] + arr[i + 1:len(arr)]
            newlist1 = self.get_fullpermutation(arr1)
            for newlist_item in newlist1:
                newlist.append(newlist_item)
        newlist.sort()
        newlist = self.remove_dumplicate(newlist)
        return newlist

    def remove_dumplicate(self, arr):
        newlist = list()
        for i in range(0, len(arr)):
            if self.already_constains(arr[i], newlist) is False:
                newlist.append(arr[i])
        return newlist

    def already_constains(self, item, curlist):
        items = list()
        if isinstance(item, str):
            items = item.split(",")
        else:
            items = item
        for i in range(0, len(curlist)):
            curitems = list()
            if isinstance(curlist[i], str):
                curitems = curlist[i].split(",")
            else:
                curitems = curlist[i]
            if len(set(items)) == len(curitems) and len(list(set(items).difference(set(curitems)))) == 0:
                return True
        return False

    def print_dict(self, curdict):
        keys = curdict.keys()
        keys = [curkey for curkey in keys]
        keys.sort()
        for curkey in keys:
            print("%s:%s" % (curkey, curdict[curkey]))

    # 计算关联规则的方法
    def get_all_subset(self, s):
        from itertools import combinations
        return sum(map(lambda r: list(combinations(s, r)), range(1, len(s) + 1)), [])

    def get_all_apriori(self, curdict):
        keys = curdict.keys()
        keys = [curkey for curkey in keys]
        for curkey in keys:
            # self.apriori[curkey] = curdict[curkey]
            self.apriori.append({curkey: curdict[curkey]})

    def cal_associative_rule(self, frelist):
        rule_list = list()
        rule_dict = dict()
        for fre_item in frelist:
            fre_items = fre_item.split(",")
            subitem_list = self.get_all_subset(fre_items)
            for subitem in subitem_list:
                # 忽略为为自身的子集
                if len(subitem) == len(fre_items):
                    continue
                else:
                    difference = set(fre_items).difference(subitem)
                    rule_list.append("--".join(subitem) + " --> " + "--".join(difference))
        print("The rule is:")
        for rule in rule_list:
            conf = self.cal_rule_confidency(rule)
            print("{0}   {1}".format(rule, conf))
            if conf >= self.min_confidence:
                rule_dict[rule] = conf
        print("The associative rule is:")
        for key in rule_list:
            if key in rule_dict.keys():
                print("{0} : {1}".format(key, rule_dict[key]))

    def cal_rule_confidency(self, rule):
        rules = rule.split(" --> ")
        support1 = self.get_support("--".join(rules), False)
        support2 = self.get_support(rules[0], False)
        if support2 == 0:
            return 0
        rule_confidency = float(support1) / float(support2)
        return rule_confidency


if __name__ == '__main__':
    data = [
        ["A", "B", "E"],
        ["B", "D"],
        ["B", "C"],
        ["A", "B", "D"],
        ["A", "C"],
        ["B", "C"],
        ["A", "C"],
        ["A", "B", "C", "E"],
        ["A", "B", "C"]
    ]

    # min_support 1 - len(data)
    min_support = 1
    min_confidence = 0.6
    Apriori(data, min_support, min_confidence)
