all: edit_dialog_ui.py paperless_ui.py

edit_dialog_ui.py: edit_dialog.ui
	pyuic4 $^ > $@

paperless_ui.py: paperless.ui
	pyuic4 $^ > $@

clean:
	@rm -f edit_dialog_ui.py paperless_ui.py *.pyc

test:
	python2.7 setup.py test
