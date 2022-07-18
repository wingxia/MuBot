from graia.ariadne.message.chain import MessageChain

from function.GlobalVariable import globalVariables as Gvb
from function.rsql import run_sql


def get_img_id(message: MessageChain):
    pr_str = message.as_persistent_string()
    id_index = pr_str.find('imageId') + 10
    return pr_str[id_index:id_index + 42]


def fresh_cache():
    Gvb.skyDealGroups = run_sql("select group_id from group_sw where deal = 1")
    Gvb.forbiddingWords = run_sql(f"select words from fb_words")
    Gvb.KeyWordsList = run_sql("select keywords from keywords_reply")
    Gvb.AdminList = run_sql("select qq_id from admin")
