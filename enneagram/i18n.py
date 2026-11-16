"""UI chrome strings (English/Arabic). Reports always render in English
regardless of this setting - see report.py / report_intervention.py."""

STRINGS = {
    "en": {
        "lang_label": "Language",
        "intro_kicker": "Confidential Clinical Tool",
        "intro_title": "Enneagram Assessment",
        "intro_sub": (
            "A structured self-report instrument designed to support therapeutic "
            "exploration of personality pattern, motivation, and growth path."
        ),
        "intro_card_intro": "This assessment includes three parts:",
        "intro_li_1": "108 statements about your core personality pattern (Enneagram type)",
        "intro_li_2": "27 statements about your instinctual focus (self-preservation / social / one-to-one)",
        "intro_li_3": "15 statements about your current overall functioning",
        "intro_card_outro": (
            "Answer honestly and quickly, based on your general tendencies rather than how you "
            "wish to be or how you act in just one context. There are no right or wrong answers. "
            "Your results will be compiled into a confidential clinical report and sent only to "
            "your therapist’s secure inbox."
        ),
        "intro_autosave_note": (
            "Your progress saves automatically as you go — it’s safe to refresh the page, "
            "go back, or reconnect without losing your answers, as long as you use the same link/tab."
        ),
        "name_label": "Client name (or identifier) — optional, shown only in the report",
        "notes_label": "Any context your therapist should know before you begin? (optional)",
        "consent_label": (
            "I understand this is a self-report tool to support therapy, not a medical or "
            "psychiatric diagnosis, and I consent to my responses being compiled into a report "
            "for my therapist."
        ),
        "begin_button": "Begin Assessment →",
        "consent_error": "Please confirm the consent checkbox to continue.",
        "part1_kicker": "Part 1 of 3",
        "part1_title": "Core Personality Pattern",
        "part1_sub": "Rate how much each statement sounds like you in general.",
        "part2_kicker": "Part 2 of 3",
        "part2_title": "Instinctual Focus",
        "part3_kicker": "Part 3 of 3",
        "part3_title": "Current Functioning",
        "part3_sub": "Rate how often each statement is true for you right now.",
        "statement_label": "Statement",
        "of": "of",
        "back_button": "← Back",
        "continue_button": "Continue →",
        "continue_part2": "Continue to Part 2 →",
        "continue_part3": "Continue to Part 3 →",
        "see_results_button": "See Results →",
        "answer_all_caption": "Please answer every statement on this page to continue.",
        "answer_all_caption_single": "Please answer every statement to continue.",
        "results_kicker": "Results",
        "results_title": "Your Clinical Profile Summary",
        "results_sub": (
            "This on-screen summary is a starting point for discussion with your therapist. "
            "A complete report has been prepared below."
        ),
        "core_fear_label": "Core fear",
        "core_desire_label": "Core desire",
        "basic_pattern_label": "Basic pattern",
        "type_scores_header": "Type Scores",
        "functioning_header": "Overall Functioning Indicator",
        "functioning_metric_label": "Functioning score",
        "instinct_stack_header": "Instinctual Stack",
        "report1_header": "Report 1 — Client Assessment Report",
        "report2_header": "Report 2 — Intervention & Session Planning Report (Practitioner Only)",
        "generate_pdf_button": "Generate PDF Report",
        "download_client_pdf": "Download Client Report PDF",
        "generate_intervention_button": "Generate Intervention Report",
        "download_intervention_pdf": "Download Intervention Report PDF",
        "email_header": "Email Reports to Practitioner",
        "email_button": "Email Report(s) to Practitioner",
        "footer_note": "Confidential — for use between client and practitioner only.",
        "access_kicker": "Private Access",
        "access_title": "Enneagram Clinical Assessment",
        "access_sub": (
            "This assessment link is restricted. Please enter the access code "
            "provided by your therapist to continue."
        ),
        "access_code_label": "Access code",
        "access_enter_button": "Enter →",
        "access_error": "Incorrect access code.",
    },
    "ar": {
        "lang_label": "اللغة",
        "intro_kicker": "أداة سريرية سرية",
        "intro_title": "تقييم الإنييغرام",
        "intro_sub": (
            "أداة تقييم ذاتي منظمة مصممة لدعم الاستكشاف العلاجي لنمط الشخصية "
            "والدوافع ومسار النمو."
        ),
        "intro_card_intro": "يتضمن هذا التقييم ثلاثة أجزاء:",
        "intro_li_1": "108 عبارات حول نمط شخصيتك الأساسي (نمط الإنييغرام)",
        "intro_li_2": "27 عبارة حول تركيزك الغريزي (الحفاظ على الذات / الاجتماعي / الفردي)",
        "intro_li_3": "15 عبارة حول أدائك الحالي بشكل عام",
        "intro_card_outro": (
            "أجب بصدق وبسرعة، بناءً على ميولك العامة وليس كما تتمنى أن تكون أو كما تتصرف "
            "في سياق واحد فقط. لا توجد إجابات صحيحة أو خاطئة. "
            "ستُجمَّع نتائجك في تقرير سريري سري يُرسل فقط إلى "
            "البريد الآمن لمعالجك النفسي."
        ),
        "intro_autosave_note": (
            "يتم حفظ تقدمك تلقائيًا أثناء الإجابة — يمكنك تحديث الصفحة أو الرجوع أو "
            "إعادة الاتصال دون فقدان إجاباتك، طالما تستخدم نفس الرابط/التبويب."
        ),
        "name_label": "اسم العميل (أو معرّف) — اختياري، يظهر فقط في التقرير",
        "notes_label": "هل هناك أي سياق يجب أن يعرفه معالجك قبل أن تبدأ؟ (اختياري)",
        "consent_label": (
            "أدرك أن هذه أداة تقييم ذاتي لدعم العلاج، وليست تشخيصًا طبيًا أو نفسيًا، "
            "وأوافق على تجميع إجاباتي في تقرير لمعالجي النفسي."
        ),
        "begin_button": "ابدأ التقييم ←",
        "consent_error": "يرجى تأكيد خانة الموافقة للمتابعة.",
        "part1_kicker": "الجزء 1 من 3",
        "part1_title": "نمط الشخصية الأساسي",
        "part1_sub": "قيّم مدى انطباق كل عبارة عليك بشكل عام.",
        "part2_kicker": "الجزء 2 من 3",
        "part2_title": "التركيز الغريزي",
        "part3_kicker": "الجزء 3 من 3",
        "part3_title": "الأداء الحالي",
        "part3_sub": "قيّم مدى صحة كل عبارة بالنسبة لك الآن.",
        "statement_label": "العبارة",
        "of": "من",
        "back_button": "رجوع →",
        "continue_button": "متابعة ←",
        "continue_part2": "متابعة إلى الجزء 2 ←",
        "continue_part3": "متابعة إلى الجزء 3 ←",
        "see_results_button": "عرض النتائج ←",
        "answer_all_caption": "يرجى الإجابة على جميع العبارات في هذه الصفحة للمتابعة.",
        "answer_all_caption_single": "يرجى الإجابة على جميع العبارات للمتابعة.",
        "results_kicker": "النتائج",
        "results_title": "ملخص ملفك السريري",
        "results_sub": (
            "هذا الملخص على الشاشة هو نقطة بداية للنقاش مع معالجك. "
            "تم إعداد تقرير كامل أدناه."
        ),
        "core_fear_label": "الخوف الأساسي",
        "core_desire_label": "الرغبة الأساسية",
        "basic_pattern_label": "النمط الأساسي",
        "type_scores_header": "درجات الأنماط",
        "functioning_header": "مؤشر الأداء العام",
        "functioning_metric_label": "درجة الأداء",
        "instinct_stack_header": "الترتيب الغريزي",
        "report1_header": "التقرير 1 — تقرير تقييم العميل",
        "report2_header": "التقرير 2 — تقرير التدخل وتخطيط الجلسات (للمعالج فقط)",
        "generate_pdf_button": "إنشاء تقرير PDF",
        "download_client_pdf": "تحميل تقرير العميل PDF",
        "generate_intervention_button": "إنشاء تقرير التدخل",
        "download_intervention_pdf": "تحميل تقرير التدخل PDF",
        "email_header": "إرسال التقارير إلى المعالج عبر البريد",
        "email_button": "إرسال التقرير/التقارير إلى المعالج",
        "footer_note": "سري — للاستخدام بين العميل والمعالج فقط.",
        "access_kicker": "وصول خاص",
        "access_title": "تقييم الإنييغرام السريري",
        "access_sub": "هذا الرابط مقيّد. يرجى إدخال رمز الوصول المقدم من معالجك للمتابعة.",
        "access_code_label": "رمز الوصول",
        "access_enter_button": "دخول ←",
        "access_error": "رمز الوصول غير صحيح.",
    },
}


def t(key, lang):
    return STRINGS.get(lang, STRINGS["en"]).get(key, STRINGS["en"].get(key, key))
