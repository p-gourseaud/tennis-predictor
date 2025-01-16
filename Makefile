make_database:
	python pipelines/1_make_tennis_atp_database.py
	python pipelines/2_compute_elo.py

