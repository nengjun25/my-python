import queue

def search(values, target):
    l = len(values)
    start = 0
    end = l - 1

    if target < values[start]:
        return start
    if target > values[end]:
        return end

    while start < end:
        mid = int((start + end) / 2)
        if start == mid:
            break
        if target < values[mid]:
            end = mid
        elif target > values[mid]:
            start = mid
        else:
            return mid

    return start + 1


def validator(values):
    gs = [{} for i in range(0, 9)]
    gc = [{} for i in range(0, 9)]
    gr = [{} for i in range(0, 9)]
    for i in range(0, 9):
        for j in range(0, 9):
            value = values[i][j]
            if value != -1:
                value = int(value)
                index = j // 3 + i // 3 * 3
                if value in gr[i]:
                    return False
                else:
                    gr[i][value] = 1
                if value in gc[j]:
                    return False
                else:
                    gc[j][value] = 1
                if value in gs[index]:
                    return False
                else:
                    gs[index][value] = 1
    return True


def resolve(values):
    back_trace(values, 0, 0)
    for j in values:
        print(j)
        print("\n")
    print(validator(values))


def back_trace(trace, c, r):
    if r == 9:
        return True

    if trace[r][c] != -1:
        if c < 8:
            if back_trace(trace, c + 1, r) is True:
                return True
        else:
            if back_trace(trace, 0, r + 1) is True:
                return True
    else:
        for i in range(1, 10):
            trace[r][c] = i
            if is_valid(r, c) is True:
                if c < 8:
                    if back_trace(trace, c + 1, r) is True:
                        return True
                else:
                    if back_trace(trace, 0, r + 1) is True:
                        return True
            trace[r][c] = -1
    return False


def is_valid(i, j):
    cs = j - j % 3
    rs = i - i % 3

    for k in range(0, 9):
        if k != j and test[i][k] == test[i][j]:
            return False
        if k != i and test[k][j] == test[i][j]:
            return False
        c = cs + k % 3
        r = rs + k // 3
        if (c != j or r != i) and test[r][c] == test[i][j]:
            return False
    return True


test = [
    [5, 3, -1, -1, 7, -1, -1, -1, -1],
    [6, -1, -1, 1, 9, 5, -1, -1, -1],
    [-1, 9, 8, -1, -1, -1, -1, 6, -1],
    [8, -1, -1, -1, 6, -1, -1, -1, 3],
    [4, -1, -1, 8, -1, 3, -1, -1, 1],
    [7, -1, -1, -1, 2, -1, -1, -1, 6],
    [-1, 6, -1, -1, -1, -1, 2, 8, -1],
    [-1, -1, -1, 4, 1, 9, -1, -1, 5],
    [-1, -1, -1, -1, 8, -1, -1, 7, 9],
]


# print(validator(test))
# resolve(test)


def get_ap(n):
    apn = "1"
    for i in range(0, n + 1):
        apn = ap_list(apn)
    print(apn)
    return apn


def ap_list(ap):
    print(ap)
    i = 0
    j = 0
    le = len(ap)
    s_list = []
    while i < le:
        if ap[i] != ap[j]:
            s_list.append(str(i - j))
            s_list.append(str(ap[j]))
            j = i
        if i == le - 1:
            s_list.append(str(i - j + 1))
            s_list.append(str(ap[j]))
        i = i + 1
    return "".join(s_list)


# get_ap(4)

res = []


def get_list_dup(choose, target):
    trace = []
    bt(trace, target, 0, choose)


def bt(trace, target, start, choose):
    if target == 0:
        res.append(trace.copy())
        return
    for i in range(start, len(choose)):
        if target - choose[i] < 0:
            continue
        trace.append(choose[i])
        bt(trace, target - choose[i], i, choose)
        trace.pop()


# get_list_dup([10, 1, 2, 7, 6, 1, 5], 8)
# print(res)


def get_list_once(choose, target):
    choose.sort(key=None)
    print(choose)
    trace = []
    bt2(trace, target, 0, choose)


def bt2(trace, target, start, choose):
    if target == 0:
        res.append(trace.copy())
        return
    for i in range(start, len(choose)):
        if i > start and choose[i] == choose[i - 1]:
            continue
        if target - choose[i] < 0:
            continue
        trace.append(choose[i])
        bt2(trace, target - choose[i], i + 1, choose)
        trace.pop()


# get_list_once([10, 1, 2, 7, 6, 1, 5], 8)
def multi(str1, str2):
    m = len(str1)
    n = len(str2)
    result = [0 for i in range(0, m + n)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            i1 = int(str2[i])
            i2 = int(str1[j])
            r = i1 * i2
            t = result[i + j + 1] + r % 10
            result[i + j + 1] = t % 10
            result[i + j] = t // 10 + r // 10
            # r = str(int(str2[i])*int(str1[j]))+"0"*(len(str2)-1-i+len(str1)-1-j)
            # result = do_sum(result, r)
    if result[0] == 0:
        del result[0]
    rs = [str(i) for i in result]
    return "".join(rs)


def do_sum(str1, str2):
    l1 = len(str1)
    l2 = len(str2)
    lm = l1
    if l1 > l2:
        x = l1 - l2
        str2 = "0" * x + str2
    elif l1 < l2:
        x = l2 - l1
        str1 = "0" * x + str1
        lm = l2
    result = [0 for i in range(0, lm + 1)]
    for i in range(0, lm):
        i1 = int(str1[::-1][i])
        i2 = int(str2[::-1][i])
        res = i1 + i2
        if res < 10:
            result[lm - i] = result[lm - i] + res
            if result[lm - i] > 9:
                r = result[lm - i]
                result[lm - i] = r % 10
                result[lm - i - 1] = result[lm - i - 1] + r // 10
        else:
            result[lm - i] = result[lm - i] + res % 10
            result[lm - i - 1] = result[lm - i - 1] + res // 10
            if result[lm - i] > 9:
                r = result[lm - i]
                result[lm - i] = r % 10
                result[lm - i - 1] = result[lm - i - 1] + r // 10

    if result[0] == 0:
        del result[0]
    rs = [str(i) for i in result]
    return "".join(rs)


print(multi("13", "13"))

rres = []


def all_range(choose):
    trace = []
    choose.sort()
    bt3(trace, choose, len(choose))


def bt3(trace, choose, total):
    print(trace)
    if len(trace) == total:
        rres.append(trace.copy())
        return
    for i in range(0, len(choose)):
        print(i)
        if i > 0 and choose[i] == choose[i - 1]:
            continue
        c = choose[i]
        trace.append(c)
        del choose[i]
        bt3(trace, choose, total)
        choose.insert(i, c)
        trace.pop()


all_range([1, 2, 1])
print(rres)


def sort_same(w_list):
    map_list = {}

    for w in w_list:
        fix = False
        for j in map_list.keys():
            if len(j) == len(w):
                for i in range(0, len(w)):
                    if w[i] not in j:
                        break
                    if i == len(w) - 1:
                        map_list[j].append(w)
                        fix = True
                if fix is True:
                    break
        if fix is False:
            map_list[w] = [w]

    print(map_list.values())
    return map_list.values()


sort_same(["eat", "tea", "tan", "ate", "nat", "bat"])


def p_pow(x, n):
    if n == 1:
        return x
    result = p_pow(x * x, n // 2)
    if n % 2 == 1:
        result = result * x
    return result


print(p_pow(6, 5))


def max_sublist(t_list):
    i = 0
    s_max = t_list[0]
    total = 0
    while i < len(t_list):
        if total + t_list[i] > 0:
            total = total + t_list[i]
            if total >= s_max:
                s_max = total
        else:
            total = 0
            if t_list[i] >= s_max:
                s_max = t_list[i]
        i = i + 1
    return s_max


max_sublist([1, 1, -3, 4, -1, 2, 1, -5, 4])

max_sublist([-2, -3, -2])


def jump(nums):
    trace = 0
    memo = {}
    print(bt4(trace, nums, memo))
    print(memo)


def bt4(trace, nums, memo):
    if trace == len(nums)-1:
        return True
    if trace in memo.keys():
        return memo[trace]

    for i in range(1, nums[trace]+1):
        if bt4(trace+i, nums, memo) is True:
            memo[trace] = True
            return True
    memo[trace] = False
    return False


jump([3, 2, 1, 0, 4])
jump([2, 3, 1, 1, 4])


def last_word(word):
    c = 0
    for i in range(len(word)-1, -1, -1):
        if word[i] != " ":
            c = c + 1
        elif c != 0:
            return c
    return c


kp_res = []


def k_permutation(n, k):
    trace = []
    choose = [i for i in range(1, n+1)]
    bt5(trace, choose, k)


def bt5(trace, choose, k):
    if len(trace) == len(choose):
        kp_res.append(trace.copy())
        if len(kp_res) == k:
            print(trace)
            return True
        else:
            return False
    for i in range(0, len(choose)):
        if choose[i] not in trace:
            trace.append(choose[i])
            if bt5(trace, choose, k) is True:
                return True
            trace.pop()
    return False


k_permutation(3, 3)
print(kp_res)


class Node(object):
    def __init__(self, index, weight, next_node=None):
        self.index = index
        self.weight = weight
        self.next_node = next_node


class AdjacentList(object):
    def __init__(self, number):
        self.number = number
        self.list = [None] * number

    def insert(self, origin, index, weight=1):
        node = Node(index, weight, self.list[origin - 1])
        self.list[origin - 1] = node
        print(self.list)

    def bfs(self, num):
        head = self.list[num-1]

        m_queue = queue.Queue()
        m_queue.put(head)

        while m_queue.empty() is not True:
            node = m_queue.get_nowait()
            print(node.index)
            while node.next_node is not None:
                m_queue.put(self.list[node.index-1])
                node = node.next_node

    def dfs(self, num):
        head = self.list[num - 1]
        stack = [head]
        while len(stack) > 0:
            node = stack.pop()
            print(node.index)
            while node.next_node is not None:
                stack.append(self.list[node.index-1])
                node = node.next_node


global total_trace
total_trace = 0
global count
count = 0


def get_trace(m, n):
    bt6(1, 1, m, n)


def bt6(x, y, m, n):
    global count
    count = count+1
    print(count)
    if x == m and y == n:
        global total_trace
        total_trace = total_trace + 1
        return
    if x < m:
        bt6(x+1, y, m, n)
    if y < n:
        bt6(x, y+1, m, n)


get_trace(10, 2)
