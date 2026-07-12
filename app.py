import os
import random
from datetime import datetime

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="AI Smart Grid Monitoring System",
    page_icon="⚡",
    layout="wide"
)


# ---------------- FILES AND MODEL ----------------

history_file = "permanent_live_history.csv"

model = joblib.load("smart_grid_model.pkl")

def generate_pdf_report(history_data):
    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "AI-Based Smart Grid Fault Detection System",
        styles["Title"]
    )

    content.append(title)
    content.append(Spacer(1, 15))

    generated_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M:%S %p"
    )

    content.append(
        Paragraph(
            f"Report Generated: {generated_time}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    total_readings = len(history_data)

    normal_readings = (
        history_data["Predicted Condition"] == "Normal"
    ).sum()

    fault_readings = total_readings - normal_readings

    summary_table_data = [
        ["Report Summary", "Value"],
        ["Total Readings", str(total_readings)],
        ["Normal Readings", str(normal_readings)],
        ["Fault Readings", str(fault_readings)]
    ]

    summary_table = Table(
        summary_table_data,
        colWidths=[220, 180]
    )

    summary_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
            ("TOPPADDING", (0, 0), (-1, 0), 10)
        ])
    )

    content.append(summary_table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Prediction History",
            styles["Heading2"]
        )
    )

    content.append(Spacer(1, 10))

    table_columns = [
        "Date",
        "Time",
        "Voltage (V)",
        "Current (A)",
        "Frequency (Hz)",
        "Power Factor",
        "Active Power (W)",
        "Predicted Condition",
        "Confidence (%)"
    ]

    pdf_table_data = [table_columns]

    for _, row in history_data.iterrows():

        pdf_table_data.append([
            str(row["Date"]),
            str(row["Time"]),
            str(row["Voltage (V)"]),
            str(row["Current (A)"]),
            str(row["Frequency (Hz)"]),
            str(row["Power Factor"]),
            str(row["Active Power (W)"]),
            str(row["Predicted Condition"]),
            str(row["Confidence (%)"])
        ])

    history_table = Table(
        pdf_table_data,
        repeatRows=1,
        colWidths=[
            52, 58, 48, 48, 52,
            48, 58, 68, 52
        ]
    )

    history_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.whitesmoke,
                colors.lightgrey
            ])
        ])
    )

    content.append(history_table)
    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Project Developed By: Mohammad Isha",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            "Madan Mohan Malaviya University of Technology, Gorakhpur",
            styles["Normal"]
        )
    )

    document.build(content)

    pdf_buffer.seek(0)

    return pdf_buffer


# ---------------- LOAD HISTORY ----------------

if "live_history" not in st.session_state:

    if os.path.exists(history_file):

        try:
            saved_history = pd.read_csv(history_file)

            st.session_state.live_history = (
                saved_history.to_dict("records")
            )

        except Exception:
            st.session_state.live_history = []

    else:
        st.session_state.live_history = []


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚡ Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Dashboard",
        "📡 Live Monitoring",
        "📁 Upload Dataset",
        "📜 Prediction History",
        "📊 Analytics",
        "ℹ About Project"
    ]
)


# ==================================================
# DASHBOARD PAGE
# ==================================================

if page == "🏠 Dashboard":

    st.title("⚡ AI Smart Grid Monitoring System")

    st.subheader("Enter Electrical Parameters")

    voltage = st.number_input(
        "Voltage (V)",
        min_value=0.0,
        value=230.0
    )

    current = st.number_input(
        "Current (A)",
        min_value=0.0,
        value=12.0
    )

    frequency = st.number_input(
        "Frequency (Hz)",
        min_value=0.0,
        value=50.0
    )

    power_factor = st.number_input(
        "Power Factor",
        min_value=0.0,
        max_value=1.0,
        value=0.95
    )

    power = voltage * current * power_factor

    st.subheader("Live Electrical Gauge")
    gauge_col1, gauge_col2, gauge_col3, gauge_col4 = st.columns(
        [1, 1, 1, 1.15]
    )

    voltage_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=voltage,
            title={
                "text": "Voltage (V)"
            },
            gauge={
                "axis": {
                    "range": [0, 300]
                },
                "steps": [
                    {
                        "range": [0, 180],
                        "color": "#8B1E1E"
                    },
                    {
                        "range": [180, 250],
                        "color": "#176B3A"
                    },
                    {
                        "range": [250, 300],
                        "color": "#8B1E1E"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 4
                    },
                    "thickness": 0.75,
                    "value": voltage
                }
            }
        )
    )

    voltage_gauge.update_layout(
        height=300,
        margin={
            "l": 30,
            "r": 30,
            "t": 60,
            "b": 20
        }
    )

    current_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current,
            title={
                "text": "Current (A)"
            },
            gauge={
                "axis": {
                    "range": [0, 100]
                },
                "steps": [
                    {
                        "range": [0, 30],
                        "color": "#176B3A"
                    },
                    {
                        "range": [30, 60],
                        "color": "#FFD43B"
                    },
                    {
                        "range": [60, 100],
                        "color": "#8B1E1E"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 4
                    },
                    "thickness": 0.75,
                    "value": current
                }
            }
        )
    )

    current_gauge.update_layout(
        height=300,
        margin={
            "l": 30,
            "r": 30,
            "t": 60,
            "b": 20
        }
    )

    frequency_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=frequency,
            title={
                "text": "Frequency (Hz)"
            },
            gauge={
                "axis": {
                    "range": [45, 55]
                },
                "steps": [
                    {
                        "range": [45, 49],
                        "color": "#8B1E1E"
                    },
                    {
                        "range": [49, 51],
                        "color": "#176B3A"
                    },
                    {
                        "range": [51, 55],
                        "color": "#8B1E1E"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 4
                    },
                    "thickness": 0.75,
                    "value": frequency
                }
            }
        )
    )

    frequency_gauge.update_layout(
        height=300,
        margin={
            "l": 30,
            "r": 30,
            "t": 60,
            "b": 20
        }
    )

    power_gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=power,
            title={
                "text": "Active Power (W)"
            },
            gauge={
                "axis": {
                    "range": [0, 10000]
                },
                "steps": [
                    {
                        "range": [0, 4000],
                        "color": "#176B3A"
                    },
                    {
                        "range": [4000, 7000],
                        "color": "#9A6A00"
                    },
                    {
                        "range": [7000, 10000],
                        "color": "#8B1E1E"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "white",
                        "width": 4
                    },
                    "thickness": 0.75,
                    "value": power
                }
            }
        )
    )

    power_gauge.update_layout(
        height=300,
        margin={
            "l": 20,
            "r": 40,
            "t": 60,
            "b": 20
        }
    )

    with gauge_col1:
        st.plotly_chart(
            voltage_gauge,
            use_container_width=True
        )

    with gauge_col2:
        st.plotly_chart(
            current_gauge,
            use_container_width=True
        )

    with gauge_col3:
        st.plotly_chart(
            frequency_gauge,
            use_container_width=True
        )

    with gauge_col4:
        st.plotly_chart(
            power_gauge,
            use_container_width=True
        )    

    if st.button(
        "Predict Fault",
        key="manual_predict"
    ):

        new_data = pd.DataFrame({
            "Voltage": [voltage],
            "Current": [current],
            "Frequency": [frequency],
            "PowerFactor": [power_factor],
            "Power": [power]
        })

        prediction = model.predict(new_data)
        probability = model.predict_proba(new_data)
        classes = model.classes_

        predicted_fault = prediction[0]
        confidence = max(probability[0]) * 100

        st.success("Prediction Completed")

        st.subheader("System Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Active Power",
                f"{round(power, 2)} W"
            )

        with result_col2:
            st.metric(
                "AI Prediction",
                predicted_fault
            )

        with result_col3:
            st.metric(
                "Confidence",
                f"{round(confidence, 2)} %"
            )

        if predicted_fault == "Normal":

            st.success("🟢 Grid Status: NORMAL")

        elif predicted_fault == "Overload":

            st.error("🚨 OVERLOAD DETECTED")
            st.warning("Reduce electrical load immediately.")

        elif predicted_fault == "Voltage Sag":

            st.error("⚠️ VOLTAGE SAG DETECTED")
            st.warning(
                "Voltage is below the safe operating limit."
            )

        elif predicted_fault == "Voltage Swell":

            st.error("⚠️ VOLTAGE SWELL DETECTED")
            st.warning(
                "Voltage is above the safe operating limit."
            )

        elif predicted_fault == "Frequency Fault":

            st.error("⚠️ FREQUENCY FAULT DETECTED")
            st.warning(
                "Frequency is outside the permissible range."
            )

        elif predicted_fault == "Short Circuit":

            st.error("🔥 SHORT CIRCUIT DETECTED")
            st.warning(
                "Disconnect the faulty line immediately."
            )

        else:
            st.info(predicted_fault)

        st.subheader("Prediction Confidence")

        confidence_data = pd.DataFrame({
            "Fault Type": classes,
            "Confidence (%)": probability[0] * 100
        })

        confidence_data = confidence_data.sort_values(
            by="Confidence (%)",
            ascending=False
        )

        st.bar_chart(
            confidence_data.set_index("Fault Type")
        )


# ==================================================
# LIVE MONITORING PAGE
# ==================================================

elif page == "📡 Live Monitoring":

    st.title("📡 Real-Time Sensor Simulation")

    st.write(
        "Generate simulated smart-grid readings and detect faults using AI."
    )

    if st.button(
        "Generate Live Sensor Reading",
        key="live_generate"
    ):

        condition = random.choice([
            "Normal",
            "Normal",
            "Normal",
            "Overload",
            "Voltage Sag",
            "Voltage Swell",
            "Frequency Fault",
            "Short Circuit"
        ])

        if condition == "Normal":

            live_voltage = round(
                random.uniform(215, 245),
                2
            )

            live_current = round(
                random.uniform(8, 20),
                2
            )

            live_frequency = round(
                random.uniform(49.7, 50.3),
                2
            )

            live_power_factor = round(
                random.uniform(0.85, 0.99),
                2
            )

        elif condition == "Overload":

            live_voltage = round(
                random.uniform(210, 235),
                2
            )

            live_current = round(
                random.uniform(35, 60),
                2
            )

            live_frequency = round(
                random.uniform(49.5, 50.5),
                2
            )

            live_power_factor = round(
                random.uniform(0.70, 0.88),
                2
            )

        elif condition == "Voltage Sag":

            live_voltage = round(
                random.uniform(150, 179),
                2
            )

            live_current = round(
                random.uniform(10, 30),
                2
            )

            live_frequency = round(
                random.uniform(49.5, 50.5),
                2
            )

            live_power_factor = round(
                random.uniform(0.75, 0.95),
                2
            )

        elif condition == "Voltage Swell":

            live_voltage = round(
                random.uniform(251, 285),
                2
            )

            live_current = round(
                random.uniform(8, 22),
                2
            )

            live_frequency = round(
                random.uniform(49.5, 50.5),
                2
            )

            live_power_factor = round(
                random.uniform(0.80, 0.98),
                2
            )

        elif condition == "Frequency Fault":

            live_voltage = round(
                random.uniform(215, 245),
                2
            )

            live_current = round(
                random.uniform(8, 20),
                2
            )

            live_frequency = round(
                random.choice([
                    random.uniform(47.0, 48.8),
                    random.uniform(51.2, 53.0)
                ]),
                2
            )

            live_power_factor = round(
                random.uniform(0.75, 0.95),
                2
            )

        else:

            live_voltage = round(
                random.uniform(50, 99),
                2
            )

            live_current = round(
                random.uniform(60, 120),
                2
            )

            live_frequency = round(
                random.uniform(48.5, 51.5),
                2
            )

            live_power_factor = round(
                random.uniform(0.30, 0.70),
                2
            )

        live_power = (
            live_voltage
            * live_current
            * live_power_factor
        )

        live_data = pd.DataFrame({
            "Voltage": [live_voltage],
            "Current": [live_current],
            "Frequency": [live_frequency],
            "PowerFactor": [live_power_factor],
            "Power": [live_power]
        })

        live_prediction = model.predict(
            live_data
        )[0]

        live_probability = model.predict_proba(
            live_data
        )

        live_confidence = (
            max(live_probability[0]) * 100
        )

        new_history_record = {
            "Date": datetime.now().strftime("%d-%m-%Y"),
            "Time": datetime.now().strftime("%I:%M:%S %p"),
            "Voltage (V)": live_voltage,
            "Current (A)": live_current,
            "Frequency (Hz)": live_frequency,
            "Power Factor": live_power_factor,
            "Active Power (W)": round(live_power, 2),
            "Predicted Condition": live_prediction,
            "Confidence (%)": round(live_confidence, 2)
        }

        st.session_state.live_history.append(
            new_history_record
        )

        new_record_dataframe = pd.DataFrame([
            new_history_record
        ])

        if os.path.exists(history_file):

            new_record_dataframe.to_csv(
                history_file,
                mode="a",
                header=False,
                index=False
            )

        else:

            new_record_dataframe.to_csv(
                history_file,
                index=False
            )

        reading_col1, reading_col2, reading_col3, reading_col4 = (
            st.columns(4)
        )

        with reading_col1:
            st.metric(
                "Voltage",
                f"{live_voltage} V"
            )

        with reading_col2:
            st.metric(
                "Current",
                f"{live_current} A"
            )

        with reading_col3:
            st.metric(
                "Frequency",
                f"{live_frequency} Hz"
            )

        with reading_col4:
            st.metric(
                "Power Factor",
                live_power_factor
            )

        st.subheader("Live AI Result")

        live_col1, live_col2, live_col3 = st.columns(3)

        with live_col1:
            st.metric(
                "Active Power",
                f"{round(live_power, 2)} W"
            )

        with live_col2:
            st.metric(
                "Detected Condition",
                live_prediction
            )

        with live_col3:
            st.metric(
                "AI Confidence",
                f"{round(live_confidence, 2)} %"
            )

        if live_prediction == "Normal":

            st.success("🟢 Live Grid Status: NORMAL")

        elif live_prediction == "Overload":

            st.error("🚨 LIVE OVERLOAD DETECTED")
            st.warning(
                "Reduce electrical load immediately."
            )

        elif live_prediction == "Voltage Sag":

            st.error("⚠️ LIVE VOLTAGE SAG DETECTED")
            st.warning(
                "Voltage is below the safe operating limit."
            )

        elif live_prediction == "Voltage Swell":

            st.error("⚠️ LIVE VOLTAGE SWELL DETECTED")
            st.warning(
                "Voltage is above the safe operating limit."
            )

        elif live_prediction == "Frequency Fault":

            st.error("⚠️ LIVE FREQUENCY FAULT DETECTED")
            st.warning(
                "Frequency is outside the permissible range."
            )

        elif live_prediction == "Short Circuit":

            st.error("🔥 LIVE SHORT CIRCUIT DETECTED")
            st.warning(
                "Disconnect the faulty line immediately."
            )

        else:
            st.info(live_prediction)


# ==================================================
# HISTORY PAGE
# ==================================================

elif page == "📜 Prediction History":

    st.title("📜 Live Prediction History")

    if len(st.session_state.live_history) > 0:

        history_data = pd.DataFrame(
            st.session_state.live_history
        )

        total_readings = len(history_data)

        normal_readings = (
            history_data["Predicted Condition"] == "Normal"
        ).sum()

        fault_readings = (
            total_readings - normal_readings
        )

        history_col1, history_col2, history_col3 = (
            st.columns(3)
        )

        with history_col1:
            st.metric(
                "Total Readings",
                total_readings
            )

        with history_col2:
            st.metric(
                "Normal Readings",
                int(normal_readings)
            )

        with history_col3:
            st.metric(
                "Fault Readings",
                int(fault_readings)
            )

        st.dataframe(
            history_data,
            use_container_width=True
        )

        csv_data = history_data.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="Download Live History CSV",
            data=csv_data,
            file_name="live_prediction_history.csv",
            mime="text/csv"
        )

        pdf_report = generate_pdf_report(
            history_data
        )

        st.download_button(
            label="📄 Download PDF Report",
            data=pdf_report,
            file_name="smart_grid_fault_report.pdf",
            mime="application/pdf"
        )

        if st.button(
            "Clear Complete History",
            key="clear_history"
        ):

            st.session_state.live_history = []

            if os.path.exists(history_file):
                os.remove(history_file)

            st.rerun()

    else:
        st.info("No live readings generated yet.")
# ==================================================
# UPLOAD DATASET PAGE
# ==================================================


elif page == "📁 Upload Dataset":

    st.title("📁 Upload Electrical Dataset")

    st.write(
        "Upload a CSV file containing electrical parameters."
    )

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        try:

            uploaded_data = pd.read_csv(uploaded_file)

            st.success("Dataset Uploaded Successfully")

            st.subheader("Dataset Preview")

            st.dataframe(
                uploaded_data,
                use_container_width=True
            )

            required_columns = [
                "Voltage",
                "Current",
                "Frequency",
                "PowerFactor",
                "Fault"
            ]

            missing_columns = [
                column
                for column in required_columns
                if column not in uploaded_data.columns
            ]

            if len(missing_columns) == 0:

                st.success(
                    "✅ Dataset Format Valid"
                )

                if "Power" not in uploaded_data.columns:

                    uploaded_data["Power"] = (
                        uploaded_data["Voltage"]
                        * uploaded_data["Current"]
                        * uploaded_data["PowerFactor"]
                    )

                    st.info(
                        "Power column was missing, so it was calculated automatically."
                    )

                st.write("### Available Columns")

                st.write(
                    list(uploaded_data.columns)
                )

            if st.button("🚀 Train Model from Uploaded Dataset"):

                from sklearn.model_selection import train_test_split
                from sklearn.ensemble import RandomForestClassifier
                from sklearn.metrics import accuracy_score
                import joblib

                X = uploaded_data[
                    [
                        "Voltage",
                        "Current",
                        "Frequency",
                        "PowerFactor",
                        "Power"
                    ]
                ]

                y = uploaded_data["Fault"]

                X_train, X_test, y_train, y_test = train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42
                )

                uploaded_model = RandomForestClassifier(
                    n_estimators=100,
                    random_state=42
                )

                uploaded_model.fit(
                    X_train,
                    y_train
                )

                predictions = uploaded_model.predict(
                    X_test
                )

                accuracy = accuracy_score(
                    y_test,
                    predictions
                )

                joblib.dump(
                    uploaded_model,
                    "smart_grid_model.pkl"
                )

                st.success(
                    "✅ Model Trained Successfully"
                )

                st.metric(
                    "Accuracy",
                    f"{accuracy*100:.2f}%"
                )

                st.info(
                    "The uploaded dataset model is now the active model."
                )

            else:

                st.error(
                    "❌ Invalid Dataset Format"
                )

                st.write(
                    "Missing Columns:"
                )

                for column in missing_columns:
                    st.write(f"- {column}")

                st.write(
                    "Required Columns:"
                )

                st.code(
                    "Voltage, Current, Frequency, PowerFactor, Fault"
                )

        except Exception as error:

            st.error(
                f"Could not read the CSV file: {error}"
            )


# ==================================================
# ANALYTICS PAGE
# ==================================================

elif page == "📊 Analytics":

    st.title("📊 Smart Grid Analytics")

    if len(st.session_state.live_history) > 0:

        history_data = pd.DataFrame(
            st.session_state.live_history
        )

        st.subheader("Fault Distribution")

        fault_distribution = (
            history_data["Predicted Condition"]
            .value_counts()
            .reset_index()
        )

        fault_distribution.columns = [
            "Fault Type",
            "Count"
        ]

        st.bar_chart(
            fault_distribution.set_index("Fault Type")
        )

        st.subheader("Voltage Trend")

        st.line_chart(
            history_data[["Voltage (V)"]]
        )

        st.subheader("Current Trend")

        st.line_chart(
            history_data[["Current (A)"]]
        )

        st.subheader("Frequency Trend")

        st.line_chart(
            history_data[["Frequency (Hz)"]]
        )

        st.subheader("Power Trend")

        st.line_chart(
            history_data[["Active Power (W)"]]
        )

    else:
        st.info(
            "Generate live sensor readings to view analytics."
        )


# ==================================================
# ABOUT PAGE
# ==================================================

elif page == "ℹ About Project":

    st.title("ℹ About Project")

    st.subheader(
        "AI-Based Smart Grid Fault Detection System"
    )

    st.write(
        """
        This project uses Python and Machine Learning to
        monitor electrical parameters and classify smart-grid
        operating conditions.
        """
    )

    st.subheader("Faults Detected")

    st.write(
        """
        - Normal Operating Condition
        - Overload
        - Voltage Sag
        - Voltage Swell
        - Frequency Fault
        - Short Circuit
        """
    )

    st.subheader("Technologies Used")

    st.write(
        """
        - Python
        - Streamlit
        - Pandas
        - Scikit-learn
        - Random Forest Classifier
        - Joblib
        - CSV Data Storage
        """
    )

    st.subheader("Project Features")

    st.write(
        """
        - Manual fault prediction
        - Real-time sensor simulation
        - Machine-learning fault classification
        - Prediction confidence
        - Smart fault alerts
        - Permanent prediction history
        - CSV report download
        - Fault distribution analytics
        - Voltage, current and frequency trends
        """
    )
