"""
ScamCheck KZ - Anti-Fraud Detector Engine
Analyzes Kazakhstani text messages and chat transcripts for fraud indicators.
Supports Russian and Kazakh languages.
"""

import re
from typing import Dict, List, Any, Optional

SCHEMES = {
    "safe_account": {
        "id": "safe_account",
        "name_ru": "Безопасный счёт / Звонок из банка",
        "name_kz": "Қауіпсіз шот / Банктен қоңырау",
        "base_weight": 45
    },
    "olx_prepay": {
        "id": "olx_prepay",
        "name_ru": "Предоплата OLX / Instagram",
        "name_kz": "OLX / Instagram алдын ала төлемі",
        "base_weight": 25
    },
    "krisha_rent": {
        "id": "krisha_rent",
        "name_ru": "Аренда без просмотра (Krisha.kz)",
        "name_kz": "Көрмей жалға алу (Krisha.kz)",
        "base_weight": 35
    },
    "telegram_job": {
        "id": "telegram_job",
        "name_ru": "Работа в Telegram (Лайки / Оценка)",
        "name_kz": "Telegram-да жұмыс (Лайктар / Тауар бағалау)",
        "base_weight": 30
    },
    "dropper_card": {
        "id": "dropper_card",
        "name_ru": "Сдай карту в аренду (Дропперство)",
        "name_kz": "Картаны жалға беру (Дропперлік)",
        "base_weight": 60
    },
    "crypto_invest": {
        "id": "crypto_invest",
        "name_ru": "Фейк-Инвестиции (Казатомпром / КазМунайГаз)",
        "name_kz": "Фейк-Инвестициялар (Қазатомпром / ҚазМұнайГаз)",
        "base_weight": 35
    },
    "sms_code": {
        "id": "sms_code",
        "name_ru": "Код из SMS / eGov",
        "name_kz": "SMS коды / eGov қайта тіркеу",
        "base_weight": 60
    },
    "fake_prize": {
        "id": "fake_prize",
        "name_ru": "Лотерея / Выигрыш в розыгрыше",
        "name_kz": "Лотерея / Ұтыс ойынындағы ұтыс",
        "base_weight": 30
    }
}

PATTERNS = [
    {
        "pattern": r"безопасн\w*\s+сч[её]т\w*|защищ[её]нн\w*\s+сч[её]т\w*|резервн\w*\s+сч[её]т\w*|қауіпсіз\s+шот\w*|зеркальн\w*\s+кредит",
        "weight": 55,
        "scheme": "safe_account",
        "tag_ru": "Перевод на «безопасный/резервный счёт»",
        "tag_kz": "«Қауіпсіз/резервтік шотқа» аудару"
    },
    {
        "pattern": r"служб\w*\s+безопасности|сотрудник\w*\s+банка|национальн\w*\s+банк|нацбанк|генеральн\w*\s+прокуратур|майор\w*|департамент\w*\s+полиции|қауіпсіздік\s+қызмет\w*|банк\s+қызметкер\w*",
        "weight": 25,
        "scheme": "safe_account",
        "tag_ru": "Представляются СБ банка, Нацбанком или МВД",
        "tag_kz": "Банк қауіпсіздігі, Ұлттық банк немесе ІІМ болып танысады"
    },
    {
        "pattern": r"оформля\w*\s+кредит|на\s+вас\s+(?:оформ|бер)\w*|заявк\w*\s+на\s+кредит|несие\s+рәсімде\w*",
        "weight": 25,
        "scheme": "safe_account",
        "tag_ru": "Угроза оформляемого кредита",
        "tag_kz": "Рәсімделіп жатқан несиемен қорқыту"
    },
    {
        "pattern": r"код\w*\s+из\s+(?:смс|sms)|продиктуйте\s+код|назовите\s+код|скажите\s+код|(?:смс|sms)[\s-]?код\w*|кодты\s+айт\w*|смс\s+код",
        "weight": 60,
        "scheme": "sms_code",
        "tag_ru": "Запрос секретного кода из SMS",
        "tag_kz": "SMS-тен құпия кодты сұрау"
    },
    {
        "pattern": r"аренд\w*\s+карт\w*|карт\w*\s+в\s+аренду|сдать\s+карту|карту\s+в\s+аренду|пропустить\s+(?:перевод|деньги)|картаңызды\s+жалға|дроппер",
        "weight": 60,
        "scheme": "dropper_card",
        "tag_ru": "Вербовка дропперов (аренда карт)",
        "tag_kz": "Дропперлерді азғыру (карталарды жалға беру)"
    },
    {
        "pattern": r"без\s+просмотра|көрмей|в\s+отъезде|шетелдемін|за\s+границей",
        "weight": 35,
        "scheme": "krisha_rent",
        "tag_ru": "Отказ от личной встречи или просмотра",
        "tag_kz": "Жеке кездесуден немесе көруден бас тарту"
    },
    {
        "pattern": r"работа\s+в\s+telegram|telegram-да\s+жұмыс|лайк\w*|за\s+отзыв\w*|подработк\w*|просмотр\w*\s+товаров|выкуп\w*\s+товара|тапсырма\w*",
        "weight": 35,
        "scheme": "telegram_job",
        "tag_ru": "Схема «Заработок на лайках/выкупе»",
        "tag_kz": "«Лайктар/сатып алу арқылы табыс» схемасы"
    },
    {
        "pattern": r"предоплат\w*|аванс\w*|алдын\s+ала\s+төлем\w*|залог\w*|кепіл\w*",
        "weight": 25,
        "scheme": "olx_prepay",
        "tag_ru": "Требование предоплаты / залога",
        "tag_kz": "Алдын ала төлем / кепіл талап ету"
    },
    {
        "pattern": r"срочно|немедленно|прямо\s+сейчас|в\s+течение\s+(?:часа|\d+\s*мин\w*)|успе(?:ть|йте)|тез\s+арада|дереу|шұғыл|асығыңыз|осталось\s+\d+\s+минут",
        "weight": 15,
        "scheme": None,
        "tag_ru": "Психологическое давление и ограничение времени",
        "tag_kz": "Психологиялық қысым және уақытты шектеу"
    },
    {
        "pattern": r"переведите|перевед[её]те|скиньте|отправьте\s+деньги|аударыңыз|ақша\s+жіберіңіз|депозит",
        "weight": 15,
        "scheme": None,
        "tag_ru": "Прямое требование перевести деньги",
        "tag_kz": "Ақша аударуды тікелей талап ету"
    },
    {
        "pattern": r"гарантированн?\w*\s+доход\w*|\d+\s?%\s+в\s+(?:месяц|день)|без\s+риска|пассивн\w*\s+доход\w*|казатомпром|казмунайгаз|кепілдендірілген\s+табыс\w*",
        "weight": 35,
        "scheme": "crypto_invest",
        "tag_ru": "Обещание сверхдоходных инвестиций",
        "tag_kz": "Өте жоғары табысты инвестицияларды уәде ету"
    },
    {
        "pattern": r"вы\s+выиграли|ваш\s+(?:приз|выигрыш)|оплатите\s+(?:только\s+)?доставку|сіз\s+ұттыңыз",
        "weight": 30,
        "scheme": "fake_prize",
        "tag_ru": "Фейковый выигрыш / Приз",
        "tag_kz": "Жасанды ұтыс / Сыйлық"
    },
    {
        "pattern": r"https?://\S+|bit\.ly/\S+|t\.me/\S+",
        "weight": 12,
        "scheme": None,
        "tag_ru": "Подозрительная внешняя ссылка",
        "tag_kz": "Күмәнді сыртқы сілтеме"
    },
    {
        "pattern": r"никому\s+не\s+говорите|не\s+сообщайте\s+(?:никому|родным)|ешкімге\s+айтпаңыз|строго\s+конфиденциально",
        "weight": 20,
        "scheme": None,
        "tag_ru": "Требование соблюдать секретность",
        "tag_kz": "Құпиялылықты сақтау талабы"
    }
]


class AntiFraudDetector:
    """Core detector engine for ScamCheck KZ."""

    def __init__(self):
        self.compiled_patterns = [
            {
                "regex": re.compile(item["pattern"], re.IGNORECASE),
                "weight": item["weight"],
                "scheme": item["scheme"],
                "tag_ru": item["tag_ru"],
                "tag_kz": item["tag_kz"]
            }
            for item in PATTERNS
        ]

    def analyze(self, text: str, lang: str = "ru") -> Dict[str, Any]:
        """Analyze text and return risk assessment."""
        if not text or not text.strip():
            return {
                "score": 0,
                "level": "safe",
                "scheme": None,
                "scheme_name": None,
                "triggers": [],
                "highlights": [],
                "recommendations": self._get_recommendations("safe", lang)
            }

        score = 0
        triggers = []
        scheme_hits: Dict[str, int] = {}
        highlights = []

        for item in self.compiled_patterns:
            matches = list(item["regex"].finditer(text))
            if matches:
                score += item["weight"]
                tag = item["tag_kz"] if lang == "kz" else item["tag_ru"]
                triggers.append(tag)

                if item["scheme"]:
                    scheme_hits[item["scheme"]] = scheme_hits.get(item["scheme"], 0) + item["weight"]

                for m in matches:
                    highlights.append({
                        "start": m.start(),
                        "end": m.end(),
                        "text": m.group(0)
                    })

        score = min(98, score)

        if score >= 50:
            level = "risk"
        elif score >= 25:
            level = "warn"
        else:
            level = "safe"

        top_scheme = None
        scheme_name = None
        if scheme_hits and level != "safe":
            top_scheme = max(scheme_hits.items(), key=lambda x: x[1])[0]
            if top_scheme in SCHEMES:
                scheme_name = SCHEMES[top_scheme]["name_kz"] if lang == "kz" else SCHEMES[top_scheme]["name_ru"]

        return {
            "score": score,
            "level": level,
            "scheme": top_scheme,
            "scheme_name": scheme_name,
            "triggers": list(dict.fromkeys(triggers)),
            "highlights": highlights,
            "recommendations": self._get_recommendations(level, lang)
        }

    def _get_recommendations(self, level: str, lang: str) -> List[str]:
        if lang == "kz":
            if level == "risk":
                return [
                    "АҚША АУДАРМАҢЫЗ және ешқандай құпия кодтарды бермеңіз",
                    "Картаның артындағы нөмір бойынша банктің ресми колл-центріне хабарласыңыз",
                    "102 немесе Киберпол нөміріне алаяқтық туралы хабарлаңыз"
                ]
            elif level == "warn":
                return [
                    "Әңгімелесушіге нақтылаушы сұрақтар қойыңыз",
                    "Чаттағы сыртқы сілтемелерге өтпеңіз",
                    "Ақпаратты ресми дереккөздерден қайта тексеріңіз"
                ]
            else:
                return [
                    "Алаяқтықтың айқын белгілері табылған жоқ",
                    "Ақша сұраса — адамға жеке қоңырау шалыңыз",
                    "SMS-кодтар мен құпия сөздерді ешқашан айтпаңыз"
                ]
        else:
            if level == "risk":
                return [
                    "НЕ ПЕРЕВОДИТЕ ДЕНЬГИ и не передавайте никакие коды из SMS",
                    "Позвоните в официальный колл-центр банка по номеру на карте",
                    "Сообщите о мошенничестве по номеру 102 или в Киберпол"
                ]
            elif level == "warn":
                return [
                    "Задайте уточняющие вопросы собеседнику",
                    "Не переходите по внешним ссылкам из чата",
                    "Перепроверьте информацию в официальных источниках"
                ]
            else:
                return [
                    "Явных признаков мошенничества не выявлено",
                    "Если вас просят о финансовой помощи — перезвоните человеку лично",
                    "Никогда не сообщайте SMS-коды и пароли"
                ]


detector = AntiFraudDetector()
