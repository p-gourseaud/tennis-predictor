make_database:
	python src/tennis_predictor/data/pipelines/make_tennis_atp_db.py
	python src/tennis_predictor/data/pipelines/compute_elo.py
	python src/tennis_predictor/data/pipelines/make_player_shortnames.py
	python src/tennis_predictor/data/pipelines/join_player_odds.py
	python src/tennis_predictor/data/pipelines/join_rank.py
	python src/tennis_predictor/data/pipelines/make_features.py
	python src/tennis_predictor/data/pipelines/train_test_split.py
	python src/tennis_predictor/data/pipelines/augment_data.py

make_train:
	python src/tennis_predictor/models/train.py

make_prediction:
	python src/tennis_predictor/models/predict.py

make_evaluation:
	python src/tennis_predictor/models/evaluate.py

make_all: make_database make_train make_prediction make_evaluation
