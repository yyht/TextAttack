import math
import torch

from textattack.constraints import Constraint

class LanguageModelConstraint(Constraint):
    """ 
        Determines if two sentences have a swapped word that has a similar
            probability according to a language model.
        
        Args:
            max_log_prob_diff (float): the maximum difference in log-probability
                between x and x_adv
    """
    
    def __init__(self, max_log_prob_diff=None):
        if max_log_prob_diff is None:
            raise ValueError('Must set max_log_prob_diff')
        self.max_log_prob_diff = max_log_prob_diff
    
    def get_log_probs_at_index(self, text_list, word_index):
        """ Gets the log-probability of items in `text_list` at index 
            `word_index` according to a language model.
        """
        raise NotImplementedError()
    
    def _check_constraint(self, x, x_adv, original_text=None):
        try:
            indices = x_adv.attack_attrs['newly_modified_indices']
        except KeyError:
            raise KeyError('Cannot apply language model constraint without `newly_modified_indices`')

        for i in indices:
            probs = self.get_log_probs_at_index((x, x_adv), i)
            if len(probs) != 2:
                raise ValueError(f'Error: get_log_probs_at_index returned {len(probs)} values for 2 inputs')
            x_prob, x_adv_prob = probs
            if self.max_log_prob_diff is None:
                x_prob, x_adv_prob = math.log(p1), math.log(p2)
            if abs(x_prob - x_adv_prob) > self.max_log_prob_diff:
                return False
        
        return True
    
    def extra_repr_keys(self):
        return ['max_log_prob_diff']
