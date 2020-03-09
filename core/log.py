from core.projection import __project__

# global ACTIVE_SESSIONS
# ACTIVE_SESSIONS = ["log"]

def __log__(*args, **kwargs):
	if args:
		print('log:')
		print('\t', *args, '\n')

	for session, text in kwargs.items():
		# if session in ACTIVE_SESSIONS:
		print(f'{session}:\t', f'{text}\n')
		__project__('log', **{session: text})



