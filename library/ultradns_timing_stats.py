#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, Daniel Haskin
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: ultradns_timing_stats
short_description: Extract and analyze timing statistics from UltraDNS quiz application logs
version_added: "1.0.0"
description:
    - Parses log files to find timing information from UltraDNS quiz application
    - Extracts the last N timing measurements from log entries
    - Calculates mean and standard deviation of timing values
    - Returns structured statistical data for monitoring purposes
options:
    log_file:
        description:
            - Path to the log file to analyze
        required: true
        type: str
    sample_size:
        description:
            - Number of most recent timing entries to analyze
        required: false
        type: int
        default: 20
author:
    - Daniel Haskin
'''

EXAMPLES = r'''
# Analyze the last 20 timing entries from the default log file
- name: Get UltraDNS timing statistics
  ultradns_timing_stats:
    log_file: /var/log/ultradns-quiz-madeup.log
    
# Analyze the last 50 timing entries
- name: Get UltraDNS timing statistics with larger sample
  ultradns_timing_stats:
    log_file: /var/log/ultradns-quiz-madeup.log
    sample_size: 50
'''

RETURN = r'''
mean:
    description: The arithmetic mean of the timing values in milliseconds
    type: float
    returned: always
    sample: 112.5
stddev:
    description: The standard deviation of the timing values in milliseconds
    type: float
    returned: always
    sample: 15.3
sample_count:
    description: The actual number of timing values found and analyzed
    type: int
    returned: always
    sample: 20
timings:
    description: List of all timing values extracted (in milliseconds)
    type: list
    elements: int
    returned: always
    sample: [125, 113, 112, 25, 115]
log_file:
    description: The log file that was analyzed
    type: str
    returned: always
    sample: /var/log/ultradns-quiz-madeup.log
'''

import re
import math
from ansible.module_utils.basic import AnsibleModule


def extract_timings(log_file, sample_size):
    """
    Extract timing values from the log file.
    
    Searches for lines matching the pattern:
    [YYYY-MM-DD HH:MM:SS,mmm] INFO Ultradns quiz application took XX ms
    
    Args:
        log_file: Path to the log file
        sample_size: Number of most recent entries to return
        
    Returns:
        List of timing values (as integers) in chronological order
    """
    # Pattern to match: [timestamp] INFO Ultradns quiz application took XX ms
    pattern = re.compile(r'\[[\d\-: ,]+\]\s+INFO\s+Ultradns quiz application took\s+(\d+)\s+ms')
    
    timings = []
    
    try:
        with open(log_file, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    timing_value = int(match.group(1))
                    timings.append(timing_value)
    except IOError as e:
        raise IOError(f"Failed to read log file {log_file}: {str(e)}")
    
    # Return the last N entries
    return timings[-sample_size:] if len(timings) > sample_size else timings


def calculate_mean(numbers):
    """
    Calculate the arithmetic mean of a list of numbers.
    
    Args:
        numbers: List of numeric values
        
    Returns:
        The mean as a float
    """
    if not numbers:
        return 0.0
    
    total = sum(numbers)
    return float(total) / len(numbers)


def calculate_stddev(numbers, mean):
    """
    Calculate the standard deviation of a list of numbers.
    
    Uses the formula: sqrt(sum((x - mean)^2) / n)
    
    Args:
        numbers: List of numeric values
        mean: The pre-calculated mean of the numbers
        
    Returns:
        The standard deviation as a float
    """
    if not numbers:
        return 0.0
    
    sum_of_squares = 0.0
    for number in numbers:
        sum_of_squares += (number - mean) ** 2
    
    return math.sqrt(sum_of_squares / len(numbers))


def run_module():
    """
    Main module execution function.
    """
    # Define module arguments
    module_args = dict(
        log_file=dict(type='str', required=True),
        sample_size=dict(type='int', required=False, default=20)
    )

    # Initialize result dictionary
    result = dict(
        changed=False,
        mean=0.0,
        stddev=0.0,
        sample_count=0,
        timings=[],
        log_file=''
    )

    # Create the module object
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract parameters
    log_file = module.params['log_file']
    sample_size = module.params['sample_size']

    # Validate sample_size
    if sample_size <= 0:
        module.fail_json(msg='sample_size must be a positive integer', **result)

    try:
        # Extract timing values from the log file
        timings = extract_timings(log_file, sample_size)
        
        # Check if we found any timing entries
        if not timings:
            module.fail_json(
                msg=f'No timing entries found in log file {log_file}',
                **result
            )
        
        # Calculate statistics
        mean = calculate_mean(timings)
        stddev = calculate_stddev(timings, mean)
        
        # Populate result
        result['mean'] = mean
        result['stddev'] = stddev
        result['sample_count'] = len(timings)
        result['timings'] = timings
        result['log_file'] = log_file
        
        # Module succeeded
        module.exit_json(**result)
        
    except IOError as e:
        module.fail_json(msg=str(e), **result)
    except Exception as e:
        module.fail_json(msg=f'Unexpected error: {str(e)}', **result)


def main():
    run_module()


if __name__ == '__main__':
    main()
