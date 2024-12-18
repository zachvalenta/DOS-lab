.PHONY: test export

help:
	@echo
	@echo "======================================================================"
	@echo
	@echo "🛠  UTILS"
	@echo
	@echo "flask:      start built-in Flask dev server"
	@echo "hc:         hit healthcheck"
	@echo
	@echo "📦 DEPENDENCIES"
	@echo
	@echo "venv:       show environment info"
	@echo "deps:       list prod dependencies"
	@echo
	@echo "======================================================================"
	@echo

#
# 🛠 UTILS
#

flask:
	poetry run flask run

hc:
	curl -w "\n" "http://127.0.0.1:5000"

#
# 📦 DEPENDENCIES
#

venv:
	poetry env info

deps:
	poetry show --tree --no-dev

