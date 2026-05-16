import gradio as gr
import joblib
import pandas as pd
import numpy as np
import os

MODEL_PATH = "churn_rf_v1_optuna.pkl"
model = scaler = ohe = num_cols = cat_cols = None
model_loaded = False

try:
    if os.path.exists(MODEL_PATH):
        artifact = joblib.load(MODEL_PATH)
        model = artifact["model"]
        scaler = artifact["scaler"]
        ohe = artifact["ohe"]
        num_cols = artifact["num_cols"]
        cat_cols = artifact["cat_cols"]
        model_loaded = True
        print("✅ Simple model loaded!")
except Exception as e:
    print(f"❌ Error: {e}")

def bool_to_yes_no(val):
    if isinstance(val, (bool, np.bool_)): return "Yes" if val else "No"
    if isinstance(val, (int, float)): return "Yes" if val == 1 else "No"
    return str(val)

def predict_churn(gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService,
                  MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
                  DeviceProtection, TechSupport, StreamingTV, StreamingMovies,
                  Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges):
    if not model_loaded:
        return {"Status": "⚠️ Model not loaded"}
    
    input_data = {
        "gender": str(gender), "SeniorCitizen": int(SeniorCitizen),
        "Partner": bool_to_yes_no(Partner), "Dependents": bool_to_yes_no(Dependents),
        "tenure": int(tenure), "PhoneService": str(PhoneService),
        "MultipleLines": str(MultipleLines), "InternetService": str(InternetService),
        "OnlineSecurity": str(OnlineSecurity), "OnlineBackup": str(OnlineBackup),
        "DeviceProtection": str(DeviceProtection), "TechSupport": str(TechSupport),
        "StreamingTV": str(StreamingTV), "StreamingMovies": str(StreamingMovies),
        "Contract": str(Contract),
        "PaperlessBilling": bool_to_yes_no(PaperlessBilling),
        "PaymentMethod": str(PaymentMethod),
        "MonthlyCharges": float(MonthlyCharges), "TotalCharges": float(TotalCharges)
    }
    
    df = pd.DataFrame([input_data])
    num_part = scaler.transform(df[num_cols])
    cat_part = ohe.transform(df[cat_cols])
    X_p = np.hstack([num_part, cat_part])
    
    prob = float(model.predict_proba(X_p)[0][1])
    return {
        "Churn Probability": f"{prob:.1%}",
        "Risk Level": "🔴 High" if prob > 0.6 else "🟡 Medium" if prob > 0.3 else "🟢 Low",
        "Recommendation": "Proactive offer" if prob > 0.6 else "Monitor normally"
    }

demo = gr.Interface(
    fn=predict_churn,
    inputs=[
        gr.Dropdown(["Male","Female"],label="Gender"),
        gr.Radio([0,1],label="Senior Citizen",value=0),
        gr.Dropdown(["Yes","No"],label="Partner"),
        gr.Dropdown(["Yes","No"],label="Dependents"),
        gr.Number(label="Tenure",value=12),
        gr.Dropdown(["Yes","No"],label="Phone Service"),
        gr.Dropdown(["Yes","No","No phone service"],label="Multiple Lines"),
        gr.Dropdown(["DSL","Fiber optic","No"],label="Internet Service"),
        gr.Dropdown(["Yes","No","No internet service"],label="Online Security"),
        gr.Dropdown(["Yes","No","No internet service"],label="Online Backup"),
        gr.Dropdown(["Yes","No","No internet service"],label="Device Protection"),
        gr.Dropdown(["Yes","No","No internet service"],label="Tech Support"),
        gr.Dropdown(["Yes","No","No internet service"],label="Streaming TV"),
        gr.Dropdown(["Yes","No","No internet service"],label="Streaming Movies"),
        gr.Dropdown(["Month-to-month","One year","Two year"],label="Contract"),
        gr.Dropdown(["Yes","No"],label="Paperless Billing",value="Yes"),
        gr.Dropdown(["Electronic check","Mailed check","Bank transfer","Credit card"],label="Payment Method"),
        gr.Number(label="Monthly Charges",value=70.0),
        gr.Number(label="Total Charges",value=800.0)
    ],
    outputs="json",
    title="📡 Telco Churn (Simple)",
    description="100% compatible model - no version conflicts",
    examples=[["Female",0,"Yes","No",12,"Yes","No","Fiber optic","No","No","No","No","Yes","Yes","Month-to-month","Yes","Electronic check",70.0,800.0]],
    cache_examples=False
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, ssr_mode=False)
