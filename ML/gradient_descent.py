import numpy as np


def gradient_descent(x, y) -> int:
    print(type(x))
    m_curr = 0
    b_curr = 0
    iterations = 10
    n = len(x)
    learning_rate = 0.06
    for i in range(iterations):
        y_predicted = m_curr * x + b_curr
        cost = (1 / n) * sum([val ** 2 for val in (y - y_predicted)])
        md = -(2 / n) * sum(x * (y - y_predicted))
        bd = -(2 / n) * sum(y - y_predicted)
        m_curr = m_curr - (learning_rate * md)
        b_curr = b_curr - (learning_rate * bd)
        print('m {}, b {}, cost {}, iteration {}'.format(m_curr, b_curr, cost, i))
    return [m_curr, b_curr]


x = np.array([1, 2, 3, 4, 5])
y = np.array([5, 7, 9, 11, 13])

gradient_descent(x, y)
