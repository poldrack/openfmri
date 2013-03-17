# Makefile to run steps of analysis

# run featregapply on the datasets

0_run_featregapply:
	rm -f /corral-repl/utexas/poldracklab/openfmri/shared2/run_featregapply.sh
	find /corral-repl/utexas/poldracklab/openfmri/shared2/ds*/sub*/model/model001/task*_ru*.feat -maxdepth 0| sed 's/^/featregapply_zstat /'>/corral-repl/utexas/poldracklab/openfmri/shared2/run_featregapply.sh
	launch -s /corral-repl/utexas/poldracklab/openfmri/shared2/run_featregapply.sh -p 120 -r 01:00:00 -n featregapply


1_stage_zstats:

	python 1_stage_zstats.py
	launch -s get_all_zstats.sh -r 01:00:00 -p 120 -n getzstats

2_create_datafiles:
	python 2_create_datafiles.py