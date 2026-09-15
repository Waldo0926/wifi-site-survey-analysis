# Sanitised survey data

The CSV in this directory is a deliberately sanitised derivative of measurements collected for a university wireless-networking exercise.

Privacy/safety changes:

- real BSSIDs/MAC addresses are removed;
- the real building, floor plan, room names and gateway address are omitted;
- APs are renamed `AP-A` through `AP-D`;
- measurement locations are abstract labels `A` through `I`;
- no packet captures, account identifiers, student information or campus-infrastructure details are included.

`radio_id` distinguishes radios/BSSIDs that belong to the same physical AP. The analysis collapses those radios by `physical_ap` before assessing roaming overlap so that two radios on one device are not incorrectly treated as two roaming candidates.
