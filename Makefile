make_database:
	python src/tennis_predictor/data/pipelines/1_make_tennis_atp_database.py
	python src/tennis_predictor/data/pipelines/2_compute_elo.py
	python src/tennis_predictor/data/pipelines/3_make_player_shortnames.py
	python src/tennis_predictor/data/pipelines/4_join_player_odds.py
	python src/tennis_predictor/data/pipelines/5_join_rank.py
	python src/tennis_predictor/data/pipelines/6_train_test_split.py
	python src/tennis_predictor/data/pipelines/7_predict.py
	python src/tennis_predictor/data/pipelines/8_evaluate.py
