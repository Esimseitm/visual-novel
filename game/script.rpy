# Персонажи
define th = Character("Thomas", color="#66BB6A")
define cap = Character("Captain Himmelshtos", color="#EF5350")
define name = Character("Hero", color="#FFCA28")

# music and sounds
define sound_napadenie = "music/napadenie.mp3"
define sound_artileriya = "music/artileriya.mp3"
define main_music = "music/mainmusic.mp3"

# Изображения background
image bg_okop = "images/war-okop.jpg"
image bg_village_base = "images/war-derevnya-base.jpg"
image bg_village_ruins = "images/war-derevnya-ruins.jpg"
image bg_village_ruins2 = "images/war-derevnya-ruins2.jpg"
image bf_mass_grave = "images/mass-grave.jpg"

# Изображения персонажей
image th base ="images/thomas.png"
image cap base ="images/captain.png"

# Переменные
default artillery_success = True
default final_boolean = True
default counter = 3

$ renpy.music.set_volume(0.2, channel="music")  # 

init python:
    all_cards = ['A', 'B', 'C']
    # ширина и высота поля
    ww = 3
    hh = 3
    max_c = 2
    card_size = 48
    # время, выделенное на прохождение
    max_time = 25
    wait = 0.5
    img_mode = True
    values_list = []
    temp = []
    for fn in renpy.list_files():
        if fn.startswith("images/card_") and fn.endswith((".png")):
            name = fn[12:-4]
            renpy.image("card " + name, fn)
            if name != "empty" and name != "back":
                temp.append(str(name))
    if len(temp) > 1:
        all_cards = temp
    else:
        img_mode = False
    def cards_init():
        global values_list
        values_list = []
        while len(values_list) + max_c <= ww * hh:
            current_card = renpy.random.choice(all_cards)
            for i in range(0, max_c):
                values_list.append(current_card)
        renpy.random.shuffle(values_list)
        while len(values_list) < ww * hh:
            values_list.append('empty')

screen memo_scr:
    timer 1.0 action If (memo_timer > 1, SetVariable("memo_timer", memo_timer - 1), Jump("check_arta") ) repeat True
    grid ww hh:
        align (.5, .5)
        for card in cards_list:
            button:
                left_padding 0
                right_padding 0
                top_padding 0
                bottom_padding 0
                background None
                if card["c_value"] == 'empty':
                    if img_mode:
                        add "card empty"
                    else:
                        text " " size card_size
                else:
                    if card["c_chosen"]:
                        if img_mode:
                            add "card " + card["c_value"]
                        else:
                            text card["c_value"] size card_size
                    else:
                        if img_mode:
                            add "card back"
                        else:
                            text "#" size card_size
                action If ( (card["c_chosen"] or not can_click), None, [SetDict(cards_list[card["c_number"]], "c_chosen", True), Return(card["c_number"]) ] )
    text str(memo_timer) xalign .5 yalign 0.0 size card_size

label find_tank_game:
    $ cards_init()
    $ cards_list = []
    python:
        for i in range (0, len(values_list) ):
            if values_list[i] == 'empty':
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":True} )   
            else:
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":False} )   
    $ memo_timer = max_time
    show screen memo_scr
    label memo_game_loop:
        $ can_click = True
        $ turned_cards_numbers = []
        $ turned_cards_values = []
        $ turns_left = max_c
        label turns_loop:
            if turns_left > 0:
                $ result = ui.interact()
                $ memo_timer = memo_timer
                $ turned_cards_numbers.append (cards_list[result]["c_number"])
                $ turned_cards_values.append (cards_list[result]["c_value"])
                $ turns_left -= 1
                jump turns_loop
        $ can_click = False
        if turned_cards_values.count(turned_cards_values[0]) != len(turned_cards_values):
            $ renpy.pause (wait, hard = True)
            python:
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_chosen"] = False
        else:
            $ renpy.pause (wait, hard = True)
            python: 
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_value"] = 'empty'
                for j in cards_list:
                    if j["c_chosen"] == False:
                        renpy.jump ("memo_game_loop")
                counter = 5
                renpy.jump ("check_arta")
        jump memo_game_loop

label start:
    play music main_music loop
    scene bg_okop 
    with fade
    show cap base at left
    with dissolve
    cap "Приветсвуя тебя солдат. А тебя что, не учили как следует обращаться старшему по званию?"
    "Вам следует представиться перед Капитаном Химелштосом"
    python:
        name = renpy.input("Как вас зовут?")
        name = name.strip() or "Манарбек"
    name "Капитан Химмелштос, младший сержант [name] прибыл в ваше подчинение."
    cap "Вот так.А ты что шлем не одел, а ну быстро привести себя в порядок. Тут ведь настоящее поле боя"
    cap "Мне доложили что должен был прибыть инженер-топографист. Это получается мы тебя ждем чтоли"
    cap "Да уж, уже совсем необученных отправляют на фронт... Что твориться\n
    Хорошо, ситуация такова, мы сейчас пытаемся войти в поселок Далекое и укрепить позиции\n"
    cap "Но враг хорошо укрепился, единственная дорога войти в деревню эта вот та прямая дорога. По всем остальным фронтам все заминирировано.\n"
    cap "Но нам не удается успешно штурмовать, все наши солдаты погибают при штурме, пока у врага хорошие позиции"
    show th base at right 
    with dissolve
    cap "Тебе нужно подобраться по ближе и составить карту обстрела. Мой солдат - Томас объяснит тебе что делать."
    cap "А нет, лучше Томас пойдет с тобой, он знает путь чтобы не подорваться на мине. Одного топографиста мы уже потеряли, второго потерять я не могу."
    hide cap base 
    with fade
    th "Держи планшет прибора ПУАО. После того как я доставлю тебя, ты будешь вбивать координаты врага в систему планшета ПУАО. Затем наша артиллерия нанесет удар по врагу согласно твоим обозначениям на планшете."
    th "Твоей задачей будет сопоставить вражеские танковые позиции на карте планшета ПУАО. Помимо этого нужно также сопоставить координаты других мирных объектов\n
    чтобы наша артилерия не ударила по мирным людям"
    th "Мы все таки не убиваем мирный народ"
    scene bg_village_base
    $ max_time = 30
    $ ww, hh = 4, 4
    call find_tank_game from _call_find_tank_game
    with fade
    return

label check_arta:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    scene bg_village_base
    hide bg_village_base
    scene bg_okop 
    show cap base at left
    show th base at right 
    th "Капитан Химельштос, мы ввели координаты. Можно начать обстрел врага с артилерии"
    cap "Не зря тебя сюда отправили [name], вот и пригодился солдат"
    cap "Артилерия огонь! Приказываю огонь со всех орудий!"
    play sound sound_artileriya
    $ renpy.pause(2, hard=True)
    $ renpy.music.stop(channel="sound", fadeout=1.0)
    cap "А теперь , когда наша артиллерия ударила по врагу, пора захватить это проклятую позицию"
    hide cap base
    hide th base 
    play sound sound_napadenie
    $ renpy.pause(2, hard=True)
    $ renpy.music.stop(channel="sound", fadeout=1.0)
    if counter > 3:
        jump successful_mission
    else:
        jump failed_mission

label successful_mission:
    scene bg_village_ruins2
    show cap base at left
    cap "Так держать. [name], все таки не зря тебя отправили сюда. Благодаря вам мы смогли без больших потерь войти в деревню."
    jump second_mission

label failed_mission:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    centered "{size=36}К сожалению вы вместе с отрядом погибли при наступлении на деревню.\n Вам следует заново пройти мини-игру со сверкой координат{/size}"
    scene bg_village_base
    jump find_tank_game

label second_mission:
    scene bg_village_ruins 
    with fade
    show cap base at left
    with dissolve
    cap "Только что ген-штаб доложил, что враг будет наступать с новыми силами. Видимо они не собирается просто так отдать эту деревню."
    cap "Так что теперь занимайте позиции, укрепляйте рубежы, за сегодня это еще не последняя битва за эту деревню. Мы ожидаем подкрепление, но когда она придет..\n"
    hide cap base
    show th base at right
    with dissolve
    th "Знаешт [name] , если до утра не подойдет 120 дивизия. Чую мы тут останемся\n
    Я готов сражаться за эту проклятую деревню. Но какой смысл. Мы уже итак потеряли половину войск пока захватили эту деревню."
    th "Все прекрасно понимают что 120 дивизия подойдет только на следующий день. Но какой смысл. Если завтра от нас уже ничего не останется"
    name "Что ты предлагаешь? Бежать? Укрыться где-то?"
    th "Знаешь [name], я всю жизнь думал что готов отдать жизнь за свою страну. Но в такие моменты, я думаю о том, что жизнь она единственная\n
    И если сегодня погибнуть, то жизнь прекратиться"
    th "Но есть одна мысль , что дает мне смысл остаться здесь и погибнуть вместе с моими братьями"
    name "Мысль? Ты о чем?"
    th "Я о том, что хоть мы и погибнем, память о нас не погибнет. Она будет жить в сердцах наших потомков."
    th "Так что, ты с нами [name], готов умереть героем?"
    hide th base
    menu:
        "Бежать с поле боя, сохранив свою жизнь":
            $ final_boolean = False
            jump final
            hide scene bg_village_ruins 

        "Погибнуть в бою героем":
            $ final_boolean = True
            jump final
            hide scene bg_village_ruins 

screen text_as_image(text_to_display):
    text text_to_display:
        xalign 0.56
        yalign 0.5
        size 30
        color "#343843" 
        outlines [(2, "#000000")]

label final:
    stop music fadeout 1
    centered "{size=36}Все кто защищал деревню Далекое погибли в тот день и были похоронены в братской могиле.{/size}"
    with dissolve
    centered "{size=36}Да, был проигран бой, но не война!{/size}"
    with dissolve
    centered "{size=36}Спустя 75 лет{/size}"
    with dissolve
    scene bf_mass_grave
    with fade
    if final_boolean == True:
        $ name_of_heroes="Сержант Дерек\n капрал Андерсон\n Капитан Химмельштос\n Старший сержант Томас\n Младший сержант [name]\n"
    else:
        $ name_of_heroes="Сержант Дерек\n Капрал Андерсон\n Капитан Химмельштос\n Старший сержант Томас\n"
    show screen text_as_image(name_of_heroes)
    with dissolve
    "Так дети. А сейчас мы с вами находимся на братской могиле солдат. Что храбро погибли сражаясь с врагом\n
    Вы всегда должны помнить о том поколении что отдало жизнь за будущее своего поколения. а именно за вас.\n"
    "Пока память о них не умрет в наших сердцах, память о героех будет жить"
    hide bf_mass_grave
    hide screen text_as_image
    return 0