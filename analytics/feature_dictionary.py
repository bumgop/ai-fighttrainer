FEATURE_DICTIONARY = {
    # Anti-Air Reaction Test Features
    'anti_air_reaction_test_success_rate': {
        'description': 'Proportion of attempts with correct timing',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = better timing accuracy'
    },
    'anti_air_reaction_test_early_rate': {
        'description': 'Proportion of attempts with premature input',
        'units': 'ratio (0-1)', 
        'range': '[0, 1]',
        'interpretation': 'Higher = tendency to rush inputs'
    },
    'anti_air_reaction_test_late_rate': {
        'description': 'Proportion of attempts with delayed input',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = slow reaction time'
    },
    'anti_air_reaction_test_miss_rate': {
        'description': 'Proportion of attempts with no input',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = failure to recognize threats'
    },
    'anti_air_reaction_test_timing_error_mean': {
        'description': 'Average timing offset from optimal window',
        'units': 'milliseconds',
        'range': '[-150, 150]',
        'interpretation': 'Closer to 0 = more precise timing'
    },
    'anti_air_reaction_test_timing_error_std': {
        'description': 'Consistency of timing across attempts',
        'units': 'milliseconds',
        'range': '[0, 100]',
        'interpretation': 'Lower = more consistent timing'
    },
    
    # Hit-Confirm Test Features
    'hit_confirm_test_correct_rate': {
        'description': 'Proportion of correct confirm/block decisions',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = better decision-making under uncertainty'
    },
    'hit_confirm_test_false_confirm_rate': {
        'description': 'Proportion of blocked hits incorrectly confirmed',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = tendency to autopilot confirm'
    },
    'hit_confirm_test_missed_confirm_rate': {
        'description': 'Proportion of confirmed hits not followed up',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = overly conservative play'
    },
    'hit_confirm_test_decision_error_rate': {
        'description': 'Overall decision error rate',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = poor hit-confirm discipline'
    },
    
    # Whiff Punish Test Features
    'whiff_punish_test_correct_rate': {
        'description': 'Proportion of attacks punished during recovery',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = better frame data knowledge'
    },
    'whiff_punish_test_early_rate': {
        'description': 'Proportion of punish attempts during startup',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = impatience or poor recognition'
    },
    'whiff_punish_test_unsafe_rate': {
        'description': 'Proportion of punish attempts during active frames',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = dangerous timing errors'
    },
    'whiff_punish_test_late_rate': {
        'description': 'Proportion of punish attempts after recovery',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = slow recognition or execution'
    },
    'whiff_punish_test_miss_rate': {
        'description': 'Proportion of whiffs not punished at all',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = missed opportunities'
    },
    'whiff_punish_test_window_offset_mean': {
        'description': 'Average timing within recovery window',
        'units': 'milliseconds',
        'range': '[0, 300]',
        'interpretation': 'Lower = faster punish execution'
    },
    'whiff_punish_test_window_offset_std': {
        'description': 'Consistency of punish timing',
        'units': 'milliseconds', 
        'range': '[0, 150]',
        'interpretation': 'Lower = more consistent execution'
    },
    
    # Defense Under Pressure Features
    'defense_under_pressure_test_block_accuracy_mean': {
        'description': 'Average proportion of attacks blocked correctly',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = better mixup defense'
    },
    'defense_under_pressure_test_block_accuracy_std': {
        'description': 'Consistency of blocking across strings',
        'units': 'ratio',
        'range': '[0, 0.5]',
        'interpretation': 'Lower = more consistent defense'
    },
    'defense_under_pressure_test_error_rate_mean': {
        'description': 'Average proportion of attacks that hit',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Lower = better defensive fundamentals'
    },
    'defense_under_pressure_test_string_success_rate': {
        'description': 'Proportion of complete strings defended',
        'units': 'ratio (0-1)',
        'range': '[0, 1]',
        'interpretation': 'Higher = sustained defensive pressure handling'
    }
}

def get_feature_info(feature_name: str) -> dict:
    return FEATURE_DICTIONARY.get(feature_name, {
        'description': 'Unknown feature',
        'units': 'unknown',
        'range': 'unknown', 
        'interpretation': 'No interpretation available'
    })