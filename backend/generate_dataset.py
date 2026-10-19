"""
Script to generate the comprehensive benchmark dataset of 150+ Kazakhstan fraud and legitimate cases.
Cases cover Russian and Kazakh languages across all primary social engineering schemes active in Kazakhstan.
"""

import json
import os

CASES = [
    # ==========================================
    # 1. SAFE ACCOUNT / BANK SECURITY IMPERSONATION (20 cases)
    # ==========================================
    {
        "id": 1,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Здравствуйте! Это старший специалист службы безопасности Национального банка. На ваше имя прямо сейчас оформляют кредит на 2 500 000 тенге. Срочно переведите деньги на безопасный резервный счёт!"
    },
    {
        "id": 2,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Сәлеметсіз бе! Бұл Ұлттық банктің қауіпсіздік қызметі. Сіздің атыңызға 2 500 000 теңге несие рәсімделуде. Ақшаны тез арада қауіпсіз шотқа аударыңыз!"
    },
    {
        "id": 3,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Капитан полиции Департамента полиции г. Астана. Зафиксирована утечка персональных данных из Kaspi Bank. Чтобы не допустить хищения, переведите остаток на защищённый счёт Нацбанка."
    },
    {
        "id": 4,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Астана қалалық полиция департаментінен хабарласып тұрмыз. Банк қызметкерлері сіздің шотыңыздан ақша шешуге тырысуда. Дереу қауіпсіз резервтік шотқа ақша аударыңыз!"
    },
    {
        "id": 5,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Внимание! На ваше имя одобрен встречный зеркальный кредит в Halyk Bank. Для аннулирования мошеннической заявки срочно переведите средства на наш единый защищённый счёт."
    },
    {
        "id": 6,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Назар аударыңыз! Сіздің атыңызға онлайн несие өтініші берілді. Бұғаттау үшін барлық қаражатты резервтік қауіпсіз шотқа аударыңыз, бұл мемлекеттік қорғаныс."
    },
    {
        "id": 7,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Служба финансового мониторинга Республики Казахстан. Ваш счёт скомпрометирован. Немедленно переведите деньги на безопасный транзитный счёт, иначе они будут заморожены."
    },
    {
        "id": 8,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Қаржылық мониторинг агенттігі. Картаңызда күдікті операция байқалды. Шот бұғатталмас үшін тез арада қорғалған қауіпсіз шотқа аударыңыз."
    },
    {
        "id": 9,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Это майор Генеральной прокуратуры. Против вас ведутся мошеннические действия сотрудниками банка. Никому не говорите, строго секретно, переведите сбережения на защищённый счёт."
    },
    {
        "id": 10,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Бас прокуратураның тергеушісі. Банк менеджерлері сіздің атыңыздан несие алуда. Ешкімге айтпаңыз, барлық ақшаны қауіпсіз шотқа жіберіңіз."
    },
    {
        "id": 11,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Служба безопасности ForteBank. Ваша карточка подверглась атаке. Срочно переведите баланс на временный безопасный счёт для перевыпуска."
    },
    {
        "id": 12,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "ForteBank қауіпсіздік қызметі. Сіздің картаңызға шабуыл жасалды. Тез арада қауіпсіз шотқа ақша аударыңыз, әйтпесе бұғатталады."
    },
    {
        "id": 13,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Центральный аппарат Нацбанка РК. Обнаружена заявка на перевод 3 000 000 тг третьим лицам. Требуется зеркальный кредит и перевод на безопасный счёт."
    },
    {
        "id": 14,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "ҚР Ұлттық банкі. 3 миллион теңгеге бөгде аударым жасалуда. Тоқтату үшін резервтік қауіпсіз шотқа аударыңыз."
    },
    {
        "id": 15,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Вам звонит старший дознаватель МВД. На вас оформляют заем в МФО. Продиктуйте данные и переведите средства на защищенный счёт следственного комитета."
    },
    {
        "id": 16,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "ІІМ тергеушісімін. Микроқаржы ұйымынан сіздің атыңызға несие рәсімделуде. Тез арада қауіпсіз шотқа ақша аударыңыз."
    },
    {
        "id": 17,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "СБ Банка ЦентрКредит: обнаружен несанкционированный доступ из другого города. Срочно скиньте средства на безопасный счёт, пока банк не заморозил транзакции."
    },
    {
        "id": 18,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Банк ЦентрКредит қауіпсіздігі: басқа қаладан кіру анықталды. Тез арада қаражатты қауіпсіз шотқа аударыңыз."
    },
    {
        "id": 19,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Единый колл-центр кибербезопасности РК. Подтвердите отмену кредита переводом суммы на безопасный счёт национального казначейства."
    },
    {
        "id": 20,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "safe_account",
        "text": "Киберқауіпсіздік орталығы. Несиені бұғаттау үшін ақшаны мемлекеттік қауіпсіз шотқа аударыңыз."
    },

    # ==========================================
    # 2. KRISHA.KZ FAKE RENT (18 cases)
    # ==========================================
    {
        "id": 21,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Квартира свободна, 2 комнаты в центре за 140 000 тг. Я сейчас за границей, показать лично не могу. Скиньте залог 50 000 на карту Каспи, и я отправлю ключи курьером."
    },
    {
        "id": 22,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Пәтер бос, 2 бөлме 140 000 тг. Мен қазір шетелдемін, көрсете алмаймын. Кепіл ретінде 50 000 аударыңыз, кілтті курьермен жіберемін."
    },
    {
        "id": 23,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Здравствуйте по поводу аренды на Крыше. Я сам в командировке в Атырау, без просмотра отдаю только серьезным. Скиньте задаток 30 000 тенге прямо сейчас, иначе сдам другим."
    },
    {
        "id": 24,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Сәлеметсіз бе, Krisha бойынша. Мен Атырауда іссапардамын, пәтерді көрмей тек кепіл беретіндерге тапсырамын. 30 000 тг алдын ала аударыңыз."
    },
    {
        "id": 25,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Сдается 1-комнатная на левом берегу за 110 тыс. Хозяева в отъезде за границей. Отправьте аванс 40000 тг на Каспи Голд для брони, договор вышлю на Ватсап."
    },
    {
        "id": 26,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Сол жағалауда 1 бөлме 110 мыңға беріледі. Иелері шетелде. Брондау үшін Каспиге 40 000 тг аванс аударыңыз, келісімшартты WhatsApp-қа саламын."
    },
    {
        "id": 27,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Показов сегодня нет, я в другом городе. Если хотите заехать завтра, переведите предоплату 50 000 тг за бронь."
    },
    {
        "id": 28,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Бүгін көру мүмкін емес, мен басқа қаладамын. Ертең кіру үшін 50 000 тг алдын ала төлем жасап қойыңыз."
    },
    {
        "id": 29,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Срочная аренда квартиры. Сам за границей, приеду через месяц. Переведите 60 000 залог на Kaspi, ключи у консьержа."
    },
    {
        "id": 30,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Шұғыл пәтер жалданады. Өзім шетелдемін, бір айдан кейін келемін. Каспиге 60 000 тг кепіл аударыңыз, кілтті консьержден аласыз."
    },
    {
        "id": 31,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Квартира в Алматы, Медео район. Я в отъезде, без личной встречи. Закиньте задаток 45000 на карту, чтобы объявление снял."
    },
    {
        "id": 32,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Алматыдағы пәтер. Сапарда жүрмін, көрмей алатындарға беремін. Хабарландыруды өшіру үшін 45 000 тг кепіл жіберіңіз."
    },
    {
        "id": 33,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Krisha.kz объявление #48921. Хозяин за границей. Переведите залог 70 000 тг на Каспи, курьер привезет ключи через час."
    },
    {
        "id": 34,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Krisha.kz хабарландыруы. Пәтер иесі шетелде. 70 000 тг кепіл аударыңыз, курьер кілтті бір сағатта жеткізеді."
    },
    {
        "id": 35,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Желающих много, бронирую только после залога 35 000 тг. Сам показать не могу, ключи передам после перевода."
    },
    {
        "id": 36,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "krisha_rent",
        "text": "Адам көп сұрап жатыр, тек 35 000 тг кепіл төлегенге қалдырамын. Көрсете алмаймын, ақша аударған соң кілтті беремін."
    },
    {
        "id": 37,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Сдам коттедж на выходные в Боровом. Я за границей. Переведите задаток 100 000 на карту Халык, бронь поставлю."
    },
    {
        "id": 38,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "krisha_rent",
        "text": "Бурабайда демалысқа коттедж. Шетелде жүрмін. Халық картасына 100 000 тг кепіл аударыңыз, бронь жасаймын."
    },

    # ==========================================
    # 3. DROPPER CARDS / MONEY MULE (18 cases)
    # ==========================================
    {
        "id": 39,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Сдай карту в аренду и получай 40 000 тенге в день! Нужно просто пропустить переводы через твой Каспи кошелек."
    },
    {
        "id": 40,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Картаңызды жалға беріп, күніне 40 000 тг алыңыз! Карта арқылы аударымдарды өткізіп жіберсеңіз болды."
    },
    {
        "id": 41,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Ищу дропперов в Астане и Алматы! Оплата до 80 000 тг за смену. Ваша карта Kaspi Gold или Halyk, вывод криптовалюты P2P."
    },
    {
        "id": 42,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Астана мен Алматыда дропперлер қажет! Ауысымына 80 000 тг төлейміз. Сіздің Каспи немесе Халық картаңызға аударымдар келеді."
    },
    {
        "id": 43,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Срочно требуются люди, готовые сдать карту в аренду. Деньги чистые, криптообменник. Даем процент от каждого перевода."
    },
    {
        "id": 44,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Картасын жалға беретін сенімді адамдар керек. Крипто-обменник, заңды ақша. Әр аударымнан пайыз береміз."
    },
    {
        "id": 45,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Легкий заработок студентам! Сдай карту Kaspi, получи 50000 сразу. Нужно просто обналичить переводы в банкомате."
    },
    {
        "id": 46,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Студенттерге оңай табыс! Каспи картаңызды жалға беріңіз, бірден 50 мың теңге аласыз. Тек аударымды банкоматтан шешу керек."
    },
    {
        "id": 47,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Работа по транзиту платежей. Сдай карту в аренду на неделю, гарантируем 250 000 тенге. Никаких рисков."
    },
    {
        "id": 48,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Төлемдерді өткізу бойынша жұмыс. Картаңызды жалға беріп бір аптаға 250 000 теңге кепілді пайда көріңіз."
    },
    {
        "id": 49,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Нужен человек с картами BCC, Jusan или Freedom. Пропустить деньги через счет, вам остается 10% от суммы."
    },
    {
        "id": 50,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "BCC, Jusan немесе Freedom картасы бар адам керек. Ақшаны шот арқылы өткізіп жіберсеңіз, соманың 10%-ы өзіңізде қалады."
    },
    {
        "id": 51,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Сдай карту Каспи в аренду прямо сейчас! Деньги начисляются ежедневно на баланс. Пишите в ЛС, всё анонимно."
    },
    {
        "id": 52,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Дәл қазір Каспи картаңызды жалға беріңіз! Күн сайын шотқа ақша түсіп отырады. Толық анонимді түрде."
    },
    {
        "id": 53,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Дропперство для молодежи: сдай карту в аренду, получи легкие 60 000 тг. Нужно дать логин и пароль от банкинга."
    },
    {
        "id": 54,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Дропперлік қызмет: картаңызды жалға беріп 60 000 тг табыңыз. Банкингтің логині мен құпия сөзі керек."
    },
    {
        "id": 55,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Купим дебетовую карту с оформленным мобильным банком. Оплата 70 тыс тенге сразу на руки."
    },
    {
        "id": 56,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "dropper_card",
        "text": "Мобильді банкингі бар банк картасын сатып аламыз. Қолма-қол 70 мың теңге береміз."
    },

    # ==========================================
    # 4. SMS CODE / EGOV FRAUD (18 cases)
    # ==========================================
    {
        "id": 57,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Добрый день, говорит менеджер eGov. Продиктуйте код из SMS для подтверждения перерегистрации льгот!"
    },
    {
        "id": 58,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Сәлеметсіз бе! СМС кодты айтыңыз, бұл eGov жүйесінде растау үшін керек!"
    },
    {
        "id": 59,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Здравствуйте, курьер Казпочты. Ваша посылка задерживается. Назовите код из SMS от 1414, чтобы изменить адрес доставки."
    },
    {
        "id": 60,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Қазпошта курьері. Сәлемдемеңіз тұрып қалды. Мекенжайды ауыстыру үшін 1414 жіберген СМС кодты айтып жіберіңіз."
    },
    {
        "id": 61,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Служба поддержки WhatsApp Казахстана. Зафиксирована попытка входа. Скажите код из смс, чтобы заблокировать мошенника."
    },
    {
        "id": 62,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "WhatsApp қолдау қызметі. Басқа біреу сіздің аккаунтыңызға кіруде. Бұғаттау үшін смс кодты айтыңыз."
    },
    {
        "id": 63,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Сотрудник ЦОН. Вы записаны на получение ЭЦП. Продиктуйте поступивший смс код для валидации профиля."
    },
    {
        "id": 64,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "ХҚКО қызметкерімін. ЭЦП алуға кезекке тұрдыңыз. Профильді растау үшін смс кодты айтыңыз."
    },
    {
        "id": 65,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Уведомление от Kaspi: для отмены ошибочного списания немедленно назовите код из SMS нашему оператору!"
    },
    {
        "id": 66,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Kaspi хабарламасы: қате шешілген ақшаны қайтару үшін операторға SMS кодты тез арада айтыңыз!"
    },
    {
        "id": 67,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Медицинский портал DamuMed. Вам назначен прием врача. Скажите код из смс для подтверждения талона."
    },
    {
        "id": 68,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "DamuMed медициналық порталы. Дәрігер қабылдауына жазылдыңыз. Талонды бекіту үшін смс кодты айтыңыз."
    },
    {
        "id": 69,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Оператор Beeline / Kcell: срок действия вашей SIM-карты истекает. Продиктуйте код из смс для продления номера."
    },
    {
        "id": 70,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Beeline / Kcell байланыс операторы: SIM картаңыздың мерзімі аяқталуда. Нөмірді созу үшін смс кодты айтыңыз."
    },
    {
        "id": 71,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Единый накопительный пенсионный фонд (ЕНПФ). Начислена выплата, назовите код из смс для перевода на карту."
    },
    {
        "id": 72,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "БЖЗҚ (ЕНПФ): төлем есептелді. Картаға түсіру үшін смс кодты хабарлаңыз."
    },
    {
        "id": 73,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "Служба безопасности Госуслуг eGov.kz. Срочно скажите код из SMS, иначе доступ к вашему ИИН будет закрыт!"
    },
    {
        "id": 74,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "sms_code",
        "text": "eGov мемлекеттік қызметі. Тез арада смс кодты айтыңыз, әйтпесе ЖСН бойынша қолжетімділік жабылады!"
    },

    # ==========================================
    # 5. TELEGRAM JOB / FAKE EARNINGS (18 cases)
    # ==========================================
    {
        "id": 75,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Работа в Telegram! За ставку лайков платим 2000 тг сразу, затем нужно пополнить баланс на 30 000 тг для выкупа товаров."
    },
    {
        "id": 76,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Telegram-да жұмыс! Лайк үшін 2000 тг төлейміз, кейін тауар сатып алу үшін балансты 30 000 тг-ге толтыру керек."
    },
    {
        "id": 77,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Удаленная работа в Wildberries / Ozon. Ставьте оценки отелям и товарам, доход 18 000 тг в день. Первые задания в Telegram."
    },
    {
        "id": 78,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Wildberries / Ozon қашықтан жұмыс. Тауарларға баға қойып, күніне 18 000 тг табыңыз. Барлық тапсырма Telegram-да."
    },
    {
        "id": 79,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Подработка для мам в декрете! Просмотр роликов на YouTube и TikTok. Оплата 500 тенге за лайк, регистрация в закрытой группе."
    },
    {
        "id": 80,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Аналарға арналған қосымша табыс! TikTok пен YouTube-та видео көру. Әр лайкқа 500 тг, Telegram топқа қосылыңыз."
    },
    {
        "id": 81,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Вы успешно выполнили первый уровень задач. Чтобы перейти на VIP-заказы с выплатой 80 000 тг, сделайте депозит 25 000 тг."
    },
    {
        "id": 82,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Бірінші кезең тапсырмаларын орындадыңыз. 80 000 тг табыс әкелетін VIP деңгейге өту үшін 25 000 тг депозит салыңыз."
    },
    {
        "id": 83,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Международная маркетинговая компания ищет респондентов. Оплата за отзывы на маркетплейсах. Работа в Телеграм, выкуп товаров."
    },
    {
        "id": 84,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Маркетингтік компания тауарларға пікір жазатын адамдарды шақырады. Жұмыс Telegram-да, тауарды выкуп жасау қажет."
    },
    {
        "id": 85,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Привет! Мы платим за подписки на каналы. 15 каналов = 3 500 тг. Затем пополнение счета для удвоения прибыли."
    },
    {
        "id": 86,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Сәлем! Каналдарға жазылу үшін төлейміз. 15 канал = 3500 тг. Сосын пайданы екі есе арттыру үшін шотты толтырасыз."
    },
    {
        "id": 87,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Быстрый заработок онлайн. Нужно бронировать отели на Booking. Заработок от 25 тыс тг, сначала внесите гарантийный сбор."
    },
    {
        "id": 88,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Онлайн жылдам табыс табу. Booking арқылы қонақүй брондау керек. Табыс 25 мың тг, бірақ алдымен кепілдік салым салу қажет."
    },
    {
        "id": 89,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Работа на дому. Ставьте лайки брендам Kaspi Магазина. Оплата ежедневно, пишите нашему менеджеру в Телеграм."
    },
    {
        "id": 90,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Үйде отырып жұмыс. Kaspi дүкен тауарларына лайк қойыңыз. Төлем күн сайын, Telegram арқылы жазыңыз."
    },
    {
        "id": 91,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "Вам начислен бонус за 3 выполненных лайка! Для вывода 15 000 тг оплатите верификацию аккаунта на сумму 8 000 тг."
    },
    {
        "id": 92,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "telegram_job",
        "text": "3 лайк үшін бонус есептелді! 15 000 тг шығарып алу үшін аккаунтты 8 000 теңгеге верификациялау қажет."
    },

    # ==========================================
    # 6. OLX / INSTAGRAM PREPAYMENT (18 cases)
    # ==========================================
    {
        "id": 93,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Продам iPhone 15 Pro Max за 250 000 тг, срочно нужны деньги. Отправлю индрайвером или казпочтой, скиньте предоплату 30 000 тг на карту."
    },
    {
        "id": 94,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "iPhone 15 Pro Max 250 000 тг сатылады, ақша шұғыл керек. Индрайвермен жіберемін, картаға 30 000 тг алдын ала төлем жасаңыз."
    },
    {
        "id": 95,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Здравствуйте по объявлению на OLX. Я сейчас в селе, привезти в город смогу только после предоплаты 10 000 тг за бензин."
    },
    {
        "id": 96,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "OLX бойынша. Ауылдамын, қалаға бензин ақшасына 10 000 тг алдын ала төлем аударсаңыз ғана жеткізіп беремін."
    },
    {
        "id": 97,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Товар в наличии в Instagram магазине. Отправка только по полной предоплате на Каспи номер. Наложенным платежом не работаем."
    },
    {
        "id": 98,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Instagram дүкенімізде тауар бар. Тек Каспиге 100% алдын ала төлем арқылы жібереміз. Қолма-қол төлем қабылданбайды."
    },
    {
        "id": 99,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "PlayStation 5 в идеале за 120 тыс тг. Покупателей много, бронь только по задатку 20 000 тг на карту физлица."
    },
    {
        "id": 100,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "PlayStation 5 жаңа күйінде 120 мың тг. Алушылар көп, тек 20 000 тг кепіл аударған адамға сақтаймын."
    },
    {
        "id": 101,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Я оформил безопасную сделку на OLX Доставке. Перейдите по ссылке http://olx-kz-delivery.net/pay и получите деньги на карту."
    },
    {
        "id": 102,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "OLX жеткізу арқылы төледім. Мына http://olx-kz-delivery.net/pay сілтемесіне өтіп, ақшаны картаңызға қабылдаңыз."
    },
    {
        "id": 103,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Коляска детская новая, отдаю дешево. Переведите аванс 15000 на карту Kaspi, иначе продам другим."
    },
    {
        "id": 104,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Балалар арбасы арзан бағада. Каспи картаға 15 000 тг аванс аударыңыз, әйтпесе басқа адам алып кетеді."
    },
    {
        "id": 105,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Продажа щенков шпица с документами. Доставка с питомника по предоплате 25 000 тенге."
    },
    {
        "id": 106,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Шпиц күшіктері құжаттарымен сатылады. Жеткізу 25 000 тг алдын ала төлем жасағанда ғана жүзеге асады."
    },
    {
        "id": 107,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Диски на Камри R18. Отправлю фурой из Караганды, переведите предоплату 40 000 тг на Каспи."
    },
    {
        "id": 108,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Камри R18 дөңгелектері. Қарағандыдан фурамен жіберемін, алдын ала 40 000 тг аударыңыз."
    },
    {
        "id": 109,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Оригинальные кроссовки со скидкой 70%. Скиньте аванс 12000 тенге прямо сейчас, акция заканчивается."
    },
    {
        "id": 110,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "olx_prepay",
        "text": "Түпнұсқа кроссовкалар 70% жеңілдікпен. 12 000 теңге аванс аударыңыз, жеңілдік мерзімі бітуде."
    },

    # ==========================================
    # 7. CRYPTO & FAKE INVESTMENT (16 cases)
    # ==========================================
    {
        "id": 111,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Инвестиционная платформа Казатомпром! Гарантированный доход от 350 000 тенге в неделю без риска. Переведите первый депозит 50 000 тг."
    },
    {
        "id": 112,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Қазатомөнеркәсіп инвестициялық платформасы! Тәуекелсіз аптасына 350 000 тг кепілдендірілген табыс. Бастапқы депозит 50 000 тг аударыңыз."
    },
    {
        "id": 113,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Национальная программа КазМунайГаз Инвест: пассивный доход 40% в месяц для всех граждан РК. Срочно внесите стартовый вклад на счет брокера."
    },
    {
        "id": 114,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "ҚазМұнайГаз Инвест ұлттық бағдарламасы: барлық ҚР азаматтарына айына 40% табыс. Брокер шотына алғашқы жарнаны дереу салыңыз."
    },
    {
        "id": 115,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Официальный трейдинг Kaspi Invest. Автоматический робот приносит 15% в день. Пополните криптовалютный депозит на 100 000 тенге."
    },
    {
        "id": 116,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Kaspi Invest ресми трейдингі. Автоматты бот күніне 15% әкеледі. 100 000 теңге көлемінде депозит салыңыз."
    },
    {
        "id": 117,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Закрытый инвестиционный клуб Тимура Турлова. Доходность 500% в год без риска. Переведите деньги на счет инвестиционного менеджера."
    },
    {
        "id": 118,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Тимур Турловтың жабық инвестициялық клубы. Жылына 500% кепілдендірілген табыс. Инвестиция менеджерінің шотына ақша аударыңыз."
    },
    {
        "id": 119,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Инвестируйте в добычу нефти и газа Казахстана. Гарантия государственного возврата, пассивный доход от 200 000 тенге каждый месяц."
    },
    {
        "id": 120,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Қазақстанның мұнай-газ секторына инвестиция. Мемлекет кепілдігі, ай сайын 200 000 теңгеден басталатын пассивті табыс."
    },
    {
        "id": 121,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Halyk Crypto Fund: вложи 60 000 тг и получи 180 000 тг уже через 3 дня. Выплаты гарантированы смарт-контрактом."
    },
    {
        "id": 122,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Halyk Крипто қоры: 60 000 тг салып, 3 күнде 180 000 тг қайтарып алыңыз. Пассивті табыс кепілдендірілген."
    },
    {
        "id": 123,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Заработок на криптовалютных арбитражах Казахстана. 12% прибыли с каждого круга без риска, перевод депозита прямо сейчас."
    },
    {
        "id": 124,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Қазақстандағы криптовалюталық арбитраж. Тәуекелсіз әр айналымнан 12% пайда, депозитті дәл қазір аударыңыз."
    },
    {
        "id": 125,
        "lang": "ru",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Казахстанская платформа AI Trading: доходность от 30% в неделю. Срочно зарегистрируйтесь и внесите депозит."
    },
    {
        "id": 126,
        "lang": "kz",
        "expected_level": "risk",
        "expected_scheme": "crypto_invest",
        "text": "Қазақстандық AI Trading жүйесі: аптасына 30% кепілді табыс. Шұғыл тіркеліп, шотқа ақша салыңыз."
    },

    # ==========================================
    # 8. FAKE PRIZE / LOTTERY (14 cases)
    # ==========================================
    {
        "id": 127,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Поздравляем! Ваш номер выиграл автомобиль Toyota Camry 75 в юбилейном розыгрыше. Оплатите только доставку 45 000 тг!"
    },
    {
        "id": 128,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Құттықтаймыз! Сіз мерейтойлық ойында Toyota Camry 75 автокөлігін ұтып алдыңыз. Тек 45 000 тг жеткізу ақысын төлеңіз!"
    },
    {
        "id": 129,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Вы выиграли iPhone 16 Pro Max от Magnum Cash&Carry! Для получения приза переведите госпошлину 15 000 тг на указанную карту."
    },
    {
        "id": 130,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Сіз Magnum-нан iPhone 16 Pro Max ұттыңыз! Сыйлықты алу үшін көрсетілген шотқа 15 000 тг салық төлемін аударыңыз."
    },
    {
        "id": 131,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Уведомление от Kaspi: ваш чек выиграл 1 000 000 тенге! Для зачисления переведите комиссию банка 25 000 тенге."
    },
    {
        "id": 132,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Kaspi хабарламасы: сіздің чегіңіз 1 000 000 теңге ұтты! Шотқа аудару үшін банктің 25 000 тг комиссиясын төлеңіз."
    },
    {
        "id": 133,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Розыгрыш от Sulpak: вы стали победителем! Оплатите страховку посылки 18 000 тг, курьер доставит ТВ вам домой."
    },
    {
        "id": 134,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Sulpak ұтысы: сіз жеңімпаз атандыңыз! 18 000 тг сақтандыру жарнасын аударыңыз, курьер теледидарды үйіңізге жеткізеді."
    },
    {
        "id": 135,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Вы выиграли путевку в Дубай на двоих! Для активации сертификата оплатите сбор туроператора 50 000 тг."
    },
    {
        "id": 136,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Дубайға екі кісілік жолдама ұтып алдыңыз! Сертификатты белсендіру үшін туроператор жиналымына 50 000 тг төлеңіз."
    },
    {
        "id": 137,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Ваш номер выпал в лотерее мобильных операторов Казахстана. Выигрыш 500 000 тг, оплатите налог 20 000 тг."
    },
    {
        "id": 138,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Қазақстан байланыс операторларының лотереясында сіздің нөміріңіз ұтты. 500 000 тг ұтысқа 20 000 тг салық төлеңіз."
    },
    {
        "id": 139,
        "lang": "ru",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Подарочный бокс от техномаркета! Вы выиграли Dyson. Оплатите курьерскую доставку 12 000 тг прямо сейчас."
    },
    {
        "id": 140,
        "lang": "kz",
        "expected_level": "warn",
        "expected_scheme": "fake_prize",
        "text": "Техномаркеттен сыйлық боксы! Dyson фенін ұтып алдыңыз. 12 000 тг жеткізу ақысын дәл қазір аударыңыз."
    },

    # ==========================================
    # 9. LEGITIMATE / SAFE MESSAGES (20 cases)
    # ==========================================
    {
        "id": 141,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Привет! Встречаемся сегодня в 19:00 возле Хан Шатыра? Я забронировал столик на троих."
    },
    {
        "id": 142,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Сәлем! Бүгін сағат 19:00-де Хан Шатыр жанында кездесеміз бе? Үстел брондап қойдым."
    },
    {
        "id": 143,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Здравствуйте! Квартира свободна, можем встретиться сегодня в 18:30 на объекте, лично всё покажу и проверим документы."
    },
    {
        "id": 144,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Сәлеметсіз бе! Пәтер бос, бүгін сағат 18:30-да кездесіп, бәрін көзбен көріп, құжаттарын тексерейік."
    },
    {
        "id": 145,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Мама, я дома, уроки сделал. Пообедал, пошел на тренировку по боксу, вернусь к восьми вечера."
    },
    {
        "id": 146,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Анашым, мен үйдемін, сабағымды орындадым. Түскі асымды ішіп, бокс жаттығуына кеттім, кешкі сегізде келемін."
    },
    {
        "id": 147,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Добрый день! Напоминаем о вашей записи на стрижку в барбершоп на завтра в 14:00. Будем рады видеть вас!"
    },
    {
        "id": 148,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Қайырлы күн! Ертең сағат 14:00-де шаш қидыруға жазылғаныңызды еске саламыз. Күтеміз!"
    },
    {
        "id": 149,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Коллеги, отчет за квартал загружен в общую папку на Google Диске. Пожалуйста, посмотрите до завтрашней планерки."
    },
    {
        "id": 150,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Әріптестер, тоқсандық есеп ортақ Google Дисктің папкасына салынды. Ертеңгі жиналысқа дейін қарап шығуларыңызды сұраймыз."
    },
    {
        "id": 151,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Привет! Скинул тебе на Каспи 3500 за вчерашний обед в столовой. Спасибо большое!"
    },
    {
        "id": 152,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Сәлем! Кешегі асханадағы түскі ас үшін 3500 теңгені Каспиіңе аударып қойдым. Көп рахмет!"
    },
    {
        "id": 153,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Здравствуйте! Заказ готов к выдаче в пункте Kaspi Postomat в ТРЦ Керуен. Срок хранения 3 дня."
    },
    {
        "id": 154,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Сәлеметсіз бе! Тапсырысыңыз Керуен СОО-дағы Kaspi Постоматында дайын тұр. Сақтау мерзімі 3 күн."
    },
    {
        "id": 155,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Асан, лекция по машинному обучению переносится в 402 аудиторию. Преподаватель попросил всех захватить ноутбуки."
    },
    {
        "id": 156,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Асан, машиналық оқыту дәрісі 402 аудиторияға ауыстырылды. Оқытушы бәріне ноутбук әкелуді ескертті."
    },
    {
        "id": 157,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Привет! Можешь одолжить конспект по линейной алгебре? Завтра занесу на кафедру в университете."
    },
    {
        "id": 158,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Сәлем! Сызықтық алгебра бойынша дәптеріңді бере тұрасың ба? Ертең университетте қайтарып беремін."
    },
    {
        "id": 159,
        "lang": "ru",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Доброе утро! Проверьте, пожалуйста, проект договора купли-продажи. Все реквизиты соответствуют госреестру."
    },
    {
        "id": 160,
        "lang": "kz",
        "expected_level": "safe",
        "expected_scheme": None,
        "text": "Қайырлы таң! Сатып алу-сату шартының жобасын тексеріп көріңізші. Барлық деректемелер мемлекеттік тізілімге сәйкес."
    }
]

def main():
    target_path = os.path.join(os.path.dirname(__file__), "dataset", "cases.json")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(CASES, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {len(CASES)} cases into {target_path}")

if __name__ == "__main__":
    main()
