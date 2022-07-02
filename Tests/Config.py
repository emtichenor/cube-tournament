class Config:
    @staticmethod
    def get_options(test_mode, options=None):

        if not options:
            options = {"TEST_FLAG": False, "NO_INPUT_FLAG": False, "SAVE_FLAG": True, 'NO_SLEEP_FLAG' : False}
        if test_mode:
            options['TEST_FLAG'] = True
            options['NO_INPUT_FLAG'] = True
            options['NO_SLEEP_FLAG'] = True
            options['TEST_USER_QUALI'] = [60.0, 61.0, 62.0, 63.0, 64.0]
            options['TEST_USER_TIMES'] = [35.0, 35.0, 35.0, 35.0, 35.0]
            options['TEST_OPP_TIMES'] = [32.0, 32.0, 32.0, 32.0, 32.0]
            options['num_qualify'] = 8
        return options