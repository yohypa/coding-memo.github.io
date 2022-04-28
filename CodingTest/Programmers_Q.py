'''Programmers Coding Test Practice'''

import os
import sys


def ExhaustiveSearch1():
    # https://programmers.co.kr/learn/courses/30/lessons/42840?language=python3
    print('완전탐색 모의고사')

    def solution(answers):
        std1 = [1, 2, 3, 4, 5]
        std2 = [2, 1, 2, 3, 2, 4, 2, 5]
        std3 = [3, 3, 1, 1, 2, 2, 4, 4, 5, 5]
        
        count = [0,0,0]
        
        for i, answer in enumerate(answers):
            if answer == std1[i%5] : count[0] += 1
            if answer == std2[i%8] : count[1] += 1
            if answer == std3[i%10] : count[2] += 1
        
        # print(count)
        max_ = max(count) #count 중 가장 큰 값
        max_idx = [i+1 for i, c in enumerate(count) if c == max_]
        # print(max_idx)
        
        return max_idx
        
    answers = [1,2,3,4,5]
    result = [1]
    if result == solution(answers):
        print('성공!')
    else:
        print('실패...')
    
    answers = [1,3,2,4,2]
    result = [1,2,3]
    if result == solution(answers):
        print('성공!')
    else:
        print('실패...')


def ExhaustiveSearch2():
    # https://programmers.co.kr/learn/courses/30/lessons/42839
    print('완전탐색 소수 찾기')

    from itertools import permutations
    def getPrime(n):
        if 0 <= n <= 1:
            return 0
            
        for i in range(2, n//2+1):
            if n%i == 0:
                return 0
        return n 

    def solution(numbers):
        list_num = list(numbers)
        # print(list_num)
                
        result = set()
        for length in range(1, len(numbers)+1):
            
            set_permu = set(map(lambda x:int(''.join(x)), permutations(list_num, length))) 
            set_permu -= (set_permu & result) #set_permu.intersection(result) #result에 있는 값은 제외
            
            # print(set_permu)
            set_result = set(map(getPrime, set_permu))
                
            result |= set_result #set|set ==> 합집합, set&set ==> 교집합
            
        result -= set([0]) #0 빼기
        # print(result)

        return len(result)
    
    numbers = "17"
    result = 3
    if result == solution(numbers):
        print('성공!')
    else:
        print('실패...')

    numbers = "011"
    result = 2
    if result == solution(numbers):
        print('성공!')
    else:
        print('실패...')


def ExhaustiveSearch3():
    # https://programmers.co.kr/learn/courses/30/lessons/42842
    print('완전탐색 카펫')

    def solution(brown, yellow):
        # yellow = ylw_x*ylw_y
        # brown = (ylw_x+ylw_y)*2 + 4
        # x, y = ylw_x+2, ylw_y+2
        
        for ylw_x in range(yellow, 0, -1):
            if yellow%ylw_x == 0 :
                ylw_y = yellow//ylw_x        

                if (ylw_x+ylw_y)*2 + 4 == brown:
                    return [ylw_x+2, ylw_y+2]
    
    brown, yellow = 10, 2 
    result = [4,3]
    if result == solution(brown, yellow):
        print('성공!')
    else:
        print('실패...')

    brown, yellow = 8, 1 
    result = [3,3]
    if result == solution(brown, yellow):
        print('성공!')
    else:
        print('실패...')

    brown, yellow = 24, 24 
    result = [8,6]
    if result == solution(brown, yellow):
        print('성공!')
    else:
        print('실패...')



def main():
    # ExhaustiveSearch1()
    # ExhaustiveSearch2()
    ExhaustiveSearch3()

if __name__ == "__main__":
    main()