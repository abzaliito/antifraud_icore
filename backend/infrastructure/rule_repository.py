"""
Infrastructure Layer - Rule Repository
Provides data access to fraud scheme definitions and pattern matching rules.
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
    """Repository implementation containing Kazakhstan anti-fraud rules."""

    def __init__(self):
        self._schemes: Dict[str, FraudScheme] = {
            "safe_account": FraudScheme(
                id="safe_account",
                name_ru="Безопасный счёт / Звонок из банка",
                name_kz="Қауіпсіз шот / Банктен қоңырау",
                description_ru="Звонки от лже-сотрудников банков или правоохранительных органов",
                description_kz="Банк немесе құқық қорғау органдарының жалған қызметкерлерінен қоңыраулар",
                base_weight=45
            ),
            "olx_prepay": FraudScheme(
                id="olx_prepay",
                name_ru="Предоплата OLX / Instagram",
                name_kz="OLX / Instagram алдын ала төлемі",
                description_ru="Требование перевести предоплату за товар на личную карту",
                description_kz="Тауар үшін жеке картаға алдын ала төлем талап ету",
                base_weight=25
            ),
            "krisha_rent": FraudScheme(
                id="krisha_rent",
                name_ru="Аренда без просмотра (Krisha.kz)",
                name_kz="Көрмей жалға алу (Krisha.kz)",
                description_ru="Залог за квартиру без предварительного показа",
                description_kz="Пәтерді көрмей тұрып алдын ала кепіл аудару",
                base_weight=35
            ),
            "telegram_job": FraudScheme(
                id="telegram_job",
                name_ru="Работа в Telegram (Лайки / Оценка)",
                name_kz="Telegram-да жұмыс (Лайктар / Тауар бағалау)",
                description_ru="Схема с начальной выгодой и последующим пополнением баланса",
                description_kz="Бастапқы пайдасы бар, кейін балансты толтыруды талап ететін схема",
                base_weight=30
            ),
            "dropper_card": FraudScheme(
                id="dropper_card",
                name_ru="Сдай карту в аренду (Дропперство)",
                name_kz="Картаны жалға беру (Дропперлік)",
                description_ru="Передача карты третьим лицам для транзита незаконных средств",
                description_kz="Заңсыз қаражатты өткізу үшін картаны бөгде адамдарға беру",
                base_weight=60
            ),
            "crypto_invest": FraudScheme(
                id="crypto_invest",
                name_ru="Фейк-Инвестиции (Казатомпром / КазМунайГаз)",
                name_kz="Фейк-Инвестициялар (Қазатомпром / ҚазМұнайГаз)",
                description_ru="Реклама нереальной прибыльности от имени нацкомпаний РК",
                description_kz="ҚР ұлттық компаниялары атынан жоғары табыс жарнамасы",
                base_weight=35
            ),
            "sms_code": FraudScheme(
                id="sms_code",
                name_ru="Код из SMS / eGov",
                name_kz="SMS коды / eGov қайта тіркеу",
                description_ru="Запрос 4-6 значного SMS кода для взлома доступа",
                description_kz="Қолжетімділікті бұзу үшін 4-6 таңбалы SMS кодты сұрау",
                base_weight=60
            ),
            "fake_prize": FraudScheme(
                id="fake_prize",
                name_ru="Лотерея / Выигрыш в розыгрыше",
                name_kz="Лотерея / Ұтыс ойынындағы ұтыс",
                description_ru="Требование уплаты комиссии или налога для получения приза",
                description_kz="Сыйлықты алу үшін комиссия немесе салық төлеу талабы",
                base_weight=30
            )
        }

        self._rules: List[PatternRule] = [
            PatternRule(
                regex_pattern=r"безопасн\w*\s+сч[её]т\w*|защищ[её]нн\w*\s+сч[её]т\w*|резервн\w*\s+сч[её]т\w*|қауіпсіз\s+шот\w*|зеркальн\w*\s+кредит",
                weight=55,
                scheme_id="safe_account",
                tag_ru="Перевод на «безопасный/резервный счёт»",
                tag_kz="«Қауіпсіз/резервтік шотқа» аудару"
            ),
            PatternRule(
                regex_pattern=r"служб\w*\s+безопасности|сотрудник\w*\s+банка|национальн\w*\s+банк|нацбанк|генеральн\w*\s+прокуратур|майор\w*|департамент\w*\s+полиции|қауіпсіздік\s+қызмет\w*|банк\s+қызметкер\w*",
                weight=25,
                scheme_id="safe_account",
                tag_ru="Представляются СБ банка, Нацбанком или МВД",
                tag_kz="Банк қауіпсіздігі, Ұлттық банк немесе ІІМ болып танысады"
            ),
            PatternRule(
                regex_pattern=r"оформля\w*\s+кредит|на\s+вас\s+(?:оформ|бер)\w*|заявк\w*\s+на\s+кредит|несие\s+рәсімде\w*",
                weight=25,
                scheme_id="safe_account",
                tag_ru="Угроза оформляемого кредита",
                tag_kz="Рәсімделіп жатқан несиемен қорқыту"
            ),
            PatternRule(
                regex_pattern=r"код\w*\s+из\s+(?:смс|sms)|продиктуйте\s+код|назовите\s+код|скажите\s+код|(?:смс|sms)[\s-]?код\w*|кодты\s+айт\w*|смс\s+код",
                weight=60,
                scheme_id="sms_code",
                tag_ru="Запрос секретного кода из SMS",
                tag_kz="SMS-тен құпия кодты сұрау"
            ),
            PatternRule(
                regex_pattern=r"аренд\w*\s+карт\w*|карт\w*\s+в\s+аренду|сдать\s+карту|карту\s+в\s+аренду|пропустить\s+(?:перевод|деньги)|картаңызды\s+жалға|дроппер",
                weight=60,
                scheme_id="dropper_card",
                tag_ru="Вербовка дропперов (аренда карт)",
                tag_kz="Дропперлерді азғыру (карталарды жалға беру)"
            ),
            PatternRule(
                regex_pattern=r"без\s+просмотра|көрмей|в\s+отъезде|шетелдемін|за\s+границей",
                weight=35,
                scheme_id="krisha_rent",
                tag_ru="Отказ от личной встречи или просмотра",
                tag_kz="Жеке кездесуден немесе көруден бас тарту"
            ),
            PatternRule(
                regex_pattern=r"работа\s+в\s+telegram|telegram-да\s+жұмыс|лайк\w*|за\s+отзыв\w*|подработк\w*|просмотр\w*\s+товаров|выкуп\w*\s+товара|тапсырма\w*",
                weight=35,
                scheme_id="telegram_job",
                tag_ru="Схема «Заработок на лайках/выкупе»",
                tag_kz="«Лайктар/сатып алу арқылы табыс» схемасы"
            ),
            PatternRule(
                regex_pattern=r"предоплат\w*|аванс\w*|алдын\s+ала\s+төлем\w*|залог\w*|кепіл\w*",
                weight=25,
                scheme_id="olx_prepay",
                tag_ru="Требование предоплаты / залога",
                tag_kz="Алдын ала төлем / кепіл талап ету"
            ),
            PatternRule(
                regex_pattern=r"срочно|немедленно|прямо\s+сейчас|в\s+течение\s+(?:часа|\d+\s*мин\w*)|успе(?:ть|йте)|тез\s+арада|дереу|шұғыл|асығыңыз|осталось\s+\d+\s+минут",
                weight=15,
                scheme_id=None,
                tag_ru="Психологическое давление и ограничение времени",
                tag_kz="Психологиялық қысым және уақытты шектеу"
            ),
            PatternRule(
                regex_pattern=r"переведите|перевед[её]те|скиньте|отправьте\s+деньги|аударыңыз|ақша\s+жіберіңіз|депозит",
                weight=15,
                scheme_id=None,
                tag_ru="Прямое требование перевести деньги",
                tag_kz="Ақша аударуды тікелей талап ету"
            ),
            PatternRule(
                regex_pattern=r"гарантированн?\w*\s+доход\w*|\d+\s?%\s+в\s+(?:месяц|день)|без\s+риска|пассивн\w*\s+доход\w*|казатомпром|казмунайгаз|кепілдендірілген\s+табыс\w*",
                weight=35,
                scheme_id="crypto_invest",
                tag_ru="Обещание сверхдоходных инвестиций",
                tag_kz="Өте жоғары табысты инвестицияларды уәде ету"
            ),
            PatternRule(
                regex_pattern=r"вы\s+выиграли|ваш\s+(?:приз|выигрыш)|оплатите\s+(?:только\s+)?доставку|сіз\s+ұттыңыз",
                weight=30,
                scheme_id="fake_prize",
                tag_ru="Фейковый выигрыш / Приз",
                tag_kz="Жасанды ұтыс / Сыйлық"
            ),
            PatternRule(
                regex_pattern=r"https?://\S+|bit\.ly/\S+|t\.me/\S+",
                weight=12,
                scheme_id=None,
                tag_ru="Подозрительная внешняя ссылка",
                tag_kz="Күмәнді сыртқы сілтеме"
            ),
            PatternRule(
                regex_pattern=r"никому\s+не\s+говорите|не\s+сообщайте\s+(?:никому|родным)|ешкімге\s+айтпаңыз|строго\s+конфиденциально",
                weight=20,
                scheme_id=None,
                tag_ru="Требование соблюдать секретность",
                tag_kz="Құпиялылықты сақтау талабы"
            )
        ]

    def get_all_schemes(self) -> List[FraudScheme]:
        return list(self._schemes.values())

    def get_scheme_by_id(self, scheme_id: str) -> Optional[FraudScheme]:
        return self._schemes.get(scheme_id)

    def get_rules(self) -> List[PatternRule]:
        return self._rules
