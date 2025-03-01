import sys
import time
import pygame
import frontend


def exit_condition():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


flag = False

home_page = frontend.HomePage()
while True:
    next_page = home_page.draw()     # exit_condition 포함
    if next_page:
        time.sleep(frontend.sleep_time)

        if next_page[0] == "login_page":
            loging_page = frontend.LoginPage(next_page[1], next_page[2])
            while True:
                next_page = loging_page.draw()     # exit_condition 포함
                if next_page:
                    time.sleep(frontend.sleep_time)

                    if next_page[0] == "main_page":
                        main_page = frontend.MainPage(next_page[1])
                        while True:
                            exit_condition()
                            next_page = main_page.draw()
                            if next_page:
                                time.sleep(frontend.sleep_time)

                                if next_page[0] == "group_page":
                                    group_page = frontend.GroupPage(next_page[1])
                                    while True:
                                        exit_condition()
                                        next_page = group_page.draw()
                                        if next_page:
                                            time.sleep(frontend.sleep_time)

                                            if next_page[0] == "lecture_page":
                                                lecture_page = frontend.LecturePage(next_page[1])
                                                while True:
                                                    next_page = lecture_page.draw()     # exit_condition 포함
                                                    if next_page:
                                                        time.sleep(frontend.sleep_time)

                                                        if next_page[0] == "group_page":
                                                            break

                                                    pygame.display.update()

                                            elif next_page[0] == "generate_page":
                                                generate_page = frontend.GeneratePage(group_page.group_list.head, next_page[1])
                                                while True:
                                                    next_page = generate_page.draw()     # exit_condition 포함
                                                    if next_page:
                                                        time.sleep(frontend.sleep_time)

                                                        if next_page[0] == "main_page":
                                                            flag = True
                                                            break

                                                        elif next_page[0] == "group_page":
                                                            break

                                                    pygame.display.update()

                                        if flag:
                                            break
                                        pygame.display.update()

                            flag = False
                            pygame.display.update()

                pygame.display.update()

        elif next_page[0] == "register_page":
            register_page = frontend.RegisterPage(next_page[1])
            while True:
                next_page = register_page.draw()     # exit_condition 포함
                if next_page:
                    time.sleep(frontend.sleep_time)

                    if next_page[0] == "home_page":
                        home_page.text = ''
                        break

                pygame.display.update()

    pygame.display.update()
