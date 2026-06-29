import plotly.express as px

def claims_chart(data):

    fig = px.line(
        data,
        x="Day",
        y="Claims",
        markers=True,
        title="Claims Trend"
    )

    fig.update_layout(height=350)

    return fig


def status_chart(data):

    fig = px.pie(
        data,
        names="Status",
        values="Count",
        hole=.45,
        title="Review Status"
    )

    fig.update_layout(height=350)

    return fig