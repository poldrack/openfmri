"""
setup task/contrast choices
"""

import os
import pickle

outdir='/corral-repl/utexas/poldracklab/openfmri/analyses/paper_analysis_Dec2012/data_prep'


def get_contrasts_to_use():
    datasets=['ds001','ds002','ds003','ds005','ds006A','ds007','ds008','ds011','ds017A','ds051','ds052','ds101','ds102','ds107']

    contrasts_to_use={}

    for d in datasets:
        contrasts_to_use[d]={}

    ## ## ds001 task001 balloon_analog_risk_task
    ## 7: 'explode_fixed'
    ## 17: 'pumps_demean_minus_ctrl_demean'

    contrasts_to_use['ds001'][1]=[17]

    ## ## ds002 task001 probabilistic_classification
    ## 1: task
    ## 2: feedback

    contrasts_to_use['ds002'][1]=[1]
    
    ## ## ds002 task002 deterministic_classification
    ## 1: task
    ## 2: feedback
    contrasts_to_use['ds002'][2]=[2]
    
    ## ## ds002 task003 mixed_event-related_probe
    ## 3: all
    contrasts_to_use['ds002'][3]=[3]

    ## ## ds003 task001 rhyme_judgment
    ## 1: 'word',
    ## 2: 'pseudoword
    ## 3: all
    contrasts_to_use['ds003'][1]=[3]


    ## ## ds005 task001 mixed-gambles_task
    ## 2: parametricgain
    ## 4: distancefromindifference
    contrasts_to_use['ds005'][1]=[2]

    ## ## ds006A task001 living-nonliving_decision_with_plain_or_mirror-reversed_text
    ## 8: 'switch_vs_nonswitch'
    ## 9: 'mr_vs_plain',
    contrasts_to_use['ds006A'][1]=[9]

    ## ## ds007 task002 stop_signal_with_letter_naming
    ## ## ds007 task003 stop_signal_with_pseudoword_naming
    ## ## ds007 task001 stop_signal_with_manual_response
    ## 1: 'go'
    ## 2: 'successfulstop'
    contrasts_to_use['ds007'][1]=[1]
    contrasts_to_use['ds007'][2]=[1]
    contrasts_to_use['ds007'][3]=[1]


    ## ## ds008 task001 stop_signal
    ## 1: 'go'
    ## 2: 'successfulstop'
    contrasts_to_use['ds008'][1]=[2]

    ## ## ds008 task002 conditional_stop_signal
    ## 1: 'go'
    ## 2: 'successfulstop'
    contrasts_to_use['ds008'][2]=[2]


    ## ## ds011 task001 tone-counting
    ## 1: 'tonecounting'
    ## 2: 'tonecountingprobe'
    contrasts_to_use['ds011'][1]=[1]

    ## ## ds011 task002 Single-task_weather_prediction
    ## 1: 'single-taskclassification'
    ## 2: 'single-taskprobe'
    contrasts_to_use['ds011'][2]=[1]

    ## ## ds011 task003 Dual-task_weather_prediction
    ## 1: 'dual-taskclassification',
    ## 2: 'dual-taskprobe'
    contrasts_to_use['ds011'][3]=[1]

    ## ## ds011 task004 Classification_probe_without_feedback
    ## 1: 'correctclassificationofsingle-taskitems'
    ## 2: 'correctclassificationofdual-taskitems
    ## 5: all
    contrasts_to_use['ds011'][4]=[5]


    ## ## ds017 task002 selective_stop-signal_task
    ## 1: 'go-critical'
    ## 2: 'go-noncritical'
    contrasts_to_use['ds017A'][2]=[1]

    ## ## ds051 task001 abstract-concrete_judgment
    ## 17: 'all'
    ## 18: 'novel_vs_repeat'
    contrasts_to_use['ds051'][1]=[18]

    ## ## ds052 task001 weather_prediction
    ## 1: 'positivefeedback',
    ## 2: 'negativefeedback'
    contrasts_to_use['ds052'][1]=[1]

    ## ## ds052 task002 reversal_weather_prediction
    ## 1: 'positivefeedback'
    ## 2: 'negativefeedback'
    contrasts_to_use['ds052'][2]=[2]

    ## ## ds101 task001 Simon_task
    ## 7: 'incongruent_vs_congruent'
    ## 8: 'incorrect_vs_correct
    contrasts_to_use['ds101'][1]=[8]

    ## ## ds102 task001 flanker_task
    ## 7: 'incongruent_vs_congruent'
    ## 8: 'incorrect_vs_correct
    contrasts_to_use['ds102'][1]=[7]

    ## ## ds107 task001 one-back_task
    ## 6: 'objects_vs_scrambled'
    ## 7: 'words_vs_consonants'
    contrasts_to_use['ds107'][1]=[6]

    return contrasts_to_use
