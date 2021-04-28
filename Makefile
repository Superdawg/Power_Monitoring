install:
	@echo Installing power_check.py
	install -m 0755 -o nobody -g nogroup power_check.py /usr/bin/power_check
	install -m 0644 -o root -g root power_check.timer /usr/lib/systemd/system/power_check.timer
	install -m 0644 -o root -g root power_check.service /usr/lib/systemd/system/power_check.service
	@echo Reloading systemd database
	-systemctl daemon-reload

start:
	@echo Enabling and starting the power_check timer.
	systemctl enable power_check.timer
	systemctl start power_check.timer
