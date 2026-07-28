df = export_history()

st.download_button(
    label="📥 Download CSV",
    data=df.to_csv(index=False),
    file_name="evaluation_history.csv",
    mime="text/csv"
)