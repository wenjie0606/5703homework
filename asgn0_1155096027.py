import csv

def problem_1(a,b):
    num = 0
    for i in range(a,b+1):
        num+=int((i%7==0) & (i%3!=0))
    return num

def problem_2(n):
    result = 0
    if isinstance(n,int)&(0 <= n<10):
        result = 3*n+220*n+11000*n
        return result
    else:
        return 0

def problem_3(nums):
    max_sum = 0
    for a in range(2,len(nums)):
        t=nums[a-2]+nums[a-1]+nums[a]
        if t>max_sum:
            max_sum=t
    return max_sum

def problem_4(sentence):
    output = ""
    list1 = sentence.split( )
    list1.sort()
    output=" ".join(list1)
    return output

def problem_5(sentence):
    output = []
    sentence=sentence.lower()
    list2 = sentence.split( )
    list3 = list(set(list2))
    for i in range(0,len(list3)):
        output.append((list2.count(list3[i]),list3[i]))
    output.sort(reverse=1)
    return output[:5]

def problem_6(path_to_file):
    output = []
    with open(path_to_file) as csvfile:
        reader = csv.DictReader(csvfile)
        output = [row for row in reader]
    return output

if __name__=="__main__":
    print(problem_1(10, 30))
    print(problem_2(8))
    print(problem_3([1, 3, -2, 4, 8, -9, 0, 5]))
    print(problem_4("the chinese university of hong kong"))
    print(problem_5("""The Transmission Control Protocol (TCP) is one of the main protocols of the Internet protocol suite."""))
    print(problem_6(r'/Users/wenjiexu/Documents/assignment0.csv'))