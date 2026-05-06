import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(page_title="ESG Emissions Dashboard", layout="wide")


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
	data = pd.read_csv(path)
	return data


def add_period_sort(df: pd.DataFrame) -> pd.DataFrame:
	period_parts = df["Reporting Period"].str.extract(
		r"(?P<Year>\d{4})\sQ(?P<Quarter>[1-4])"
	)
	df = df.copy()
	df["Year"] = period_parts["Year"].astype(int)
	df["Quarter"] = period_parts["Quarter"].astype(int)
	df["PeriodSort"] = df["Year"] * 10 + df["Quarter"]
	return df


st.title("ESG Emissions Dashboard")

data_path = "ESG Data Analytics Task.cleaned.csv"
df = load_data(data_path)
df = add_period_sort(df)

st.sidebar.header("Filters")
facility_options = sorted(df["Facility Name"].unique())
scope_options = sorted(df["Scope"].unique())
period_options = sorted(df["Reporting Period"].unique())

selected_facilities = st.sidebar.multiselect(
	"Facility", facility_options, default=facility_options
)
selected_scopes = st.sidebar.multiselect(
	"Scope", scope_options, default=scope_options
)
selected_periods = st.sidebar.multiselect(
	"Reporting Period", period_options, default=period_options
)

filtered = df[
	df["Facility Name"].isin(selected_facilities)
	& df["Scope"].isin(selected_scopes)
	& df["Reporting Period"].isin(selected_periods)
]

if filtered.empty:
	st.warning("No data for the selected filters.")
	st.stop()

# KPI Cards
total_emissions = filtered["Emissions (tons)"].sum()
facility_totals = (
	filtered.groupby("Facility Name")["Emissions (tons)"].sum()
)
top_facility = facility_totals.idxmax()
top_facility_value = facility_totals.max()

quarter_totals = (
	filtered.groupby("Reporting Period")["Emissions (tons)"].sum()
)
avg_quarter_emissions = quarter_totals.mean()

scope_totals = filtered.groupby("Scope")["Emissions (tons)"].sum()
top_scope = scope_totals.idxmax()
top_scope_value = scope_totals.max()

kpi_cols = st.columns(4)
kpi_cols[0].metric("Total Emissions", f"{total_emissions:,.0f}")
kpi_cols[1].metric(
	"Highest Emitting Facility", top_facility, f"{top_facility_value:,.0f}"
)
kpi_cols[2].metric("Average Quarterly Emissions", f"{avg_quarter_emissions:,.0f}")
kpi_cols[3].metric("Scope with Highest Emissions", top_scope, f"{top_scope_value:,.0f}")

st.subheader("Quarterly Trend")
quarter_df = (
	filtered.groupby(["Reporting Period", "PeriodSort"])["Emissions (tons)"]
	.sum()
	.reset_index()
	.sort_values(by="PeriodSort")
)
fig_trend = px.line(
	quarter_df,
	x="Reporting Period",
	y="Emissions (tons)",
	markers=True,
)
st.plotly_chart(fig_trend, use_container_width=True)

st.subheader("Facility Comparison")
facility_df = (
	filtered.groupby("Facility Name")["Emissions (tons)"]
	.sum()
	.reset_index()
	.sort_values(by="Emissions (tons)", ascending=False)
)
fig_facility = px.bar(
	facility_df,
	x="Facility Name",
	y="Emissions (tons)",
)
st.plotly_chart(fig_facility, use_container_width=True)

st.subheader("Scope Analysis")
scope_df = scope_totals.reset_index()
fig_scope = px.bar(
	scope_df,
	x="Scope",
	y="Emissions (tons)",
)
st.plotly_chart(fig_scope, use_container_width=True)

st.subheader("Scope-wise Emissions by Facility")
scope_facility_df = (
	filtered.groupby(["Facility Name", "Scope"])["Emissions (tons)"]
	.sum()
	.reset_index()
)
fig_scope_fac = px.bar(
	scope_facility_df,
	x="Facility Name",
	y="Emissions (tons)",
	color="Scope",
)
st.plotly_chart(fig_scope_fac, use_container_width=True)

st.subheader("GHG Contribution")
ghg_df = (
	filtered.groupby("GHG Type")["Emissions (tons)"]
	.sum()
	.reset_index()
)
fig_ghg = px.pie(
	ghg_df,
	names="GHG Type",
	values="Emissions (tons)",
	hole=0.3,
)
st.plotly_chart(fig_ghg, use_container_width=True)
