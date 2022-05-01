'''Programmers Coding Test Practice'''

import os
import sys

def Hash1():
    # https://programmers.co.kr/learn/courses/30/lessons/42576?language=python3

    print("해시 완주하지 못한 선수")

    def solution(participant, completion):
        answer = ''.join(set(participant) - set(completion))

        # print(answer)
        
        if not answer:
            for name in completion:
                if participant.count(name) != completion.count(name):
                    answer = name
                    break
        return answer

    def solution_(participant, completion):
                
        cp = {}
        for name in completion:
            if name in cp.keys():
                cp[name] += 1
            else:
                cp[name] = 1
        
        for name in participant:
            if name in cp.keys():
                cp[name] -= 1
                if cp[name] < 0:
                    answer = name
                    
            else:
                answer = name    
        return answer

    participant = ["leo", "kiki", "eden"]
    completion = ["eden", "kiki"]
    result = "leo"
    if result == solution(participant, completion):
        print('성공!')
    else:
        print('실패...')        

    participant = ["marina", "josipa", "nikola", "vinko", "filipa"]
    completion = ["josipa", "filipa", "marina", "nikola"]
    result = "vinko"
    if result == solution(participant, completion):
        print('성공!')
    else:
        print('실패...')        

    participant = ["mislav", "stanko", "mislav", "ana"]
    completion = ["stanko", "ana", "mislav"]
    result = "mislav"
    if result == solution(participant, completion):
        print('성공!')
    else:
        print('실패...')        


def hash2():
    # https://programmers.co.kr/learn/courses/30/lessons/42577?language=python3
    print('해시 전화번호 목록')

    def solution(phone_book):
        phone_book.sort()
        
        for i in range(len(phone_book)-1):
            if phone_book[i+1].startswith(phone_book[i]):
                return False
        
        return True
    
    phone_book = ["119", "97674223", "1195524421"]
    result = False
    if result == solution(phone_book):
        print('성공!')
    else:
        print('실패...')
    
    phone_book = ["123","456","789"]
    result = True
    if result == solution(phone_book):
        print('성공!')
    else:
        print('실패...')
    
    phone_book = ["12","123","1235","567","88"]
    result = False
    if result == solution(phone_book):
        print('성공!')
    else:
        print('실패...')


def hash3():
    # https://programmers.co.kr/learn/courses/30/lessons/42578?language=python3
    print('해시 위장')
    
    def solution(clothes):
        # (종류1개수+1)*(종류2개수+1).... - 1 = 정답
        dict_c = {}
        for cloth in clothes:
            if cloth[1] in dict_c.keys():
                dict_c[cloth[1]] += 1
            else:
                dict_c[cloth[1]] = 2
        
        answer = 1
        for v in dict_c.values():
            answer *= v
        
        return answer-1

    phone_book = [["yellowhat", "headgear"], ["bluesunglasses", "eyewear"], ["green_turban", "headgear"]]
    result = 5
    if result == solution(phone_book):
        print('성공!')
    else:
        print('실패...')

    phone_book = [["crowmask", "face"], ["bluesunglasses", "face"], ["smoky_makeup", "face"]]
    result = 3
    if result == solution(phone_book):
        print('성공!')
    else:
        print('실패...')


def hash4():
    # https://programmers.co.kr/learn/courses/30/lessons/42579?language=python3
    print('해시 베스트앨범')

    def solution(genres, plays):
        dict_track = {genre:[] for genre in set(genres)}
        dict_count = {genre:0 for genre in set(genres)}
        
        for i, (g, p) in enumerate(zip(genres, plays)):
            dict_track[g].append((p, i))
            dict_count[g] += p
            
        sorted_count = list(r[0] for r in sorted(dict_count.items(), key=lambda x: x[1], reverse=True))
        
        answer = []
        for g in sorted_count:
            track = dict_track[g]
            track.sort(key=lambda x:(-x[0], x[1]))
            result = [t[1] for t in track[:2]]
            
            answer.extend(result)
        
        return answer

    def solution_(genres, plays):
        dict_song = {}
        dict_count = {}
        for i, g in enumerate(genres):
            if g in dict_song.keys():
                #count
                dict_count[g] += plays[i]
            
                #song idx
                list_g = dict_song[g]           
                if len(list_g) < 2:
                    idx = list_g[0]
                    if plays[i] > plays[idx]: #현재 i번째의 plays값이 기존 값보다 큼
                        list_g.insert(0, i) #맨 앞 추가  
                    else: #같거나 작음
                        list_g.append(i)
                else:
                    idx1, idx2 = list_g[0], list_g[1]
                    if plays[i] >= plays[idx1]:
                        insert_i = 0 if plays[i] > plays[idx1] else 1                    
                        list_g.insert(insert_i, i)
                        list_g = list_g[:-1]
                
                    elif plays[i] > plays[idx2]:
                        list_g.insert(1, i)
                        list_g = list_g[:-1]
                    
                # print(list_g)
            
                dict_song[g] = list_g
                        
            else:
                #count 
                dict_count[g] = plays[i]
            
                #song idx
                dict_song[g] = [i]
                        
        # print(dict_song)
        # print(dict_count)

        answer = []
        sorted_count = dict(sorted(dict_count.items(), key=lambda x: x[1], reverse=True))
        print(sorted_count)
        for k in sorted_count.keys():
            answer.extend(dict_song[k])

        return answer

    

    genres = ["classic", "pop", "classic", "classic", "pop"]
    plays = [500, 600, 150, 800, 2500]
    result = [4, 1, 3, 0]
    if result == solution(genres, plays):
        print('성공!')
    else:
        print('실패...')  

       		
    



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