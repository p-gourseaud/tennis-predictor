make_database:
	python pipelines/1_make_tennis_atp_database.py
	python pipelines/2_compute_elo.py
	python pipelines/3_make_player_shortnames.py
	python pipelines/4_join_player_odds.py
	python pipelines/5_join_rank.py
