from string import Template

#### RAG PROMPTS ####

#### System ####

system_prompt = Template("\n".join([
    "You are an assistant to generate a response for the user.",
    "You will be provided by a set of docuemnts associated with the user's query and previous summary.",
    "You have to generate a response based on the documents provided and summary.",
    "Ignore the documents that are not relevant to the user's query or not relavant summary.",
    "You can applogize to the user if you are not able to generate a response.",
    "You have to generate response in the same language as the user's query.",
    "Be polite and respectful to the user.",
    "Be precise and concise in your response. Avoid unnecessary information.",
    "Be careful with the information you provide, and avoid making up facts.",
    "you should use reasoning in you resposes by braking down the problem into smaller parts and solving each part step by step.",
]))

#### Document ####
document_prompt = Template(
    "\n".join([
        "## Document No: $doc_num",
        "### Content: $chunk_text",
        "## Summary:",
        "$summary",
        "##previous_question:",
        "$previous_question",
    ])
)


#### Footer ####
footer_prompt = Template("\n".join([
    "Based only on the above documents and summary, please generate an answer for the user.",
    "## Question:",
    "$query",
    "",
    "## Answer:",
])) 