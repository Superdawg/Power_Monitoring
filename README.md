# Power_Monitoring
Notifications for power events from connected APC UPS

# DEPENDENCIES
- This requires python3
- This requires python3 lib called 'apcaccess'.  Install by running `pip3 install apcaccess`

# INSTALL
- Clone this repository `git clone https://github.com/Superdawg/Power_Monitoring.git`
- Update power_check.service to use a valid email address and/or relay host.
- Run the install operation as root.  `sudo make install`
- Verify that the timer actually got implemented `sudo systemctl list-timers --all` (You should see a line for UNIT power_check.timer)

# KNOWN ISSUES
- If you run this on something other than a debian-like system (i.e. CentOS/RHEL, etc.), then you will need to change the group from 'nogroup' to something else like 'nobody'
