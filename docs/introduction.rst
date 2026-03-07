Introduction
============

Overview
--------

The UltraDNS quiz application is a critical component of the DNS infrastructure,
responsible for processing and responding to DNS queries. Monitoring its
performance is essential for ensuring reliable service delivery.

This project provides a custom Ansible module and playbook for analyzing timing
statistics from the UltraDNS quiz application logs. By extracting and analyzing
response times, operations teams can:

- Identify performance degradation early
- Compare performance across servers
- Set up automated alerting for anomalies
- Track performance trends over time

Log Format
----------

The UltraDNS quiz application logs timing information in the following format:

::

    [2021-07-01 00:01:44,726] INFO Ultradns quiz application took 125 ms

The log entries contain:

- **Timestamp**: Date and time of the operation (YYYY-MM-DD HH:MM:SS,mmm)
- **Log Level**: INFO
- **Application**: "Ultradns quiz application"
- **Timing**: Response time in milliseconds

Architecture
------------

The solution consists of three main components:

1. **Custom Ansible Module** (`ultradns_timing_stats`)

   Parses log files and extracts timing statistics. The module:
   - Reads the specified log file
   - Extracts all timing entries matching the expected pattern
   - Returns the last N entries (configurable, default 20)
   - Calculates mean and standard deviation
   - Returns structured data for further processing

2. **Ansible Playbook** (`ultradns_timing_monitor.yml`)

   Automates the collection and analysis of timing statistics across multiple
   servers. The playbook:
   - Targets all quiz.example.vercara servers
   - Collects timing statistics from each server
   - Displays per-server results
   - Provides optional alerting for high response times
   - Generates summary reports

3. **Sphinx Documentation**

   Comprehensive documentation for the module and playbook, including:
   - API reference
   - Usage examples
   - Installation instructions
   - Best practices

Requirements
------------

- Python 3.6+
- Ansible 2.9+
- Sphinx 4.0+ (for building documentation)
