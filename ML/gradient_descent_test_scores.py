from math import isclose

import pandas as pd
from sklearn import linear_model


def gradient_descent_test_scores(x, y, expected_coeff, expected_intercept) -> float:
    print(type(x))
    """
    Calculates the best fit line for the training set using the x and y coordinates

    mean squared error = 1/n * ( summation(i = 1 to n) of (y_i - (m * x_i + b))**2 )
    partial_derivative of m = 2/n * ( summation(i = 1 to n) of - x_i * (y_i - (m * x_i + b)) )
    partial_derivative of b = 2/n * ( summation(i = 1 to n) of - (y_i - (m * x_i + b)) )

    :param x: The x coordinates, nparray
    :param y: The y coordinates, np array
    :return: The best fit line for the training set
    """
    m_curr = 0.00  # the slope
    b_curr = 0.00  # the point
    score = 0.00
    max_iterations = 415533
    learning_rate = 0.0002
    iterations = 0
    n = len(x)
    while not isclose(m_curr, expected_coeff, rel_tol=1e-20) and not isclose(b_curr, expected_intercept,
                                                                             rel_tol=1e-20) and iterations < max_iterations:
        y_predicted = m_curr * x + b_curr  # predicts the next y
        score = (1 / n) * sum([z ** 2 for z in (y - y_predicted)])
        partial_derivative_m = -(2 / n) * sum(x * (y - y_predicted))
        partial_derivative_b = -(2 / n) * sum(y - y_predicted)
        m_curr = m_curr - (learning_rate * partial_derivative_m)
        b_curr = b_curr - (learning_rate * partial_derivative_b)
        iterations += 1
        print('[m_curr {} expected_m {}] [b_curr {} expected_b {}] | score {} | iteration {}\n'.format(m_curr,
                                                                                                       expected_coeff,
                                                                                                       b_curr,
                                                                                                       expected_intercept,
                                                                                                       score,
                                                                                                       iterations))


if __name__ == '__main__':
    test_scores_df = pd.read_csv('csvfiles/test_scores.csv')
    test_scores_model = linear_model.LinearRegression()
    test_scores_model.fit(test_scores_df[['math']], test_scores_df[['cs']])
    test_scores_model_coef = test_scores_model.coef_[0][0]
    test_scores_model_intercept = test_scores_model.intercept_[0]
    print(test_scores_model.predict([[95]]))
    gradient_descent_test_scores(test_scores_df['math'].to_numpy(), test_scores_df['cs'].to_numpy(),
                                 test_scores_model_coef, test_scores_model_intercept)
