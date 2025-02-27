help:
	@echo "start_db - start postgres"
test_db:
	@pytest -m connect_db_rules 
test_infrastructure:
	@pytest -m interface_rules
test_api:
	@pytest -m api_rules
