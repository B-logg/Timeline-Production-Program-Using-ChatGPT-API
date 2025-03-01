import os
import math
import collections


class Group:     # Node 개념
    code = 1

    def __init__(self):
        self.element = []     # 강의의 연번을 담는 리스트
        self.next = None     # 다음 그룹을 향한 포인터
        self.cnt = 0     # 그룹에 담긴 강의의 개수
        self.code = Group.code     # 그룹의 고유번호
        Group.code += 1

    def add_lecture(self, lecture_number):     # 강의 담기 함수
        selected[lecture_number] = self.code
        self.element.append(lecture_number)
        self.cnt += 1
        return

    def remove_lecture(self, lecture_number):     # 강의 제거하기 함수
        selected[lecture_number] = None
        self.element.remove(lecture_number)
        self.cnt -= 1
        return

    def sort(self):     # 평점이 높은 순으로 강의 정렬하기 함수
        self.element.sort(key=lambda x: lecture_list[x][-1], reverse=True)
        return

    def empty(self):     # 강의 모두 제거하기 함수
        for lecture_number in self.element:
            selected[lecture_number] = None
        self.element = []
        self.cnt = 0
        return


class GroupList:     # Linked-List 개념
    def __init__(self):
        self.head = None     # 첫 번째 그룹을 가리키는 포인터
        self.cnt = 0     # 그룹의 개수

    def add_group(self):     # 마지막에 새로운 그룹 추가하기 함수
        new_group = Group()

        if self.cnt == 0:
            self.head = new_group

        else:
            current_group = self.head
            while current_group.next is not None:
                current_group = current_group.next
            current_group.next = new_group

        self.cnt += 1
        return

    def remove_group(self, group_number):     # 그룹 제거하기 함수
        current_group = self.head

        if self.cnt == 1:     # 유일한 그룹을 제거
            self.head = None
            current_group.empty()
            del current_group
            self.cnt -= 1

        elif group_number == 1:     # 첫 번째 그룹을 제거
            self.head = current_group.next
            current_group.empty()
            del current_group
            self.cnt -= 1

        else:
            for _ in range(group_number - 1):
                pre_group = current_group
                current_group = current_group.next

            if current_group.next is None:     # 마지막 그룹을 제거
                pre_group.next = None
                current_group.empty()
                del current_group
                self.cnt -= 1

            else:     # 일반적인 중간 그룹을 제거
                pre_group.next = current_group.next
                current_group.empty()
                del current_group
                self.cnt -= 1

        return

    def get_nth_group(self, group_number):     # n번째 그룹을 반환하는 함수
        current_group = self.head
        for _ in range(group_number - 1):
            current_group = current_group.next
        return current_group


# 재귀 탐색에서 사용되는 global 자료형
generated_list = []     # 재귀를 통해 생성된 시간표들을 저장하는 리스트
day_dictionary = {'월': 'MON', '화': 'TUE', '수': 'WED', '목': 'THU', '금': 'FRI'}
time_piece = set()     # 재귀 과정에서 시간 조각을 임시로 저장하는 셋
stack = []     # 재귀 과정에서 강의를 임시로 저장하는 리스트


def recursion(group):     # 재귀 탐색
    global generated_list
    global day_dictionary
    global time_piece
    global stack

    if group is None:     # *Base Case*
        generated_list.append(stack[:])
        return

    for lecture in group.element:     # *Recursive Call*
        make_piece = []     # 강의 시간을 시간 조각으로 변환하고 모으는 리스트
        temp = lecture_list[lecture][5].split(',')     # 연번으로 강의 시간 불러오기
        day = None
        for thing in temp:
            if thing.isnumeric():
                make_piece.append(day_dictionary[day] + thing)
            else:
                day = thing[0]
                make_piece.append(day_dictionary[day] + thing[1:])

        for piece in make_piece:     # 백트래킹(시간 충돌 조사)
            if piece in time_piece:
                break
        else:
            for piece in make_piece:
                time_piece.add(piece)
            stack.append(lecture)
            recursion(group.next)     # 재귀 진입
            stack.pop()
            for piece in make_piece:
                time_piece.remove(piece)

    return


def filter_table(MORNING, FREE, CONTINUE):     # 사용자가 설정한 조건에 부합하는 시간표를 필터링
    global generated_list
    global day_dictionary

    filtered_list = []     # 필터링된 시간표를 모으는 리스트
    for table in generated_list:
        current_table = collections.defaultdict(list)     # 강의 시간을 시간 조각으로 변환하고 모으는 딕셔너리
        for lecture in table:
            temp = lecture_list[lecture][5].split(',')
            day = None
            for thing in temp:
                if thing.isnumeric():
                    current_table[day_dictionary[day]].append(int(thing))
                else:
                    day = thing[0]
                    current_table[day_dictionary[day]].append(int(thing[1:]))

        flag = False     # 조건 충돌 유무를 확인

        if isinstance(MORNING, list):
            for day in MORNING:
                if 1 in current_table[day]:
                    flag = True
                    break

        if isinstance(MORNING, int):
            cnt = 0
            for value in current_table.values():
                if 1 in value:
                    cnt += 1
            if cnt > MORNING:
                flag = True

        if isinstance(FREE, list):
            for day in FREE:
                if current_table[day]:
                    flag = True
                    break

        if isinstance(CONTINUE, int):
            for key in current_table.keys():
                for time in current_table[key]:
                    for next_time in range(time, time + CONTINUE * 2 + 1):
                        if next_time not in current_table[key]:
                            break
                    else:
                        flag = True
                        break
                if flag:
                    break

        if not flag:     # 생존한 시간표를 저장
            filtered_list.append(table)

    return filtered_list


# lecture_DB의 정보를 리스트 형태로 업로드
dir = os.getcwd()
file = open(dir + r'/lecture_DB.txt', mode='r', encoding='UTF-8')
lecture_list = [file.readline().split()]
for line in file.read().split('\n'):
    temp = line.split()
    temp[0] = int(temp[0])     # 연번은 정수형으로 변환
    temp[8] = float(temp[8])     # 평점은 실수형으로 변환
    lecture_list.append(temp)
file.close()
page_len = math.ceil((len(lecture_list) - 1) / 10)
if page_len == 0:
    page_len = 1

# 해당 연번의 강의가 특정 그룹에 담겼는지 판별
selected = [None] * len(lecture_list)


def update_lecture_DB(search):     # 강의명 검색에 따라 정보를 선별
    global dir
    global lecture_list
    global page_len

    file = open(dir + r'/lecture_DB.txt', mode='r', encoding='UTF-8')
    lecture_list = [file.readline().split()]
    for line in file.read().split('\n'):
        temp = line.split()
        if search == '':
            temp[0] = int(temp[0])     # 연번은 정수형으로 변환
            temp[8] = float(temp[8])     # 평점은 실수형으로 변환
            lecture_list.append(temp)
        elif temp[2].startswith(search.replace(' ', '_')):
            temp[0] = int(temp[0])     # 연번은 정수형으로 변환
            temp[8] = float(temp[8])     # 평점은 실수형으로 변환
            lecture_list.append(temp)
    file.close()

    page_len = math.ceil((len(lecture_list) - 1) / 10)
    if page_len == 0:
        page_len = 1
