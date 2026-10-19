"""
Infrastructure Layer - Rule Repository
Provides data access to Kazakhstan fraud schemes and optimized pattern matching rules.
Supports Russian and Kazakh languages with precision-tuned weights and NLP regex patterns.
"""

import re
from typing import List, Dict, Optional
from domain.entities import FraudScheme
from domain.value_objects import Language


class PatternRule:
    """Encapsulates a single detection pattern rule."""
    def __init__(
        self,
        regex_pattern: str,
        weight: int,
        scheme_id: Optional[str],
        tag_ru: str,
        tag_kz: str
    ):
        self.regex = re.compile(regex_pattern, re.IGNORECASE)
        self.weight = weight
        self.scheme_id = scheme_id
        self.tag_ru = tag_ru
        self.tag_kz = tag_kz

    def get_tag(self, lang: Language) -> str:
        return self.tag_kz if lang == Language.KAZAKH else self.tag_ru


class InMemoryRuleRepository:
    """Repository implementation containing comprehensive Kazakhstan anti-fraud rules."""

    def __init__(self):
        self._schemes: Dict[str, FraudScheme] = {
            "safe_account": FraudScheme(
                id="safe_account",
                name_ru="Безопасный счёт / Звонок из банка",
                name_kz="Қауіпсіз шот / Банктен қоңырау",
                description_ru="Звонки от лже-сотрудников банков, МВД или Нацбанка с требованием перевода средств",
                description_kz="Банк, ІІМ немесе Ұлттық банк атынан қаражат аударуды талап ететін қоңыраулар",
                base_weight=55
            ),
            "krisha_rent": FraudScheme(
                id="krisha_rent",
                name_ru="Аренда без просмотра (Krisha.kz)",
                name_kz="Көрмей жалға алу (Krisha.kz)",
                description_ru="Требование залога за аренду квартиры без личного просмотра хозяином в отъезде",
                description_kz="Пәтер иесі шетелде/іссапарда деп пәтерді көрмей кепіл аудару талабы",
                base_weight=55
            ),
            "dropper_card": FraudScheme(
                id="dropper_card",
                name_ru="Сдай карту в аренду (Дропперство)",
                name_kz="Картаны жалға беру (Дропперлік)",
                description_ru="Вербовка дропперов: передача банковских карт третьим лицам для транзита крипты/средств",
                description_kz="Дропперлерді тарту: қаражатты өткізу үшін картаны жалға беру не сату",
                base_weight=65
            ),
            "sms_code": FraudScheme(
                id="sms_code",
                name_ru="Код из SMS / eGov",
                name_kz="SMS коды / eGov қайта тіркеу",
                description_ru="Запрос одноразового SMS-кода под предлогом eGov, доставки Казпочты или банка",
                description_kz="eGov, Қазпошта немесе банк атынан біржолғы SMS кодты сұрау",
                base_weight=65
            ),
            "crypto_invest": FraudScheme(
                id="crypto_invest",
                name_ru="Фейк-Инвестиции (Казатомпром / КазМунайГаз)",
                name_kz="Фейк-Инвестициялар (Қазатомпром / ҚазМұнайГаз)",
                description_ru="Реклама сверхдоходных инвестиций от имени нацкомпаний РК или банков",
                description_kz="ҚР ұлттық компаниялары мен банктері атынан жалған жоғары табыс жарнамасы",
                base_weight=55
            ),
            "telegram_job": FraudScheme(
                id="telegram_job",
                name_ru="Работа в Telegram (Лайки / Оценка)",
                name_kz="Telegram-да жұмыс (Лайктар / Тауар бағалау)",
                description_ru="Схема с начальной мелкой выплатой и последующим требованием пополнить баланс",
                description_kz="Бастапқы ұсақ төлем жасап, кейін ірі сомаға балансты толтыруды талап ететін схема",
                base_weight=30
            ),
            "olx_prepay": FraudScheme(
                id="olx_prepay",
                name_ru="Предоплата OLX / Instagram",
                name_kz="OLX / Instagram алдын ала төлемі",
                description_ru="Требование предоплаты или задатка за товар по подозрительно низкой цене",
                description_kz="Бағасы нарықтан төмен тауар үшін алдын ала төлем талап ету",
                base_weight=30
            ),
            "fake_prize": FraudScheme(
                id="fake_prize",
                name_ru="Лотерея / Выигрыш в розыгрыше",
                name_kz="Лотерея / Ұтыс ойынындағы ұтыс",
                description_ru="Сообщение о выигрыше с требованием оплатить налог, комиссию или доставку",
                description_kz="Сыйлық не көлік ұтып алдыңыз деп жеткізу не салық төлемін сұрау",
                base_weight=30
            ),
            "relative_emergency": FraudScheme(
                id="relative_emergency",
                name_ru="«Родственник в беде» / Срочная помощь",
                name_kz="«Туыс қиын жағдайда» / Шұғыл көмек",
                description_ru="Просьба срочно дать или перевести деньги на лечение, операцию или из-за аварии от имени родственника либо знакомого",
                description_kz="Туыс не таныс атынан емделуге, операцияға немесе апатқа байланысты ақша беруді/аударуды сұрау",
                base_weight=40
            )
        }

        self._rules: List[PatternRule] = [
            # 1. SAFE ACCOUNT SCHEME RULES (Target Level: Risk, score 65-80)
            PatternRule(
                regex_pattern=r"безопасн\w*\s+сч[её]т\w*|защищ[её]нн\w*\s+сч[её]т\w*|резервн\w*\s+сч[её]т\w*|транзитн\w*\s+сч[её]т\w*|қауіпсіз\s+шот\w*|резервтік\s+шот\w*|қорғалған\s+қауіпсіз\s+шот\w*|зеркальн\w*\s+кредит\w*",
                weight=55,
                scheme_id="safe_account",
                tag_ru="Перевод на «безопасный/резервный счёт»",
                tag_kz="«Қауіпсіз/резервтік шотқа» аудару"
            ),
            PatternRule(
                regex_pattern=r"служб\w*\s+безопасности|сотрудник\w*\s+банка|национальн\w*\s+банк\w*|нацбанк\w*|генеральн\w*\s+прокуратур\w*|майор\w*|капитан\s+полиции|департамент\w*\s+полиции|қауіпсіздік\s+қызмет\w*|банк\s+қызметкер\w*|полиция\s+департамент\w*|қаржылық\s+мониторинг|тергеуші\w*|дознаватель\w*|киберқауіпсіздік|утечка\s+персональных\s+данных|скомпрометирован\w*",
                weight=30,
                scheme_id="safe_account",
                tag_ru="Представляются СБ банка, Нацбанком, МВД или прокуратурой",
                tag_kz="Банк қауіпсіздігі, Ұлттық банк немесе ІІМ болып танысады"
            ),
            PatternRule(
                regex_pattern=r"оформля\w*\s+кредит|на\s+вас\s+(?:оформ|бер)\w*|заявк\w*\s+на\s+кредит|несие\s+рәсімде\w*|несие\s+өтініші|онлайн\s+несие|заем\s+в\s+мфо",
                weight=25,
                scheme_id="safe_account",
                tag_ru="Угроза оформляемого кредита / займа",
                tag_kz="Рәсімделіп жатқан несиемен қорқыту"
            ),

            # 2. DROPPER CARDS RULES (Target Level: Risk, score 65)
            PatternRule(
                regex_pattern=r"аренд\w*\s+карт\w*|карт\w*\s+в\s+аренду|сдать\s+карту|сдай\s+карту|сдавай\s+карту|карта[сң]?[ыі]?н?\s+жалға|жалға\s+бер\w*|дроппер\w*|пропустить\s+(?:перевод|деньги)|өткізіп\s+жібер\w*|обналичить\s+переводы|банкоматтан\s+шешу|транзит\w*\s+платеж\w*|төлемдерді\s+өткізу|купим\s+(?:дебетовую\s+)?карту|картасын\s+сатып\s+аламыз|логин\s+и\s+пароль\s+от\s+банкинг\w*|крипто-?обменник\w*|аударымнан\s+пайыз",
                weight=65,
                scheme_id="dropper_card",
                tag_ru="Вербовка дропперов (аренда/покупка банковских карт)",
                tag_kz="Дропперлерді азғыру (карталарды жалға беру/сату)"
            ),

            # 3. SMS CODE RULES (Target Level: Risk, score 65)
            PatternRule(
                regex_pattern=r"код\w*\s+из\s+(?:смс|sms)|продиктуйте\s+код|назовите\s+код|скажите\s+код|(?:смс|sms)[\s-]?код\w*|кодты\s+айт\w*|смс\s+код|смс-код|1414|egov|құпия\s+код",
                weight=65,
                scheme_id="sms_code",
                tag_ru="Запрос секретного кода из SMS / eGov / 1414",
                tag_kz="SMS / eGov / 1414 құпия кодын сұрау"
            ),

            # 4. CRYPTO & FAKE INVESTMENT RULES (Target Level: Risk, score 60-70)
            PatternRule(
                regex_pattern=r"гарантированн?\w*\s+доход\w*|\d+\s?%\s+в\s+(?:месяц|день|неделю)|без\s+риска|пассивн\w*\s+доход\w*|казатомпром|қазатомөнеркәсіп|казмунайгаз|қазмұнайгаз|тимур\w*\s+турлов\w*|kaspi\s+invest|halyk\s+crypto|крипто\s+қор\w*|crypto\s+fund|кепілдендірілген\s+табыс\w*|тәуекелсіз|криптовалютн\w*\s+арбитраж\w*|ai\s+trading|первый\s+депозит|бастапқы\s+депозит|мұнай-газ|нефть\s+и\s+газ|мемлекет\s+кепілдігі|государственн\w*\s+возврат\w*",
                weight=60,
                scheme_id="crypto_invest",
                tag_ru="Обещание сверхдоходных инвестиций от имени нацкомпаний/банков",
                tag_kz="Ұлттық компаниялар/банктер атынан жоғары табысты уәде ету"
            ),

            # 5. KRISHA.KZ FAKE RENT RULES (Target Level: Risk, score 60-70)
            PatternRule(
                regex_pattern=r"без\s+просмотра|көрмей|в\s+отъезде|шетелде\w*|за\s+границей|в\s+командировке|басқа\s+қалада|в\s+другом\s+городе|показов\s+(?:сегодня\s+)?нет|показать\s+(?:лично\s+)?не\s+могу|көрсете\s+алмаймын|жеке\s+көрсете\s+алмаймын",
                weight=45,
                scheme_id="krisha_rent",
                tag_ru="Отказ от личной встречи или просмотра жилья",
                tag_kz="Жеке кездесуден немесе пәтерді көруден бас тарту"
            ),
            PatternRule(
                regex_pattern=r"krisha(?:\.kz)?|крыш\w*|пәтер\w*|квартир\w*|коттедж\w*|бөлме\w*|жиль[её]\w*|показов\w*|заехать\s+завтра",
                weight=10,
                scheme_id="krisha_rent",
                tag_ru="Контекст аренды недвижимости",
                tag_kz="Жылжымайтын мүлікті жалдау мәнмәтіні"
            ),

            # 6. TELEGRAM JOB RULES (Target Level: Warn, score 30-40)
            PatternRule(
                regex_pattern=r"работа\s+в\s+telegram|telegram-да\s+жұмыс|лайк\w*|за\s+отзыв\w*|подработк\w*|просмотр\w*\s+товаров|выкуп\w*\s+товара|тауард?ы?\s+выкуп|выкуп\s+жасау|тапсырма\w*|wildberries|ozon|оценка\s+товаров|vip-заказ\w*|vip\s+деңгей|верификаци\w*\s+аккаунт\w*|подписк\w*\s+на\s+канал\w*|каналдарға\s+жазылу|удвоени\w*\s+прибыли|пайданы\s+екі\s+есе|бронирова\w*\s+отел\w*|қонақүй\s+брондау|гарантийн\w*\s+сбор|кепілдік\s+салым|пікір\s+жаз\w*",
                weight=30,
                scheme_id="telegram_job",
                tag_ru="Схема «Заработок на лайках/выкупе товаров/подписках»",
                tag_kz="«Лайктар/сатып алу/жазылу арқылы табыс» схемасы"
            ),

            # 7. OLX / INSTAGRAM PREPAYMENT RULES (Target Level: Warn, score 30-40)
            PatternRule(
                regex_pattern=r"olx(?:\.kz)?|инстаграм|instagram|индрайвер\w*|наложенным\s+платежом\s+не|қолма-қол\s+төлем\s+қабылданбайды|айфон|iphone|playstation|дөңгелек|диски\s+на|щенк\w*|коляск\w*|арбасы|кроссовк\w*",
                weight=20,
                scheme_id="olx_prepay",
                tag_ru="Товары / маркетплейс OLX или Instagram",
                tag_kz="Тауарлар / OLX не Instagram маркетплейсі"
            ),
            PatternRule(
                regex_pattern=r"предоплат\w*|алдын\s+ала\s+төлем\w*|залог\w*|задаток\w*|кепіл\w*|аванс\w*|бронь\w*|брондау|алдын\s+ала\s+\d+[\s\d]*\s*(?:тг|теңге)?\s*аудар\w*",
                weight=25,
                scheme_id="olx_prepay",  # Defaults to olx_prepay, krisha_rent rules override it when apartment context exists
                tag_ru="Требование предоплаты / залога / аванса",
                tag_kz="Алдын ала төлем / кепіл / аванс талап ету"
            ),

            # 8. FAKE PRIZE RULES (Target Level: Warn, score 30-40)
            PatternRule(
                regex_pattern=r"вы\s+выиграли|сіз\s+ұттыңыз|ұтып\s+алдыңыз|ұтты|выигрыш\w*|ұтыс\w*|оплатите\s+(?:только\s+)?доставку|жеткізу\s+ақысын\s+төлеңіз|госпошлин\w*|комисси\w*\s+банка|салық\s+төлемі\w*|страховк\w*\s+посылки|сақтандыру\s+жарнасы\w*|сбор\s+туроператора|розыгрыш\w*|dyson|toyota\s+camry",
                weight=30,
                scheme_id="fake_prize",
                tag_ru="Фейковый выигрыш / Приз с требованием оплаты комиссии или доставки",
                tag_kz="Жасанды ұтыс / Сыйлық үшін комиссия не салық сұрау"
            ),

            # 8.5 RELATIVE EMERGENCY / IMPERSONATION (Target Level: Warn, score 20-40)
            PatternRule(
                regex_pattern=r"на\s+лечени\w*|на\s+операци\w*|попал\w*\s+в\s+авари\w*|в\s+больниц\w*|положили\s+в\s+больниц\w*|на\s+похорон\w*|сбил\w*\s+человек\w*|перелом\w*|реанимаци\w*|мама\s+я\s+попал\w*|сын\w*\s+в\s+беде|дочь\s+в\s+беде|емдеу\w*\s+үшін|емделу\w*\s+үшін|операция\w*\s+үшін|ауруханада\w*|жол\s+апат\w*|шұғыл\s+ота\w*",
                weight=20,
                scheme_id="relative_emergency",
                tag_ru="Эмоциональное давление: лечение / авария / беда с родственником",
                tag_kz="Эмоциялық қысым: емделу / апат / туыспен жағдай"
            ),

            # 9. GENERAL PSYCHOLOGICAL & TECHNICAL TRIGGER RULES (Subtle weights)
            PatternRule(
                regex_pattern=r"срочно|немедленно|прямо\s+сейчас|в\s+течение\s+(?:часа|\d+\s*мин\w*)|успе(?:ть|йте)|тез\s+арада|дереу|шұғыл|асығыңыз|осталось\s+\d+\s+минут|дәл\s+қазір",
                weight=5,
                scheme_id=None,
                tag_ru="Психологическое давление и искусственная спешка",
                tag_kz="Психологиялық қысым және жасанды асықтыру"
            ),
            PatternRule(
                regex_pattern=r"переведите|перевед[её]те|скиньте|скинь\b|перекин\w*|перекид\w*|перечисл\w*|кинь(?:те)?|отправьте\s+деньги|аударыңыз|ақша\s+жіберіңіз|ақша\s+(?:аудар|салып|тастап)\w*|депозит\s+салыңыз|пополните\s+баланс|балансты\s+толтыр\w*",
                weight=5,
                scheme_id=None,
                tag_ru="Прямое требование перевести деньги или пополнить баланс",
                tag_kz="Ақша аударуды немесе балансты толтыруды тікелей талап ету"
            ),
            PatternRule(
                # Stranger supplying a card/account/phone as the transfer destination —
                # a strong fraud signal (e.g. "перекинь на счёт 98765456789", "карта 4400...").
                regex_pattern=r"\b\d{12,20}\b|(?:сч[её]т|карт|номер|каспи|kaspi|halyk|шот)\w*\s*(?:на|№|#)?\s*\d[\d\s.\-]{6,}\d",
                weight=25,
                scheme_id=None,
                tag_ru="Перевод на счёт/карту/номер конкретного получателя",
                tag_kz="Нақты алушының шотына/картасына/нөміріне аудару"
            ),
            PatternRule(
                # Direct request to give / lend / send money ("дай мне денег на лечение").
                regex_pattern=r"(?:дай|дайте|дашь)\s+(?:мне\s+|пожалуйста\s+)*(?:\d|деньг|денег|на\s+лечени\w*|на\s+операци\w*|взаймы|в\s+долг|тенге|тг)|(?:одолжи|одолжите|займи|займите)\s+(?:мне\s+)?(?:\d|деньг|денег|сумм|тенге|тг|взаймы)|(?:вышли|перешли|пришли)\s+(?:мне\s+)?деньг\w*|срочно\s+нужн\w*\s+деньг\w*|нужны\s+деньги\s+на|помоги\w*\s+деньг\w*|ақша\s+бер\w*|қарыз(?:ға)?\s+бер\w*|маған\s+ақша\s+бер\w*",
                weight=15,
                scheme_id=None,
                tag_ru="Просьба дать / одолжить / выслать деньги",
                tag_kz="Ақша беруді / қарыз беруді сұрау"
            ),
            PatternRule(
                regex_pattern=r"никому\s+не\s+говорите|не\s+сообщайте\s+(?:никому|родным)|ешкімге\s+айтпаңыз|строго\s+секретно|строго\s+конфиденциально|гостайна",
                weight=10,
                scheme_id=None,
                tag_ru="Требование секретности (изоляция жертвы)",
                tag_kz="Құпиялылықты сақтау талабы (жәбірленушіні оқшаулау)"
            ),
            PatternRule(
                regex_pattern=r"https?://\S+|bit\.ly/\S+|t\.me/\S+",
                weight=5,
                scheme_id=None,
                tag_ru="Подозрительная внешняя ссылка",
                tag_kz="Күмәнді сыртқы сілтеме"
            )
        ]

    def get_all_schemes(self) -> List[FraudScheme]:
        return list(self._schemes.values())

    def get_scheme_by_id(self, scheme_id: str) -> Optional[FraudScheme]:
        return self._schemes.get(scheme_id)

    def get_rules(self) -> List[PatternRule]:
        return self._rules
