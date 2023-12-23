﻿MESSAGES = {
    "start": (
        "Привет, я кот Фуражкин, "
        "могу рассказать вам про приют для животных «Преданное сердце»"
    ),
    "menu_btn": "Для возврата в главное меню нажмите кнопку",
    "menu": "Сейчас вы в меню, выберите что вы хотите узнать",
    "alert_message": (
        "Извините, это сообщение я пока не понимаю :( \n"
        "Если хотите задать мне вопрос - выберите в меню "
        'раздел "Частые вопросы"'
    ),
    "faq": "Выберите вопрос, который вас интересует:",
    "url": "Нажмите на кнопку, чтобы перейди на сайт.",
    "server_error": "Ошибка. Нажмите, чтобы сообщить администратору",
}


class ConversationTextMessage:
    COMMUNICATION_WAY = "Выберите способ общения:"
    WRITE_FULLNAME = "Пожалуйста, представьтесь. \nНапишите Имя и Фамилию."
    WRITE_EMAIL = "Приятно познакомиться!\nТеперь напишите свой e-mail."
    WRITE_PHONE = "Напишите номер своего телефона в формате +7ХХХХХХХХХХ."
    WRITE_SUBJECT = "Введите тему сообщения."
    WRITE_QUESTION = (
        "Отправьте своё сообщение.\n"
        "Соблюдайте вежливость, а не то я поцарапаю."
    )
    SEND_QUESTION_TG = (
        "Спасибо!\nВаш вопрос отправлен и будет рассмотрен в рабочее время.\n"
        "Скоро вы получите ответ, а пока посмотрите котиков."
    )
    SEND_QUESTION_EMAIL = (
        "Спасибо!\n"
        "Ваш вопрос отправлен и будет рассмотрен в ближайшее время.\n"
        "Ответ вы получите на указанный вами ящик электронной почты,\n"
        "а пока ждёте  - посмотрите котиков."
    )
    CANCEL = "Жаль, что передумали.\nВы сможете задать вопрос в любой момент."
    ANSWER_FROM_ADMIN = (
        "<b>На ваш вопрос поступил ответ от администратора:</b>\n\n"
        "%s\n\n\n"
        "<i>Пожалуйста, не отвечайте на это сообщение. Если вы хотите задать "
        "новый вопрос, выберите в меню пункт Частые вопросы.</i>"
    )
    ANSWER_BY_FAQ = "<b>Вопрос:\n</b>%s\n\n<b>Ответ:\n</b>%s"
    SERVER_ERROR = "Произошла ошибка в работе бота. Сообщите в поддержку"
    ERROR_THANKS = "Спасибо! Благодаря вам скоро мы все исправим!"


class MenuLogMessage:
    SHOW_MENU_BTN = "Показана кнопка вызова главного меню"
    SHOW_MAIN_MENU = "Показано главное меню"
    UNKNOWN_MESSAGE = "Получено необрабатываемое сообщение: %s"
    PROCESSING_BTN = "Обработка кнопки `%s`"
    STUB_BTN = "Здесь должна быть обработка кнопки %s, но её пока нет"
    CREATE_MAIN_KB = "Создана основная клавиатура"
    REMOVE_KB = "Клавиатура удалена"
    CREATE_FAQ_KB = "Создана страница №%s клавиатуры частых вопросов"
    UNKNOWN_ERROR = "Что-то пошло не так! Ошибка: %s"
    SERVER_ERROR = "Ошибка получения данных с сервера: %s"
    UPDATE_FAQ_LIST = "Список частых вопросов обновлён"
    CREATE_CUSTOM_QUESTION_KB = "Создана клавиатура нового вопроса"
    CREATE_BACK_TO_FAQ_KB = "Создана кнопка возврата к частым вопросам"


class ConversationLogMessage:
    START = "Начато общение с пользователем id:%s"
    RECEIVED_FULLNAME = "Полное имя пользователя id:%s получено"
    RECEIVED_EMAIL = "Email пользователя id:%s получен"
    RECEIVED_PHONE = "Номер телефона пользователя id:%s получен"
    RECEIVED_SUBJECT = "Тема сообщения пользователя id:%s получена"
    RECEIVED_QUESTION = "Вопрос пользователя id:%s получен"
    INVALIDATE = "Полученные данные удалены, т.к. не прошли проверку"
    SEND_QUESTION = "Вопрос пользователя id:%s отправлен администратору"
    END = "Общение с пользователем id:%s завершено"
    CANCEL = "Общение прервано пользователем id:%s"
    ANSWER_FROM_ADMIN = "Пользователю %s отправлен ответ администратора"
    ERROR_TO_ADMIN = "Сообщение об ошибке отправлено администратору"


class PlaceholderMessage:
    MENU_BTN = "Нажмите кнопку для входа в меню"
    MAIN_MENU = "Выберите пункт меню"


class InlineButtonText:
    CUSTOM_QUESTION = "Задать другой вопрос коту Фуражкину"
    FIRST_PAGE = "<<  Перв."
    LAST_PAGE = "Посл.  >>"
    PREV_PAGE = "<  Пред."
    NEXT_PAGE = "След.  >"
    TELEGRAM_QUESTION = "Telegram"
    EMAIL_QUESTION = "Email"
    BACK_TO_FAQ = "Назад к вопросам"


class SubMessageText:
    USER_DATE = "Ваши данные:"
    DONE = "Мяу, вы успешно подписаны на рассылку сообщений. Вот ваши данные:"
    ERROR = "Мррр, что-то пошло не так:\n"


class SubTextButton:
    START = "Подписаться на рассылку"
    RETURN = "Попробовать еще раз"
    CANCEL = "ОТМЕНА"
