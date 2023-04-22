def percentage(num):
    """convert numbers to percentage (note: I made these functions before I was aware of f-string formatting for percentages)"""
    p_num = round(num * 100, 1)
    return p_num

def add_percent_sign(num):
    s_num = str(num) + "%"
    return s_num