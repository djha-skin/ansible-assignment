# UltraDNS Timing Statistics Monitoring

This project provides tools for monitoring and analyzing the performance of the UltraDNS quiz application across multiple servers.

## Components

### Custom Ansible Module

The `ultradns_timing_stats` module parses log files to extract timing information from the UltraDNS quiz application and calculates statistical metrics.

**Features:**
- Extracts timing values from log entries matching the pattern `[TIMESTAMP] INFO Ultradns quiz application took XX ms`
- Calculates mean response time
- Calculates standard deviation of response times
- Configurable sample size for analysis
- Graceful error handling for missing files or malformed logs

### Ansible Playbook

The `ultradns_timing_monitor.yml` playbook automates the collection and analysis of timing statistics across multiple servers.

**Features:**
- Targets all quiz.example.vercara servers
- Collects timing statistics from each server
- Displays per-server results
- Provides optional alerting for high response times or variability
- Generates summary reports

### Documentation

Sphinx-generated documentation provides:
- Module reference documentation
- Usage examples
- Installation instructions
- Monitoring best practices

## Installation

### Prerequisites

- Python 3.6+
- Ansible 2.9+
- Sphinx 4.0+ (for building documentation)

### Setting Up the Module

1. Copy the module to your Ansible library path:

```bash
cp library/ultradns_timing_stats.py /usr/share/ansible/plugins/modules/
```

Or use the `library` directive in your playbook:

```yaml
- name: Gather UltraDNS Timing Statistics
  hosts: quiz_servers
  library: ./library
  tasks:
    - ultradns_timing_stats:
        log_file: /var/log/ultradns-quiz-madeup.log
```

### Setting Up the Playbook

1. Copy the playbook to your Ansible plays directory:

```bash
cp tasks/ultradns_timing_monitor.yml /etc/ansible/plays/
```

2. Configure your inventory file with the quiz servers:

```ini
[quiz_servers]
server00.quiz.example.vercara
server01.quiz.example.vercara
server02.quiz.example.vercara
server03.quiz.example.vercara
server04.quiz.example.vercara
server05.quiz.example.vercara
```

## Usage

### Running the Playbook

```bash
# Run with default inventory
ansible-playbook -i inventory tasks/ultradns_timing_monitor.yml

# Run with specific tags
ansible-playbook -i inventory tasks/ultradns_timing_monitor.yml --tags timing

# Run in check mode (dry run)
ansible-playbook -i inventory tasks/ultradns_timing_monitor.yml --check
```

### Using the Module Directly

```bash
# Test the module locally
ansible localhost -m ultradns_timing_stats -a "log_file=/path/to/log.log sample_size=20"
```

## Building Documentation

To build the Sphinx documentation locally:

```bash
cd docs
make html
```

The generated HTML documentation will be in `docs/_build/html/`.

## GitHub Actions

This repository automatically builds and deploys documentation to GitHub Pages when changes are pushed to the main branch.

The workflow:
1. Checks out the repository
2. Sets up Python environment
3. Installs Sphinx and dependencies
4. Builds the documentation
5. Deploys to GitHub Pages

## Author

Daniel Haskin
