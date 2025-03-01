import sys
import time
import math
import pygame
import openai
import backend
import collections

openai.api_key = ""

pygame.init()
screen = pygame.display.set_mode((480, 640))
pygame.display.set_caption("대화형 시간표 마법사")
giant_text = pygame.font.SysFont("arialblack", 45)
big_text = pygame.font.SysFont("malgungothic", 24)
small_text = pygame.font.SysFont("malgungothic", 16)
tiny_text = pygame.font.SysFont("malgungothic", 12)
micro_text = pygame.font.SysFont("malgungothic", 10)
sleep_time = 0.1

# 이미지 업로드 (home_page)
home_background_img = pygame.image.load(backend.dir + r'/object/home_background.jpg').convert_alpha()
login_img = pygame.image.load(backend.dir + r'/object/login.jpg').convert_alpha()
register_img = pygame.image.load(backend.dir + r'/object/register.jpg').convert_alpha()

# 이미지 업로드 (login_page & register_page)
pw_background_img = pygame.image.load(backend.dir + r'/object/pw_background.jpg').convert_alpha()

# 이미지 업로드 (main_page)
main_background_img = pygame.image.load(backend.dir + r'/object/main_background.jpg').convert_alpha()
create_img = pygame.image.load(backend.dir + r'/object/create.jpg').convert_alpha()
big_blank_tile_img = pygame.image.load(backend.dir + r'/object/big_blank_tile.jpg').convert_alpha()
big_tile_1_img = pygame.image.load(backend.dir + r'/object/big_tile_1.jpg').convert_alpha()
big_tile_2_img = pygame.image.load(backend.dir + r'/object/big_tile_2.jpg').convert_alpha()
big_tile_3_img = pygame.image.load(backend.dir + r'/object/big_tile_3.jpg').convert_alpha()
big_tile_4_img = pygame.image.load(backend.dir + r'/object/big_tile_4.jpg').convert_alpha()
big_tile_5_img = pygame.image.load(backend.dir + r'/object/big_tile_5.jpg').convert_alpha()
big_tile_6_img = pygame.image.load(backend.dir + r'/object/big_tile_6.jpg').convert_alpha()
download_img = pygame.image.load(backend.dir + r'/object/download.jpg').convert_alpha()

# 이미지 업로드 (group_page)
group_background_img = pygame.image.load(backend.dir + r'/object/group_background.jpg').convert_alpha()
generate_table_img = pygame.image.load(backend.dir + r'/object/generate_table.jpg').convert_alpha()
add_group_img = pygame.image.load(backend.dir + r'/object/add_group.jpg').convert_alpha()
group_box_img = pygame.image.load(backend.dir + r'/object/group_box.jpg').convert_alpha()
remove_group_img = pygame.image.load(backend.dir + r'/object/remove_group.jpg').convert_alpha()
add_lecture_img = pygame.image.load(backend.dir + r'/object/add_lecture.jpg').convert_alpha()

# 이미지 업로드 (lecture_page)
lecture_background_img = pygame.image.load(backend.dir + r'/object/lecture_background.jpg').convert_alpha()
save_img = pygame.image.load(backend.dir + r'/object/save.jpg').convert_alpha()
left_img = pygame.image.load(backend.dir + r'/object/left.jpg').convert_alpha()
right_img = pygame.image.load(backend.dir + r'/object/right.jpg').convert_alpha()
unchecked_img = pygame.image.load(backend.dir + r'/object/unchecked.jpg').convert_alpha()
checked_img = pygame.image.load(backend.dir + r'/object/checked.jpg').convert_alpha()
faded_checked_img = pygame.image.load(backend.dir + r'/object/faded_checked.jpg').convert_alpha()
star_img = pygame.image.load(backend.dir + r'/object/star.jpg').convert_alpha()
search_blank_img = pygame.image.load(backend.dir + r'/object/search_blank.jpg').convert_alpha()
search_img = pygame.image.load(backend.dir + r'/object/search.jpg').convert_alpha()
information_img = pygame.image.load(backend.dir + r'/object/information.jpg').convert_alpha()
info_img = pygame.image.load(backend.dir + r'/object/info.jpg').convert_alpha()
close_info_img = pygame.image.load(backend.dir + r'/object/close_info.jpg').convert_alpha()

# 이미지 업로드 (generate_page)
generate_background_img = pygame.image.load(backend.dir + r'/object/generate_background.jpg').convert_alpha()
apply_img = pygame.image.load(backend.dir + r'/object/apply.jpg').convert_alpha()
colored_left_img = pygame.image.load(backend.dir + r'/object/colored_left.jpg').convert_alpha()
colored_right_img = pygame.image.load(backend.dir + r'/object/colored_right.jpg').convert_alpha()
the_end_img = pygame.image.load(backend.dir + r'/object/the_end.jpg').convert_alpha()
return_img = pygame.image.load(backend.dir + r'/object/return.jpg').convert_alpha()
blank_tile_img = pygame.image.load(backend.dir + r'/object/blank_tile.jpg').convert_alpha()
tile_1_img = pygame.image.load(backend.dir + r'/object/tile_1.jpg').convert_alpha()
tile_2_img = pygame.image.load(backend.dir + r'/object/tile_2.jpg').convert_alpha()
tile_3_img = pygame.image.load(backend.dir + r'/object/tile_3.jpg').convert_alpha()
tile_4_img = pygame.image.load(backend.dir + r'/object/tile_4.jpg').convert_alpha()
tile_5_img = pygame.image.load(backend.dir + r'/object/tile_5.jpg').convert_alpha()
tile_6_img = pygame.image.load(backend.dir + r'/object/tile_6.jpg').convert_alpha()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.pressed = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.pressed:
                self.pressed = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.pressed = False

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


class HomePage:
    def __init__(self):
        self.background = home_background_img
        self.button_list = []
        self.button_list.append(Button(60, 350, login_img))     # 로그인 버튼 (idx = 0)
        self.button_list.append(Button(240, 350, register_img))     # 가입하기 버튼 (idx = 1)
        self.text = ''
        self.color_off = pygame.Color('lightskyblue3')
        self.color_on = pygame.Color('grey15')
        self.blank = pygame.Rect(145, 250, 250, 80)
        self.issue = None

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 8:
                    self.text += event.unicode

        screen.blit(self.background, (0, 0))
        if self.text:
            pygame.draw.rect(screen, self.color_on, self.blank, 2)
        else:
            pygame.draw.rect(screen, self.color_off, self.blank, 2)
        screen.blit(giant_text.render(self.text, True, (0, 0, 0)), (self.blank.x + 3, self.blank.y + 8))
        if self.issue == 'login':
            screen.blit(big_text.render("존재하지 않는 ID 입니다", True, (255, 80, 120)), (85, 205))
        if self.issue == 'register':
            screen.blit(big_text.render("이미 등록된 ID 입니다", True, (255, 80, 120)), (85, 205))

        next_page = None
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 로그인 버튼
                    file = open(backend.dir + r'/user_DB.txt', mode='r', encoding='UTF-8')
                    for line in file.read().strip().split('\n'):
                        temp = line.split('+')
                        if temp[0] == self.text:
                            self.issue = None
                            next_page = ('login_page', temp[0], temp[1])
                            break
                    else:
                        self.issue = 'login'
                    file.close()

                else:     # 가입하기 버튼
                    file = open(backend.dir + r'/user_DB.txt', mode='r', encoding='UTF-8')
                    for line in file.read().strip().split('\n'):
                        temp = line.split('+')
                        if temp[0] == self.text:
                            self.issue = 'register'
                            break
                    else:
                        self.issue = None
                        next_page = ('register_page', self.text)
                    file.close()

        return next_page


class LoginPage:
    def __init__(self, id, pw):
        self.background = pw_background_img
        self.button_list = []
        self.button_list.append(Button(150, 350, login_img))     # 로그인 버튼 (idx = 0)
        self.text = ''
        self.color_off = pygame.Color('lightskyblue3')
        self.color_on = pygame.Color('grey15')
        self.blank = pygame.Rect(170, 255, 230, 80)
        self.issue = False
        self.id = id
        self.pw = pw

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 8:
                    self.text += event.unicode

        screen.blit(self.background, (0, 0))
        if self.text:
            pygame.draw.rect(screen, self.color_on, self.blank, 2)
        else:
            pygame.draw.rect(screen, self.color_off, self.blank, 2)
        screen.blit(giant_text.render(self.text, True, (0, 0, 0)), (self.blank.x + 3, self.blank.y + 8))
        if self.issue:
            screen.blit(big_text.render("올바르지 않은 PW 입니다", True, (255, 80, 120)), (105, 210))

        next_page = None
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 로그인 버튼
                    if self.text == self.pw:
                        self.issue = False
                        next_page = ('main_page', self.id)
                    else:
                        self.issue = True

        return next_page


class RegisterPage:
    def __init__(self, id):
        self.background = pw_background_img
        self.button_list = []
        self.button_list.append(Button(150, 350, register_img))     # 가입하기 버튼 (idx = 0)
        self.text = ''
        self.color_off = pygame.Color('lightskyblue3')
        self.color_on = pygame.Color('grey15')
        self.blank = pygame.Rect(170, 255, 230, 80)
        self.id = id

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < 8:
                    self.text += event.unicode

        screen.blit(self.background, (0, 0))
        if self.text:
            pygame.draw.rect(screen, self.color_on, self.blank, 2)
        else:
            pygame.draw.rect(screen, self.color_off, self.blank, 2)
        screen.blit(giant_text.render(self.text, True, (0, 0, 0)), (self.blank.x + 3, self.blank.y + 8))

        next_page = None
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 가입하기 버튼
                    if self.text:
                        file = open(backend.dir + r'/user_DB.txt', mode='a', encoding='UTF-8')
                        file.write(self.id + '+' + self.text + '+' + '{}' + '\n')
                        file.close()
                        next_page = ('home_page', )

        return next_page


class MainPage:
    def __init__(self, id):
        self.background = main_background_img
        self.blank_tile = big_blank_tile_img
        self.tile = [big_tile_1_img, big_tile_2_img, big_tile_3_img, big_tile_4_img, big_tile_5_img, big_tile_6_img]
        self.button_list = []
        self.button_list.append(Button(89, 510, create_img))     # 새로운 시간표 만들기 버튼 (idx = 0)
        self.button_list.append(Button(425, 450, download_img))     # 시간표 다운받기 버튼 (idx = 1)
        self.id = id
        self.table = None

    def draw(self):
        screen.blit(self.background, (0, 0))
        screen.blit(giant_text.render(self.id, True, (0, 0, 0)), (10, 35))

        file = open(backend.dir + r'/user_DB.txt', mode='r', encoding='UTF-8')
        for line in file.read().strip().split('\n'):
            temp = line.split('+')
            if temp[0] == self.id:
                self.table = eval(temp[2])
        file.close()
        if self.table:
            screen.blit(small_text.render("MON      TUE       WED      THU       FRI", True, (0, 0, 0)), (80, 105))
            for i in range(4):
                screen.blit(small_text.render(str(9 + i).zfill(2), True, (0, 0, 0)), (42, 117 + 40 * i))
            for i in range(6):
                screen.blit(small_text.render(str(i + 1).zfill(2), True, (0, 0, 0)), (42, 277 + 40 * i))
            for i in range(5):
                for j in range(18):
                    screen.blit(self.blank_tile, (65 + 70 * i, 130 + 20 * j))
            for key, value in self.table.items():
                day = ['MON', 'TUE', 'WED', 'THU', 'FRI'].index(key)
                for sequence, time, is_start in self.table[key]:
                    screen.blit(self.tile[sequence], (65 + 70 * day, 130 + 20 * (time - 1)))
            for key, value in self.table.items():
                day = ['MON', 'TUE', 'WED', 'THU', 'FRI'].index(key)
                for sequence, time, is_start in self.table[key]:
                    if is_start:
                        screen.blit(tiny_text.render(backend.lecture_list[is_start][2][:5].replace('_', ' '), True, (0, 0, 0)), (67 + 70 * day, 132 + 20 * (time - 1)))
                        screen.blit(tiny_text.render(backend.lecture_list[is_start][6], True, (0, 0, 0)), (67 + 70 * day, 132 + 20 * time))

        next_page = None
        if self.button_list[0].draw():     # 새로운 시간표 만들기 버튼
            next_page = ('group_page', self.id)
        if self.table:
            if self.button_list[1].draw():     # 시간표 다운받기 버튼
                pygame.image.save(screen, str(self.id) + "_timetable.png")

        return next_page


class GroupPage:
    def __init__(self, id):
        self.background = group_background_img
        self.box = group_box_img
        self.button_list = []
        self.button_list.append(Button(103, 560, generate_table_img))     # 시간표 생성하기 버튼 (idx = 0)
        self.button_list.append(Button(103, 495, add_group_img))     # 그룹 추가하기 버튼 (idx = 1
        self.group_list = backend.GroupList()
        self.id = id

    def draw(self):
        screen.blit(self.background, (0, 0))
        for i in range(self.group_list.cnt):
            screen.blit(self.box, (55, 30 + i * 75))
        i = 0
        current_node = self.group_list.head
        while current_node:
            screen.blit(big_text.render(f"그룹{str(i + 1)}: 강의 {current_node.cnt}개", True, (0, 0, 0)), (65, 50 + i * 75))
            current_node = current_node.next
            i += 1

        remove = False
        next_page = None
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 시간표 생성하기 버튼
                    next_page = ('generate_page', self.id)

                elif i == 1:     # 그룹 추가하기 버튼
                    if self.group_list.cnt < 6:
                        self.group_list.add_group()
                        self.button_list.append(Button(395, 30 + (self.group_list.cnt - 1) * 75, remove_group_img))
                        self.button_list.append(Button(250, 43 + (self.group_list.cnt - 1) * 75, add_lecture_img))

                elif i % 2 == 0:     # 그룹 삭제하기 버튼
                    remove = True
                    self.group_list.remove_group(i // 2)

                else:     # 강의 추가하기 버튼
                    next_page = ('lecture_page', self.group_list.get_nth_group(i // 2))

        if remove:
            self.button_list.pop()
            self.button_list.pop()

        return next_page


class LecturePage:
    def __init__(self, current_group):
        self.background = lecture_background_img
        self.star = star_img
        self.search_blank = search_blank_img
        self.button_list = []
        self.button_list.append(Button(115, 570, save_img))     # 강의 저장 버튼 (idx = 0)
        self.button_list.append(Button(120, 520, left_img))     # 왼쪽 버튼 (idx = 1)
        self.button_list.append(Button(320, 520, right_img))     # 오른쪽 버튼 (idx = 2)
        self.button_list.append(Button(375, 25, search_img))     # 검색 버튼 (idx = 3)
        self.text = ''
        self.korean = ''
        self.current_page = 1
        self.current_group = current_group
        self.info = False     # 강의 정보 창 on/off
        self.code = None
        self.name = None
        self.grade = None
        self.category = None
        self.location = None
        self.professor = None
        self.rating = None
        self.comment = None
        self.info_background = info_img

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    if self.text:
                        self.text = self.text[:-1]
                elif event.key == pygame.K_SPACE:
                    self.text += event.unicode
                    self.text += ' '
                elif event.key == pygame.K_PERIOD:
                    self.text += event.unicode
                    self.text += '.'
                elif event.key == pygame.K_COMMA:
                    self.text += event.unicode
                    self.text += ','
                else:
                    self.text += event.unicode

                self.korean = ''
                for char in self.text:
                    if char.isnumeric() or char in (' ', '.', ',') or ord(char) > 40000:
                        self.korean += char
                self.korean = self.korean[:12]

        screen.blit(self.background, (0, 0))
        screen.blit(self.search_blank, (70, 25))
        screen.blit(big_text.render(self.korean, True, (0, 0, 0)), (76, 28))
        screen.blit(big_text.render(f"{str(self.current_page).zfill(2)}/{str(backend.page_len).zfill(2)} 페이지", True, (0, 0, 0)), (170, 522))
        screen.blit(small_text.render("학수번호   강의명             학점  교수명  강의평가", True, (27, 79, 135)), (30, 70))
        temp = (len(backend.lecture_list) - 1) - ((self.current_page - 1) * 10)
        if temp < 10:
            for i in range(temp):
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][1][:7], True, (0, 0, 0)), (30, 105 + i * 42))
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][2][:7].replace('_', ' '), True, (0, 0, 0)), (135, 105 + i * 42))
                screen.blit(small_text.render(str(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][3]), True, (0, 0, 0)), (260, 105 + i * 42))
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][7][:3], True, (0, 0, 0)), (280, 105 + i * 42))
                for n in range(math.floor(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][8])):
                    screen.blit(self.star, (340 + n * 14, 110 + i * 42))
        else:
            for i in range(10):
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][1][:7], True, (0, 0, 0)), (30, 105 + i * 42))
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][2][:7].replace('_', ' '), True, (0, 0, 0)), (135, 105 + i * 42))
                screen.blit(small_text.render(str(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][3]), True, (0, 0, 0)), (260, 105 + i * 42))
                screen.blit(small_text.render(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][7][:3], True, (0, 0, 0)), (280, 105 + i * 42))
                for n in range(math.floor(backend.lecture_list[(self.current_page - 1) * 10 + i + 1][8])):
                    screen.blit(self.star, (340 + n * 14, 110 + i * 42))

        if temp < 10:
            for i in range(temp):
                if backend.selected[backend.lecture_list[(self.current_page - 1) * 10 + i + 1][0]] is None:
                    self.button_list.append(Button(420, 100 + i * 42, unchecked_img))
                elif backend.selected[backend.lecture_list[(self.current_page - 1) * 10 + i + 1][0]] == self.current_group.code:
                    self.button_list.append(Button(420, 100 + i * 42, checked_img))
                else:
                    self.button_list.append(Button(420, 100 + i * 42, faded_checked_img))
        else:
            for i in range(10):
                if backend.selected[backend.lecture_list[(self.current_page - 1) * 10 + i + 1][0]] is None:
                    self.button_list.append(Button(420, 100 + i * 42, unchecked_img))
                elif backend.selected[backend.lecture_list[(self.current_page - 1) * 10 + i + 1][0]] == self.current_group.code:
                    self.button_list.append(Button(420, 100 + i * 42, checked_img))
                else:
                    self.button_list.append(Button(420, 100 + i * 42, faded_checked_img))

        if self.info:
            screen.blit(self.info_background, (75, 150))
            self.button_list.append(Button(375, 150, close_info_img))
            screen.blit(big_text.render(self.name.replace('_', ' '), True, (0, 0, 0)), (90, 220))
            screen.blit(small_text.render(self.code, True, (0, 0, 0)), (90, 255))
            screen.blit(small_text.render(self.grade + "학점", True, (0, 0, 0)), (210, 255))
            screen.blit(small_text.render(self.category, True, (0, 0, 0)), (270, 255))
            screen.blit(small_text.render("- 교수명 : " + self.professor.replace(',', ', '), True, (0, 0, 0)), (90, 295))
            screen.blit(small_text.render("- 장소 : " + self.location.replace(',', ', '), True, (0, 0, 0)), (90, 320))
            screen.blit(small_text.render("- 강의평가 : " + self.rating + " / 5.0", True, (0, 0, 0)), (90, 345))
            screen.blit(small_text.render("강의 한줄평", True, (0, 0, 0)), (90, 385))
            screen.blit(tiny_text.render(self.comment.replace('_', ' ')[:28], True, (0, 0, 0)), (90, 410))
            screen.blit(tiny_text.render(self.comment.replace('_', ' ')[28:], True, (0, 0, 0)), (90, 430))
        else:
            if temp < 10:
                for i in range(temp):
                    self.button_list.append(Button(108, 106 + i * 42, information_img))
            else:
                for i in range(10):
                    self.button_list.append(Button(108, 106 + i * 42, information_img))

        next_page = None
        change = False
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 강의 저장 버튼
                    backend.update_lecture_DB('')
                    self.current_group.sort()
                    next_page = ('group_page', )

                elif i == 1:     # 왼쪽 버튼
                    if self.current_page > 1:
                        self.current_page -= 1

                elif i == 2:     # 오른쪽 버튼
                    if self.current_page < backend.page_len:
                        self.current_page += 1

                elif i == 3:     # 검색 버튼
                    backend.update_lecture_DB(self.korean.strip())
                    self.text = ''
                    self.korean = ''
                    self.current_page = 1

                elif i == len(self.button_list) - 1 and self.info:     # 강의 정보 닫기 버튼
                    self.info = False
                    change = True

                else:
                    if temp < 10:
                        if i < 4 + temp:
                            if backend.selected[backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0]] is None:
                                self.current_group.add_lecture(backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0])
                            elif backend.selected[backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0]] == self.current_group.code:
                                self.current_group.remove_lecture(backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0])
                            time.sleep(sleep_time)

                        else:
                            self.info = True
                            copy = backend.lecture_list[i - 3 - temp + (self.current_page - 1) * 10][:]
                            self.code = copy[1]
                            self.name = copy[2]
                            self.grade = copy[3]
                            self.category = copy[4]
                            self.location = copy[6]
                            self.professor = copy[7]
                            self.rating = str(copy[8])
                            self.comment = copy[9]
                            change = True

                    else:
                        if i < 14:
                            if backend.selected[backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0]] is None:
                                self.current_group.add_lecture(backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0])
                            elif backend.selected[backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0]] == self.current_group.code:
                                self.current_group.remove_lecture(backend.lecture_list[i - 3 + (self.current_page - 1) * 10][0])
                            time.sleep(sleep_time)

                        else:     # 강의 정보 버튼
                            self.info = True
                            copy = backend.lecture_list[i - 13 + (self.current_page - 1) * 10][:]
                            self.code = copy[1]
                            self.name = copy[2]
                            self.grade = copy[3]
                            self.category = copy[4]
                            self.location = copy[6]
                            self.professor = copy[7]
                            self.rating = str(copy[8])
                            self.comment = copy[9]
                            change = True

        if self.info == change:
            if temp < 10:
                for _ in range(temp * 2):
                    self.button_list.pop()
            else:
                for _ in range(20):
                    self.button_list.pop()
        else:
            self.button_list.pop()
            if temp < 10:
                for _ in range(temp):
                    self.button_list.pop()
            else:
                for _ in range(10):
                    self.button_list.pop()

        return next_page


class GeneratePage:
    def __init__(self, head, id):
        self.background = generate_background_img
        self.blank_tile = blank_tile_img
        self.tile = [tile_1_img, tile_2_img, tile_3_img, tile_4_img, tile_5_img, tile_6_img]
        self.button_list = []
        self.button_list.append(Button(115, 585, apply_img))     # 조건 적용하기 버튼 (idx = 0)
        self.button_list.append(Button(95, 295, colored_left_img))     # 왼쪽 버튼 (idx = 1)
        self.button_list.append(Button(345, 295, colored_right_img))     # 오른쪽 버튼 (idx = 2)
        self.button_list.append(Button(167, 335, the_end_img))     # 저장하기 버튼 (idx = 3)
        self.button_list.append(Button(5, 20, return_img))     # 이전 화면으로 돌아가기 버튼 (idx = 4)
        self.id = id
        self.text = ''
        self.korean = ['']
        self.messages = []
        self.current_page = 1
        self.current_table = collections.defaultdict(list)
        backend.generated_list = []
        backend.recursion(head)
        if not backend.generated_list:
            backend.generated_list.append([])
        if backend.generated_list:
            for sequence, lecture in enumerate(backend.generated_list[0]):
                temp = backend.lecture_list[lecture][5].split(',')
                day = None
                for thing in temp:
                    if thing.isnumeric():
                        self.current_table[backend.day_dictionary[day]].append((sequence, int(thing), None))
                    else:
                        day = thing[0]
                        self.current_table[backend.day_dictionary[day]].append((sequence, int(thing[1:]), lecture))

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass
                elif event.key == pygame.K_BACKSPACE:
                    if self.text:
                        self.text = self.text[:-1]
                elif event.key == pygame.K_SPACE:
                    self.text += event.unicode
                    self.text += ' '
                elif event.key == pygame.K_PERIOD:
                    self.text += event.unicode
                    self.text += '.'
                elif event.key == pygame.K_COMMA:
                    self.text += event.unicode
                    self.text += ','
                else:
                    self.text += event.unicode

                self.korean = ['']
                for char in self.text:
                    if char.isnumeric() or char in (' ', '.', ',') or ord(char) > 40000:
                        if len(self.korean) == 2 and len(self.korean[-1]) == 25:     # 한 줄의 글자 수 제한
                            break
                        if len(self.korean) == 1 and len(self.korean[-1]) == 25:     # 한 줄의 글자 수 제한
                            self.korean.append('')
                        self.korean[-1] += char

        screen.blit(self.background, (0, 0))
        screen.blit(big_text.render(f"{str(self.current_page).zfill(4)}/{str(len(backend.generated_list)).zfill(4)} 페이지", True, (0, 0, 0)), (143, 297))
        screen.blit(tiny_text.render("MON      TUE       WED      THU        FRI", True, (0, 0, 0)), (125, 20))
        for i in range(4):
            screen.blit(tiny_text.render(str(9 + i).zfill(2), True, (0, 0, 0)), (95, 29 + 28 * i))
        for i in range(6):
            screen.blit(tiny_text.render(str(i + 1).zfill(2), True, (0, 0, 0)), (95, 141 + 28 * i))
        for i in range(5):
            for j in range(18):
                screen.blit(self.blank_tile, (114 + 50 * i, 38 + 14 * j))
        for key, value in self.current_table.items():
            day = ['MON', 'TUE', 'WED', 'THU', 'FRI'].index(key)
            for sequence, time, is_start in self.current_table[key]:
                screen.blit(self.tile[sequence], (114 + 50 * day, 38 + 14 * (time - 1)))
        for key, value in self.current_table.items():
            day = ['MON', 'TUE', 'WED', 'THU', 'FRI'].index(key)
            for sequence, time, is_start in self.current_table[key]:
                if is_start:
                    screen.blit(micro_text.render(backend.lecture_list[is_start][2][:5].replace('_', ' '), True, (0, 0, 0)), (114 + 50 * day, 38 + 14 * (time - 1)))
                    screen.blit(micro_text.render(backend.lecture_list[is_start][6], True, (0, 0, 0)), (114 + 50 * day, 38 + 14 * time))
        for i, text in enumerate(self.korean):
            screen.blit(small_text.render(text, True, (0, 0, 0)), (65, 510 + i * 28))

        next_page = None
        for i, button in enumerate(self.button_list):
            if button.draw():
                if i == 0:     # 조건 적용하기 버튼
                    temp = ''
                    for thing in self.korean:
                        temp += thing

                    if temp:
                        self.text = ''
                        self.korean = ['']

                        user_content = '''
                        'MORNING' variable exists, which can be both positive int or a list.
                        월, 화, 수, 목, 금 correspond to MON, TUE, WED, THU, FRI respectively.
                        'MORNING' variable is about first class in the morning.
                        If someone says, "월요일 1교시를 제거해주세요" or "월요일 아침 수업을 빼주세요",
                        you should return the following one-line Python code: MORNING = ['MON'].
                        If you get a request like "1교시 3개까지 허용할게요" or "1교시는 세개 까지가 좋겠습니다",
                        you should return the following one-line Python code: MORNING = 3.
                        
                        'FREE' variable exists, which is a list and represents the days without classes.
                        If someone says, "수요일이 공강이면 좋겠습니다" or "수요일 수업을 전부 빼주세요,
                        you should return the following one-line Python code: FREE = ['WED'].

                        'CONTINUE' variable exists, which is a positive integer and represents the hours of consecutive classes.
                        If someone says, "연강은 4시간 까지 가능합니다" or "수업은 연속해서 4시간 까지",
                        you should return the following one-line Python code: CONTINUE = 4.

                        Now, provide the appropriate one-line Python code for the following situation: "''' + temp

                        self.messages.append({"role": "user", "content": user_content})
                        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
                        assistant_content = completion.choices[0].message["content"].strip()
                        self.messages.append({"role": "assistant", "content": assistant_content})
                        assistant_content = assistant_content.rstrip('.')
                        print(assistant_content)

                        MORNING = None
                        FREE = None
                        CONTINUE = None
                        if assistant_content.startswith('MORNING'):
                            MORNING = eval(assistant_content.split(' = ')[1])
                        if assistant_content.startswith('FREE'):
                            FREE = eval(assistant_content.split(' = ')[1])
                        if assistant_content.startswith('CONTINUE'):
                            CONTINUE = eval(assistant_content.split(' = ')[1])

                        backend.generated_list = backend.filter_table(MORNING, FREE, CONTINUE)[:]
                        if not backend.generated_list:
                            backend.generated_list.append([])
                        self.current_page = 1
                        self.current_table = collections.defaultdict(list)
                        if backend.generated_list:
                            for sequence, lecture in enumerate(backend.generated_list[0]):
                                temp = backend.lecture_list[lecture][5].split(',')
                                day = None
                                for thing in temp:
                                    if thing.isnumeric():
                                        self.current_table[backend.day_dictionary[day]].append((sequence, int(thing), None))
                                    else:
                                        day = thing[0]
                                        self.current_table[backend.day_dictionary[day]].append((sequence, int(thing[1:]), lecture))

                elif i == 1:     # 왼쪽 버튼
                    if self.current_page > 1:
                        self.current_page -= 1
                        self.current_table = collections.defaultdict(list)
                        for sequence, lecture in enumerate(backend.generated_list[self.current_page - 1]):
                            temp = backend.lecture_list[lecture][5].split(',')
                            day = None
                            for thing in temp:
                                if thing.isnumeric():
                                    self.current_table[backend.day_dictionary[day]].append((sequence, int(thing), None))
                                else:
                                    day = thing[0]
                                    self.current_table[backend.day_dictionary[day]].append((sequence, int(thing[1:]), lecture))

                elif i == 2:     # 오른쪽 버튼
                    if self.current_page < len(backend.generated_list):
                        self.current_page += 1
                        self.current_table = collections.defaultdict(list)
                        for sequence, lecture in enumerate(backend.generated_list[self.current_page - 1]):
                            temp = backend.lecture_list[lecture][5].split(',')
                            day = None
                            for thing in temp:
                                if thing.isnumeric():
                                    self.current_table[backend.day_dictionary[day]].append((sequence, int(thing), None))
                                else:
                                    day = thing[0]
                                    self.current_table[backend.day_dictionary[day]].append((sequence, int(thing[1:]), lecture))

                elif i == 3:     # 저장하기 버튼
                    if self.current_table:
                        backend.selected = [None] * len(backend.lecture_list)

                        copy = []
                        file = open(backend.dir + r'/user_DB.txt', mode='r', encoding='UTF-8')
                        for line in file.read().strip().split('\n'):
                            temp = line.split('+')
                            copy.append(temp)
                        file.close()

                        file = open(backend.dir + r'/user_DB.txt', mode='w', encoding='UTF-8')
                        for id, pw, table in copy:
                            if id == self.id:
                                file.write(id + '+' + pw + '+' + str(self.current_table)[28:-1] + '\n')
                            else:
                                file.write(id + '+' + pw + '+' + table + '\n')
                        file.close()

                        next_page = ('main_page', )

                else:     # 이전 화면으로 돌아가기 버튼
                    next_page = ('group_page', )

        return next_page
