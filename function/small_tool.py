from graia.ariadne.message.chain import MessageChain


def get_img_id(message: MessageChain):
    pr_str = message.as_persistent_string()
    id_index = pr_str.find('imageId') + 10
    return pr_str[id_index:id_index + 42]
