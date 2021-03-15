import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

import plotly
import plotly.express as px
import time


dfY = pd.read_csv("/Users/carrot/Dropbox/PJT/youtube3_python/300_pannels/results/all/keyword_trend_Yr.csv")
dfM = pd.read_csv("/Users/carrot/Dropbox/PJT/youtube3_python/300_pannels/results/all/keyword_trend_Mn.csv")
dfW = pd.read_csv("/Users/carrot/Dropbox/PJT/youtube3_python/300_pannels/results/all/keyword_trend_Wk.csv")
df = dfY


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Label("카테고리:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id = 'categories_dpdn',
        options = [{'label': s, 'value': s} for s in sorted(df.ch_category.unique())],
        value = sorted(df.ch_category.unique())[0],
        clearable = False
    ),

    html.Label("키워드:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(id = 'keywords_dpdn', options=[], multi=True),

    html.Label("시간주기:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id = 'timeUnit_dpdn', 
        options=[{'label': '년간', 'value': 'perYear'},
                 {'label': '월간', 'value': 'perMonth'},
                 {'label': '주간', 'value': 'perWeek'}],
        value = 'perMonth',
        clearable = False
    ),

    dcc.Graph(id = 'fig_videoProd_trend', figure={})
])

@app.callback(
    Output('keywords_dpdn', 'options'),
    Input('categories_dpdn', 'value')
)
def set_keywords_options(chosen_category):
    dff = df[df.ch_category == chosen_category]
    print([{'label': c, 'value': c} for c in sorted(dff.keyword.unique())])
    return [{'label': c, 'value': c} for c in sorted(dff.keyword.unique())]

@app.callback(
    Output('keywords_dpdn', 'value'),
    Input('keywords_dpdn', 'options')
)
def set_keywords_value(available_options):
    return [x['value'] for x in available_options]

@app.callback(
    Output('fig_videoProd_trend', 'figure'),
    Input('categories_dpdn', 'value'),
    Input('keywords_dpdn', 'value'),
    Input('timeUnit_dpdn', 'value')
)
def update_videoProd_trend(selected_category, selected_keywords, timeUnit):
    print("*****그래프 상태확인****")
    # print(selected_category)
    # print(selected_keywords)
    # print(timeUnit)

    if len(selected_keywords) == 0:
        return dash.no_update
    else:
        if timeUnit == 'perMonth':
            df = dfM
            dtick= 'M1' # 1개월
        elif timeUnit =='perWeek':
            df = dfW
            dtick = 86400000*7 # 7일 (=1000ms*3600초*24시간*7일)
        else:
            df = dfY
            dtick = 'M12' # 12개월
        # print(df)

        dff = df[(df.ch_category==selected_category) & (df.keyword.isin(selected_keywords))].copy()
        dff = dff[(dff.time >= "2018-01-01") & (dff.time <= "2021-02-01")]
        print(dff.head())
        # print('1',dff.keyword.unique())
        time.sleep(0.1)

        fig = px.line(
            data_frame=dff,
            x='time',
            y='video_count',
            color='keyword',
            hover_name='keyword',
            hover_data={'keyword': False},
            labels={'time': '시간',
                    'video_count':'동영상수'}
        )
        # print('2',dff.keyword.unique())

        fig.update_xaxes(
            type = "date",
            tick0 = '2018-01-01',
            dtick = dtick, 
            tickangle = 90,
            tickfont = {'size': 8}
        )

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)

