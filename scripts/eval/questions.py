# -*- coding: utf-8 -*-

QUESTIONS = [
    # 推理/逻辑
    {
        "id": "reasoning-01",
        "dimension": "reasoning",
        "prompt": "一个水果篮里共有苹果和橙子 12 个，苹果比橙子多 4 个。请问苹果和橙子各有多少个？请给出计算过程。",
        "hints": ["8", "4"],
    },
    {
        "id": "reasoning-02",
        "dimension": "reasoning",
        "prompt": "鸡和兔关在同一个笼子里，共有 35 个头、94 只脚。请问鸡和兔各有多少只？",
        "hints": ["23", "12"],
    },
    {
        "id": "reasoning-03",
        "dimension": "reasoning",
        "prompt": "甲、乙、丙三人中只有一个人说真话。甲说“乙在说谎”，乙说“丙在说谎”，丙说“甲和乙都在说谎”。请问谁说真话？请说明推理过程。",
        "hints": ["乙"],
    },
    # 代码生成
    {
        "id": "code-01",
        "dimension": "code",
        "prompt": "用 Python 写一个函数 is_prime(n)，判断一个整数是否为素数，并给出 2 个测试示例。",
        "hints": ["def", "is_prime", "%", "return"],
    },
    {
        "id": "code-02",
        "dimension": "code",
        "prompt": "用 Python 实现斐波那契数列，输出前 10 项。",
        "hints": ["def", "1, 1, 2", "fib"],
    },
    {
        "id": "code-03",
        "dimension": "code",
        "prompt": "用 Python 写一个函数 reverse_string(s)，将字符串反转，例如输入 \"hello\" 输出 \"olleh\"。",
        "hints": ["def", "reverse", "[::-1]"],
    },
    # 通用问答/知识
    {
        "id": "knowledge-01",
        "dimension": "knowledge",
        "prompt": "日本的首都是哪座城市？",
        "hints": ["东京", "Tokyo"],
    },
    {
        "id": "knowledge-02",
        "dimension": "knowledge",
        "prompt": "水的化学式是什么？",
        "hints": ["H2O", "H₂O"],
    },
    {
        "id": "knowledge-03",
        "dimension": "knowledge",
        "prompt": "地球绕太阳公转一周大约需要多少天？",
        "hints": ["365"],
    },
    # 翻译（Smartrans 题材）
    {
        "id": "translation-01",
        "dimension": "translation",
        "prompt": "请将下面这句话翻译成日语：\n“关于贵公司的产品报价，我们将在本周内确认并回复。”",
        "hints": ["見積", "今週", "返信"],
    },
    {
        "id": "translation-02",
        "dimension": "translation",
        "prompt": "请将下面这句日语翻译成中文：\n「本システムの導入により、業務効率の大幅な改善が期待されます。」",
        "hints": ["系统", "效率", "改善"],
    },
    {
        "id": "translation-03",
        "dimension": "translation",
        "prompt": "请将下面这句合同条款翻译成日语：\n“本合同自双方签字之日起生效，有效期为三年。”",
        "hints": ["契約", "発効", "有効期間"],
    },
    # 指令遵循/格式
    {
        "id": "instruction-01",
        "dimension": "instruction",
        "prompt": "请严格使用 JSON 格式输出以下信息：你的名称、所在公司、擅长领域。只输出 JSON，不要输出其他任何文字。",
        "hints": ["{", "}", "name", "company"],
    },
    {
        "id": "instruction-02",
        "dimension": "instruction",
        "prompt": "请用 Markdown 无序列表列出三种提高工作效率的方法，每项不超过 10 个字。",
        "hints": ["- ", "* "],
    },
    {
        "id": "instruction-03",
        "dimension": "instruction",
        "prompt": "请只回答一个字：是 或 否。问题是：“1+1 等于 2 吗？”",
        "hints": ["是"],
    },
    # 长文本理解
    {
        "id": "longtext-01",
        "dimension": "longtext",
        "prompt": "请阅读以下关于智能翻译系统 Smartrans 的介绍，然后回答问题。\n介绍：Smartrans 是一款面向企业客户的智能翻译系统，支持中文、日语、英语等 20 多种语言的互译。该系统于 2023 年上线，目前已服务超过 500 家企业客户，日均翻译量达到 100 万字符。\n问题：Smartrans 目前服务了多少家企业客户？",
        "hints": ["500"],
    },
    {
        "id": "longtext-02",
        "dimension": "longtext",
        "prompt": "请阅读以下介绍后回答问题。\n介绍：Smartrans 是一款面向企业客户的智能翻译系统，支持中文、日语、英语等 20 多种语言的互译，在金融、法律、IT 等垂直领域表现突出。\n问题：Smartrans 支持多少种语言的互译？",
        "hints": ["20"],
    },
    {
        "id": "longtext-03",
        "dimension": "longtext",
        "prompt": "请阅读以下介绍后回答问题。\n介绍：Smartrans 是一款面向企业客户的智能翻译系统，该系统于 2023 年上线，日均翻译量达到 100 万字符。\n问题：Smartrans 于哪一年上线？",
        "hints": ["2023"],
    },
    # 多轮对话
    {
        "id": "dialog-01",
        "dimension": "dialog",
        "prompt": "以下是用户与助手的对话：\n用户：我想了解贵公司的智能翻译产品。\n助手：您好，我们的 Smartrans 产品支持 20 多种语言互译。\n用户：它在金融领域的表现如何？\n问题：用户最后一句中的「它」指的是什么？",
        "hints": ["Smartrans"],
    },
    {
        "id": "dialog-02",
        "dimension": "dialog",
        "prompt": "对话：\n甲：这个项目下周五之前能完成吗？\n乙：可以，我会在周三提交初稿，周五提交终稿。\n问题：乙承诺什么时候提交终稿？",
        "hints": ["周五"],
    },
    {
        "id": "dialog-03",
        "dimension": "dialog",
        "prompt": "对话：\n顾客：这款手机有蓝色吗？\n店员：蓝色暂时缺货，我们还有黑色和白色。\n顾客：那我要一台黑色的。\n问题：顾客最终决定购买什么颜色的手机？",
        "hints": ["黑色"],
    },
    # 信息抽取
    {
        "id": "extraction-01",
        "dimension": "extraction",
        "prompt": "请从以下文本中提取所有出现的人名和地名：\n「李明在北京工作，他的同事王芳来自上海。」",
        "hints": ["李明", "王芳", "北京", "上海"],
    },
    {
        "id": "extraction-02",
        "dimension": "extraction",
        "prompt": "请从以下文本中提取所有数字信息：\n「公司 2024 年营收达到 1.5 亿元，同比增长 20%，员工人数从 300 人增长到 450 人。」",
        "hints": ["2024", "1.5", "20", "300", "450"],
    },
    {
        "id": "extraction-03",
        "dimension": "extraction",
        "prompt": "请从以下文本中提取公司名称、成立年份和主营业务：\n「字节跳动成立于 2012 年，是一家以短视频和信息分发为主的科技公司。」",
        "hints": ["字节跳动", "2012", "短视频"],
    },
]

DIMENSIONS = ["reasoning", "code", "knowledge", "translation", "instruction", "longtext", "dialog", "extraction"]

DIMENSION_NAMES = {
    "reasoning": "推理/逻辑",
    "code": "代码生成",
    "knowledge": "通用问答/知识",
    "translation": "翻译(Smartrans题材)",
    "instruction": "指令遵循/格式",
    "longtext": "长文本理解",
    "dialog": "多轮对话",
    "extraction": "信息抽取",
}
