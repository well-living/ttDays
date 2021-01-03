# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 12:44:12 2021

@author: ry8128
"""


# 日付処理
import datetime
import calendar

import pandas as pd

# 可視化
#import plotly.express as px
import plotly.graph_objects as go
# Webフレームワーク
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
#import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
from dash.dependencies import Input, Output, State

# 本日日付を取得
today = datetime.date.today()


# CSS
dash_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# Dashインスタンスを生成
app = dash.Dash(__name__, external_stylesheets=dash_stylesheets)

app.layout = html.Div(
    children=[
            # 2つ目のタブ
            dcc.Tab(
                children=[
                    html.Div(
                        children=[
                            dcc.Dropdown(
                                id="gender_dropdown",
                                options=[
                                    {"label": "未設定", "value": "未設定"},
                                    {"label": "男性", "value": "男性"},
                                    {"label": "女性", "value": "女性"},
                                ],
                                value="未設定",
                                style={
                                    "width": 200,
                                    ## マージン
                                    "margin-left": "20%",  #10% auto
                                    "margin-right": "20%",  #10% auto
                                    "margin-bottom": 10, 
                                    
                                    "text-align": "left",
                                    #"display": "inline-block",  # 横に並べて表示
                                },
                            ),
                            # 生年月日
                            html.H6(
                                children="あなたの生年月日は？",
                                style={
                                    # ボックス
                                    ## 幅
                                    "width": "60%",
                                    ## 高さ デフォルト
                                    ## マージン
                                    "margin-left": "20%",  #10% auto
                                    "margin-right": "20%",  #10% auto
                                    ## ボーダー なし
                                    ## パディング なし
                                },
                            ),
                           # 生年
                            dcc.Dropdown(
                                id="birth_year_dropdown",
                                options=[{"label": str(i)+"年", "value": str(i)+"年"} for i in range(1900, today.year+1)],
                                value="1990年",
                                style={
                                    "width": 200,
                                    "margin-left": "20%",  #10% auto
                                    "margin-right": "20%",  #10% auto
                                    "margin-bottom": 10, 
                                }
                            ),
                            # 月
                            dcc.Dropdown(
                                id="birth_month_dropdown",
                                options=[{"label": str(i)+"月", "value": str(i)+"月"} for i in range(1, 13)],
                                value="1月",
                                style={
                                    "width": 200,
                                    "margin-left": "20%",  #10% auto
                                    "margin-right": "20%",  #10% auto
                                    "margin-bottom": 10, 
                                }
                            ),
                            # 日
                            dcc.Dropdown(
                                id="birth_day_dropdown",
                                options=[{"label": str(i)+"日", "value": str(i)+"日"} for i in range(1, 32)],
                                value="1日",
                                style={
                                    "width": 200,
                                    "margin-left": "20%",  #10% auto
                                    "margin-right": "20%",  #10% auto
                                    "margin-bottom": 10, 
                                }
                            ),
                            # 年齢
                            html.H6(
                                children="あなたの年齢",
                                style={
                                    # ボックス
                                    # 幅
                                    #"width": "60%",
                                    # 高さ デフォルト
                                    # マージン
                                    "margin-left": "20%",  #10% auto
                                    #"margin-right": "20%",  #10% auto
                                    # ボーダー なし
                                    # パディング なし
                                    "display": "inline-block",  # 横に並べて表示
                                },
                            ),
                            html.H4(
                                children="",
                                id="age",
                                style={
                                    "margin-left": 10, 
                                    "display": "inline-block",  # 横に並べて表示
                                },
                            ),
                            # 生まれて何日目
                            html.Button(
                                id="ttDays",
                                n_clicks=0,
                                children="設定完了",
                                style={
                                    #"width": 20,
                                    "margin-left": "25%",  #10% auto
                                    #"margin-right": "20%",  #10% auto
                                    #"margin-top": 10, 
                                    "display": "block",
                                }
                            ),
                            html.H3(
                                id="how_many_days",
                                style={
                                    "margin-left": "20%",
                                }
                            ),
                            html.H3(
                                id="ten_thousand_days",
                                style={
                                    "margin-left": "20%",
                                }
                            ),
                            html.H3(
                                id="twenty_thousand_days",
                                style={
                                    "margin-left": "20%",
                                }
                            ),
                            html.H3(
                                id="thirty_thousand_days",
                                style={
                                    "margin-left": "20%",
                                }
                            ),
                        ],
                        style={
                            "margin": "auto"
                        }
                    ), # Tabの中のDivの終わり
                ],# Tabの中のchildrenの終わり
                id="personal",
                label="個人設定",
            ),
    ],  # layoutDivのchildrenの閉じ括弧
    id="layout_div",
    # CSSのプロパティとPプロパティ値を設定
    style={
    },  # layoutDivのstyleの閉じ括弧
)


## 生年月日から年齢を計算する
@app.callback(
    Output(component_id="birth_day_dropdown", component_property="options"),
    Output(component_id="age", component_property="children"),
    Input(component_id="birth_year_dropdown", component_property="value"),
    Input(component_id="birth_month_dropdown", component_property="value"),
    Input(component_id="birth_day_dropdown", component_property="value"),
)
def CalcAge(year, month ,day):
    """
    year: str or None
    month: str or None
    day: str or None
    ありえない日にち(2/30など)になってないか
    """
    # 
    age = ""
    if (type(year) == str) & (type(month) == str):
        year = int(year[:-1])
        month = int(month[:-1])
        end_month = calendar.monthrange(year, month)[1]
        options_days = [{"label": str(i)+"日", "value": str(i)+"日"} for i in range(1, end_month+1)]
        if type(day) == str:
            day = int(day[:-1])
            if day <= end_month:
                birthday = datetime.date(year, month, day)
                age = today.year - birthday.year
                if (today.month < birthday.month) | ((today.month==birthday.month)&(today.day<birthday.day)):
                    age -= 1
                age = str(age) + "歳"
    else:
        options_days = [{"label": str(i)+"日", "value": str(i)+"日"} for i in range(1, 29)]
    return options_days, age

## ttDays
@app.callback(
    Output(component_id="how_many_days", component_property="children"),
    Output(component_id="ten_thousand_days", component_property="children"),
    Output(component_id="twenty_thousand_days", component_property="children"),
    Output(component_id="thirty_thousand_days", component_property="children"),
    Input(component_id="ttDays", component_property="n_clicks"),
    State(component_id="birth_year_dropdown", component_property="value"),
    State(component_id="birth_month_dropdown", component_property="value"),
    State(component_id="birth_day_dropdown", component_property="value"),
    
)
def ttDays(n_clicks, year, month ,day):
    how_many_days_msg = ""
    ten_thousand_days_msg = ""
    twenty_thousand_days_msg = ""
    thirty_thousand_days_msg = ""
    if n_clicks:
        if (type(year) == str) & (type(month) == str) & (type(day) == str):
            year = int(year[:-1])
            month = int(month[:-1])
            day = int(day[:-1])
            end_month = calendar.monthrange(year, month)[1]
            if day <= end_month:
                birthday = datetime.date(year, month, day)
                how_many_days = datetime.date.today() - birthday
                how_many_days_msg = '今日は生まれて' + str(how_many_days.days) + '日目'
                ten_thousand_days = birthday + datetime.timedelta(days=9999)
                twenty_thousand_days = birthday + datetime.timedelta(days=19999)
                thirty_thousand_days = birthday + datetime.timedelta(days=29999)
                ten_thousand_days_msg = '生まれて１万日目は、%d年%d月%d日' % (ten_thousand_days.year, ten_thousand_days.month, ten_thousand_days.day)
                twenty_thousand_days_msg = '生まれて２万日目は、%d年%d月%d日' % (twenty_thousand_days.year, twenty_thousand_days.month, twenty_thousand_days.day)
                thirty_thousand_days_msg = '生まれて３万日目は、%d年%d月%d日' % (thirty_thousand_days.year, thirty_thousand_days.month, thirty_thousand_days.day)
            else:
                how_many_days_msg = "生年月日を入力してください"
        else:
            how_many_days_msg = "生年月日を入力してください"
    return how_many_days_msg, ten_thousand_days_msg, twenty_thousand_days_msg, thirty_thousand_days_msg




if __name__ == "__main__":
    app.run_server(debug=True)


