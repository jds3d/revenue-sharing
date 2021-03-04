from . import delegator
import random
import scipy.stats as stats


# policy
def should_instantiate_delegate(params, step, sL, s):
    # flip a coin (1 joins if there's room and random says to)
    arrives = False

    rng = random.random()
    if rng >= params['arrival_rate']:
        arrives = True

    return {"arrives": arrives}


# mechanism
def instantiate_delegate(params, step, sL, s, inputs):
    # add new members
    shares = 0
    reserve_token_holdings = params['expected_reserve_token_holdings'] * stats.expon.rvs()
    system_expected_revenue = params['expected_revenue']

    # epsion is the noise in the delegator's estimate of the expectation
    epsilon = stats.norm.rvs() * params['delegator_estimation_noise_variance'] + \
        params['delegator_estimation_noise_mean']

    # this must be positive
    delegator_expected_revenue = (1 + epsilon) * system_expected_revenue
    if delegator_expected_revenue < 0:
        delegator_expected_revenue = 0

    time_factor = 2

    if inputs['should_join']:
        d = delegator.Delegator(shares, reserve_token_holdings, delegator_expected_revenue, 
                                time_factor)
        s['delegators'][d.id] = d

    key = "delegators"
    value = s['delegators']
    return key, value