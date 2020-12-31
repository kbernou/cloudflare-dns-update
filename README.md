# cloudflare-dns-update
Updates the DNS records for a specific zone in Cloudflare. Meant to be ran intermittently. Probably best to keep for personal use only, for those of us without access to a static IP.

## Short form
* Get public IP
* Compare to public IP from last run
* If last and current are the same, exit
* Otherwise, update all A records for the zone in Cloudflare
* Log failures, if any
* If all records were successfully updated, update the IP file

## Long form
Updates all the A records in a zone in Cloudflare with the new external IP. Using a locally updated file, will only update records if the external IP has changed from the last run, and will only update the file if all records are updated successfully. Also logs failures. Should probably do some truncation on that front.

## Requirements
* Python 3
* Requests
