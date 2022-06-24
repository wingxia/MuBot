def get_img_id(pr_str):
    id_index = pr_str.find('imageId') + 10
    return pr_str[id_index:id_index + 42]
