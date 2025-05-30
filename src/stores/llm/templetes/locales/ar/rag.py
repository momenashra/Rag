from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "أنت مساعد لتوليد رد للمستخدم.",
    "ستحصل على مجموعة من المستندات المرتبطة باستفسار المستخدم.",
    "عليك توليد رد بناءً على المستندات المقدمة.",
    "تجاهل المستندات التي لا تتعلق باستفسار المستخدم.",
    "يمكنك الاعتذار للمستخدم إذا لم تتمكن من توليد رد.",
    "عليك توليد الرد بنفس لغة استفسار المستخدم.",
    "كن مؤدباً ومحترماً في التعامل مع المستخدم.",
    "كن دقيقًا ومختصرًا في ردك. تجنب المعلومات غير الضرورية.",
    "كن حذرًا في المعلومات التي تقدمها، وتجنب اختلاق الحقائق.",
    "يجب أن تستخدم المنطق في استجاباتك من خلال تقسيم المشكلة إلى أجزاء صغيرة وحل كل جزء خطوة بخطوة.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## المستند رقم: $doc_num",
        "### المحتوى: $chunk_text",
        "## الملخص:",
        "$summary",
        "## السؤال السابق:",
        "$previous_question",
    ])
)


#### Footer ####
footer_prompt = Template("\n".join([
    "بناءً فقط على المستندات المذكورة أعلاه والملخص، يرجى توليد إجابة للمستخدم.",
    "## السؤال:",
    "$query",
    "",
    "## الإجابة:",
]))