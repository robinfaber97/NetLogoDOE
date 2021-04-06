import PySimpleGUI as sg
import ast
from NetLogoDOE.src.util.Sampler import MonteCarloSampler, LatinHypercubeSampler, FullFactorialSampler, FASTSampler, \
    FiniteDifferenceSampler, SaltelliSampler, SobolSampler
from NetLogoDOE.src.util.config_dicts.get_experiment_dict import get_experiment_config_dictionary
from NetLogoDOE.src.gui.custom_components import title
from NetLogoDOE.src.gui.custom_components import question_mark


class ExperimentScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Experimental runs')],
                       [sg.Text('Experiment Name'), sg.Input(key='experiment_name_input'),
                        sg.Input(key='experiment_dummy_import', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import experiment', file_types=[("Text Files", "*.txt")],
                                      target='experiment_dummy_import', key='experiment_import_button')],
                       [sg.Text('Model file name'), sg.Input(key='experiment_model_input'),
                        sg.Input(key='experiment_model_dummy_import', enable_events=True, visible=False, size=(0, 0)),
                        sg.FileBrowse('Import model', file_types=[("NetLogo Files", "*.nlogo")],
                                      target='experiment_model_dummy_import', key='experiment_model_import_button')],
                       [sg.Text('Vary variables as follows:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline(key='experiment_bound_input')],
                       [sg.Text('Explain the format: variable-name lower-bound upper-bound')],
                       [sg.Text('Sampling method:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Radio('Monte Carlo', 'experiment_sampler_radiogroup', key='sample_mc'),
                        sg.Radio('Latin Hypercube', 'experiment_sampler_radiogroup', key='sample_lhs'),
                        sg.Radio('Full Factorial', 'experiment_sampler_radiogroup', key='sample_ff'),
                        sg.Radio('FAST', 'experiment_sampler_radiogroup', key='sample_fast'),
                        # sg.Radio('Finite Difference', 'experiment_sampler_radiogroup', key='sample_fd'),
                        #                         question_mark('Help', padding=question_mark_padding),
                        sg.Radio('Saltelli', 'experiment_sampler_radiogroup', key='sample_saltelli'),
                        sg.Radio('Sobol sequence', 'experiment_sampler_radiogroup', key='sample_ss')],
                       [sg.Text('Number of scenarios:'),
                        question_mark('Help', padding=question_mark_padding),
                        sg.Input('10', key='experiment_scenario_input')],
                       [sg.Text('Number of repetitions per scenario:'),
                        question_mark('Help', padding=question_mark_padding),
                        sg.Input('10', key='experiment_repetition_input')],
                       [sg.Text('Maximum number of ticks per run:'),
                        question_mark('Help', padding=question_mark_padding),
                        sg.Input('100', key='experiment_tick_input')],
                       [sg.Text('Measure runs using these reporters:'),
                        question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline(key='experiment_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [sg.Text('Setup commands:'),
                        question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline('setup', key='experiment_setup_input')],
                       [sg.Text('Number of parallel executors:'),
                        question_mark('Help', padding=question_mark_padding),
                        sg.Input('2', key='experiment_process_input')],
                       [sg.Button('Run', key="experiment_run_button")],
                       [sg.Button('Back', key="experiment_back_button"),
                        sg.Input(key='experiment_dummy_export', enable_events=True, visible=False, size=(0, 0)),
                        sg.SaveAs('Save Experiment', file_types=[("Text Files", "*.txt")],
                                  target='experiment_dummy_export', key="experiment_save_button")]]

    def check_events(self, event, values, window):
        if event == 'experiment_run_button':
            valid, error_message = self.validate_user_input(values)
            if not valid:
                window.write_event_value('show_error_window', error_message)
                return

            window['experiment_panel'].update(visible=False)
            window['run_panel'].update(visible=True)
            window.read(0.01)

            problem = self.construct_problem(values)
            param_values = self.get_param_values(problem, values)
            window.write_event_value('experiment_run_signal', (problem, param_values))

        if event == 'experiment_dummy_import' and not (values['experiment_dummy_import'] == ''):
            self.import_experiment(window, values['experiment_dummy_import'])
        if event == 'experiment_model_dummy_import' and not (values['experiment_model_dummy_import'] == ''):
            window['experiment_model_input'].update(values['experiment_model_dummy_import'])
        if event == 'experiment_dummy_export' and not (values['experiment_dummy_export'] == ''):
            self.export_experiment(values, values['experiment_dummy_export'])
        if event == 'experiment_back_button':
            window['main_panel'].update(visible=True)
            window['experiment_panel'].update(visible=False)

    def construct_problem(self, values):
        num_vars, names, bounds = self.get_problem_values(values['experiment_bound_input'])
        return {
            'num_vars': num_vars,
            'names': names,
            'bounds': bounds
        }

    def get_problem_values(self, bounds):
        rows = bounds.split('\n')
        rows = list(filter(('').__ne__, rows))
        split_rows = list(map(lambda x: x.split(' '), rows))
        names = list(map(lambda x: x[0], split_rows))
        bounds = list(map(lambda x: [int(x[1]), int(x[2])], split_rows))
        return len(rows), names, bounds

    def get_param_values(self, problem, values):
        keys = ['sample_mc', 'sample_lhs', 'sample_ff', 'sample_fast', 'sample_saltelli', 'sample_ss']#, 'sample_fd']
        scenarios = int(values['experiment_scenario_input'])
        for key in keys:
            if values[key]:
                param_values = []
                if key == 'sample_mc':
                    param_values = MonteCarloSampler().sample(problem, scenarios)
                elif key == 'sample_lhs':
                    param_values = LatinHypercubeSampler().sample(problem, scenarios)
                elif key == 'sample_ff':
                    param_values = FullFactorialSampler().sample(problem, scenarios)
                elif key == 'sample_fast':
                    param_values = FASTSampler().sample(problem, scenarios)
                elif key == 'sample_fd':
                    param_values = FiniteDifferenceSampler().sample(problem, scenarios)
                elif key == 'sample_saltelli':
                    param_values = SaltelliSampler().sample(problem, scenarios)
                elif key == 'sample_ss':
                    param_values = SobolSampler().sample(problem, scenarios)
                return param_values
        return LatinHypercubeSampler().sample(problem, scenarios)

    def import_experiment(self, window, file_path):
        f = open(file_path, "r")
        experiment_string = f.read()
        f.close()

        try:
            experiment_dict = ast.literal_eval(experiment_string)
            window['experiment_name_input'].update(experiment_dict['Experiment Name'])
            window['experiment_model_input'].update(experiment_dict['Model file'])
            window['experiment_bound_input'].update('\n'.join((experiment_dict['Variable bounds'])))
            window['experiment_scenario_input'].update(experiment_dict['Number of scenarios'])
            window['experiment_repetition_input'].update(experiment_dict['Repetitions'])
            window['experiment_tick_input'].update(experiment_dict['Ticks per run'])
            window['experiment_reporter_input'].update('\n'.join(experiment_dict['NetLogo reporters']))
            window['experiment_setup_input'].update('\n'.join(experiment_dict['Setup commands']))
            window['experiment_process_input'].update(experiment_dict['Parallel executors'])
        except (SyntaxError, KeyError, TypeError, IndexError):
            window.write_event_value('show_error_window', 'Invalid file syntax for experiment configuration')
            return

    def export_experiment(self, values, file_path):
        experiment_dict = get_experiment_config_dictionary(values)

        f = open(file_path, "w")
        f.write(str(experiment_dict))
        f.close()

    def validate_user_input(self, values):
        if values['experiment_model_input'] == '' or \
                values['experiment_bound_input'] == '\n' or \
                values['experiment_scenario_input'] == '' or \
                values['experiment_repetition_input'] == '' or \
                values['experiment_tick_input'] == '' or \
                values['experiment_reporter_input'] == '\n' or \
                values['experiment_setup_input'] == '\n' or \
                values['experiment_process_input'] == '':
            return False, 'Error in input: One or more field are empty. ' \
                          'Please make sure all options are filled out.'

        try:
            problem = self.construct_problem(values)
        except (IndexError, ValueError):
            return False, 'Error in input: Invalid variable bounds input. ' \
                          'Please make sure the correct format is used.'
        try:
            scenarios = int(values['experiment_scenario_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the number of scenarios. ' \
                          'Please make sure it\'s an integer.'
        try:
            repetitions = int(values['experiment_repetition_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the number of repetitions. ' \
                          'Please make sure it\'s an integer.'
        try:
            repetitions = int(values['experiment_tick_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the maximum number of ticks. ' \
                          'Please make sure it\'s an integer.'
        try:
            process_amount = int(values['experiment_process_input'])
        except ValueError:
            return False, 'Error in input: Invalid value for the number of executors. Please make sure it\'s an integer.'

        return True, ''