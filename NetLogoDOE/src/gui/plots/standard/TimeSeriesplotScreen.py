import PySimpleGUI as sg
import plotly.graph_objects as go
import plotly.express as px
from plotly.colors import hex_to_rgb
import numpy as np
from NetLogoDOE.src.util.data_processing.merge_standard_data import merge_data
from NetLogoDOE.src.gui.custom_components import title, question_mark, metric3_radio_buttons


class TimeSeriesplotScreen:

    def __init__(self):
        question_mark_padding = ((0, 0), (0, 0))
        self.layout = [[title('Timeseries plot')],
                       [sg.Text('Graph Title'), sg.Input(key='timeseries_title_input')],
                       [sg.Text('Reporters to plot:'), question_mark('Help', padding=question_mark_padding)],
                       [sg.Multiline('', key='timeseries_reporter_input')],
                       [sg.Text('Only input a single reporter on each line')],
                       [sg.Text('Metric:'), question_mark('Help', padding=question_mark_padding)],
                       metric3_radio_buttons('timeseries'),
                       [self.collapse([
                           [sg.Text('Type of variance indication:')],
                           [sg.Radio('None', 'timeseries_variancegroup', key='timeseries_variance_1'),
                            sg.Radio('Error Bars', 'timeseries_variancegroup', key='timeseries_variance_2'),
                            sg.Radio('Shaded areas', 'timeseries_variancegroup', key='timeseries_variance_3')]],
                           'timeseries_variance_radiobuttons')],
                       [sg.Button('Generate', key='timeseries_generate_button')],
                       [sg.Button('Back', key='timeseries_back_button')]]
        self.results = None

    def check_events(self, event, values, window):
        if event == 'standard_write_results_event':
            self.results = values['standard_write_results_event']

        if event == 'timeseries_metric_1':
            window['timeseries_variance_radiobuttons'].update(visible=True)
        if event in ('timeseries_metric_2', 'timeseries_metric_3'):
            window['timeseries_variance_radiobuttons'].update(visible=False)

        if event == 'timeseries_generate_button':
            self.generate_timeseries(values, window)
        if event == 'timeseries_back_button':
            window['timeseries_panel'].update(visible=False)
            window['standard_result_panel'].update(visible=True)

    def collapse(self, layout, key):
        return sg.pin(sg.Column(layout, key=key, visible=False))

    def generate_timeseries(self, values, window):
        reporters = self.format_reporters(values)
        metric = self.get_selected_radio_button(values, 'timeseries_metric', 3)
        variance = self.get_selected_radio_button(values, 'timeseries_variance', 3)
        merged_data = merge_data(self.results[1], metric)

        try:
            [merged_data[reporter] for reporter in reporters]
        except KeyError:
            window.write_event_value('show_error_window', 'Error in input: Invalid reporter name.\nPlease make '
                                                          'sure all reporters are valid with the current run '
                                                          'configuration.')
            return

        if variance > 1 and metric == 1:
            fig = self.generate_variance_figure(merged_data, variance, reporters)
        else:
            fig = go.Figure()
            for reporter in reporters:
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter))

        fig.update_layout(title=values['timeseries_title_input'])
        fig.update_xaxes(title_text='Ticks')
        fig.update_yaxes(title_text='Value')
        fig.show()

    def generate_variance_figure(self, merged_data, variance, reporters):
        fig = go.Figure()
        for reporter in reporters:
            zipped = list(zip(*self.results[1][reporter]))
            zipped_std = list(map(lambda x: np.std(x), zipped))

            if variance == 2:
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter,
                                         error_y=dict(
                                             type='data',
                                             symmetric=False,
                                             array=zipped_std,
                                             arrayminus=zipped_std)
                                         ))
            if variance == 3:
                plus_std = [x + zipped_std[i] for i, x in enumerate(merged_data[reporter])]
                minus_std = [x - zipped_std[i] for i, x in enumerate(merged_data[reporter])]
                fig.add_trace(go.Scatter(y=merged_data[reporter], mode='lines', name=reporter))
                fig.add_trace(go.Scatter(y=plus_std, showlegend=False,
                                         line=dict(width=0), hoverinfo='skip'))
                fig.add_trace(go.Scatter(y=minus_std, showlegend=False,
                                         fill='tonexty',
                                         fillcolor=f"rgba{(*hex_to_rgb(px.colors.qualitative.Plotly[0]), 0.2)}",
                                         line=dict(width=0), hoverinfo='skip'))

        return fig

    def get_selected_radio_button(self, values, prefix, n):
        for i in range(n):
            if values[f'{prefix}_{i + 1}']:
                return i + 1
        return 1

    def format_reporters(self, values):
        reporters = list(filter(('').__ne__, values['timeseries_reporter_input'].split('\n')))
        reporters = list(map(lambda x: x.strip(), reporters))
        return reporters

    def validate_user_input(self, values):
        if values['timeseries_reporter_input'] == '\n':
            return False, 'Error in input: One or more fields are empty. ' \
                          'Please make sure all options are filled out.'

        return True, ''
