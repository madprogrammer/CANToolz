
#  Load modules
load_modules = {
    'mod_stat_beta'    : {},
    'gen_replay'   : {'load_from':'..\bmw4\act_window_close'}
}


# Scenario

actions = [
    {'gen_replay'     : {'pipe':1}},
    {'mod_stat_beta':{'pipe': 1}}

]