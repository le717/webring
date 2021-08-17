# 1.0.3

_Unreleased_

- Escape link info on update

# 1.0.2

_Released August 16, 2021_

- Remove auto linkrot check on link add/update
- Fallback to text log for linkrot events if Discord logging is disabled
- Linkrot event messages are more informative
- Update dead link title to indicate Web Archive link when available
- Update link title to remove Web Archive link if revived
- Fix inconsistent linkrot status record cleanup
- Switch to Alpine Linux Python container

# 1.0.1

_Released August 13, 2021_

- Fix one-off error with `TIMES_FAILED_THRESHOLD`
- Fix linkrot record count not being deleted on status "yes"
- Add `pytest` based testing
