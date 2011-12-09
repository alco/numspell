
def pl_1(order):
    """2, 3, 4"""
    return (order == 'тысяча') and 'тысячи' or order + 'а'

def pl_2(order):
    """5 и больше"""
    return (order == 'тысяча') and 'тысяч' or order + 'ов'

RU_PASSES = """
^ 1 <order> = <order>
1 <thousand> = одна тысяча
2 <thousand> = две тысячи
<2_to_4> <order> = <order, pl_1>
<not_1> <order> = <order, pl_2>
"""

