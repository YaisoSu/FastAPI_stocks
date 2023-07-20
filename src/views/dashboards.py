from datetime import datetime, timedelta

import plotly.graph_objs as go

from src.parsers.currencies_fetch import get_historical_currency_data
from fastapi import APIRouter, Response

router = APIRouter(
    tags=['dashboard']
)


@router.get("/forex_chart/")
async def forex_chart():
    days_to_display = 14
    dates = [(datetime.now() - timedelta(days=days_to_display) + timedelta(n)).strftime("%Y-%m-%d")
             for n in range(days_to_display)]
    eur = "EUR"
    usd = "USD"
    mxn = "MXN"

    usd_to_eur = await get_historical_currency_data(dates, eur, [usd])
    mxn_to_eur = await get_historical_currency_data(dates, eur, [mxn])
    usd_rates = [data.rates['USD'] for data in usd_to_eur]
    mxn_rates = [data.rates['MXN'] for data in mxn_to_eur]
    data = [
        go.Scatter(x=dates, y=usd_rates, mode='lines', name='EUR to USD'),
        go.Scatter(x=dates, y=mxn_rates, mode='lines', name='EUR to MXN')
    ]

    layout = go.Layout(
        title=f'Forex rates over the last {days_to_display}',
        xaxis=dict(title='Date'),
        yaxis=dict(
            title='Rate',
            tick0=0,
            dtick=0.5
        )
    )

    fig = go.Figure(data=data, layout=layout)
    return Response(content=fig.to_html(), media_type="text/html")
