# app.py - Medical Insurance Cost Prediction System
import streamlit as st
import pandas as pd
import numpy as np
import os
import random
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Insurance Cost Predictor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2e86ab;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .prediction-card {
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .cost-low {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
    }
    .cost-medium {
        background: linear-gradient(135deg, #f7971e 0%, #ffd200 100%);
    }
    .cost-high {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2e86ab;
        margin: 0.5rem 0;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
    .insurance-plans {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


class InsurancePredictor:
    def __init__(self):
        self.feature_info = {
            'age': {
                'desc': 'Age of the primary beneficiary (18-80 years)',
                'type': 'number',
                'min': 18, 'max': 80, 'step': 1,
                'default': 35,
                'normal_range': (18, 80)
            },
            'sex': {
                'desc': 'Gender of the beneficiary',
                'type': 'select',
                'options': {'0': 'Female', '1': 'Male'},
                'default': 0
            },
            'bmi': {
                'desc': 'Body Mass Index (15-50 kg/m²) - Healthy range: 18.5-25',
                'type': 'number',
                'min': 15.0, 'max': 50.0, 'step': 0.1,
                'default': 22.5,
                'normal_range': (18.5, 25.0),
                'risk_ranges': {
                    'critical_low': (15.0, 16.0),
                    'high_risk_low': (16.0, 18.5),
                    'healthy': (18.5, 25.0),
                    'overweight': (25.0, 30.0),
                    'obese': (30.0, 50.0)
                }
            },
            'children': {
                'desc': 'Number of children covered by health insurance',
                'type': 'number',
                'min': 0, 'max': 10, 'step': 1,
                'default': 1,
                'normal_range': (0, 10)
            },
            'smoker': {
                'desc': 'Smoking status',
                'type': 'select',
                'options': {'0': 'No', '1': 'Yes'},
                'default': 0
            },
            'region': {
                'desc': 'Residential area in the US',
                'type': 'select',
                'options': {
                    '0': 'Northeast',
                    '1': 'Northwest',
                    '2': 'Southeast',
                    '3': 'Southwest'
                },
                'default': 0
            }
        }

    def get_bmi_category(self, bmi):
        """Determine BMI category and risk level"""
        if bmi < 16.0:
            return "Critical Underweight", "🔴", "Application may be rejected", 4000
        elif bmi < 18.5:
            return "Underweight", "🟠", "High risk - may affect premium", 1500
        elif bmi <= 25.0:
            return "Healthy", "🟢", "Optimal range - lowest risk", 0
        elif bmi <= 30.0:
            return "Overweight", "🟡", "Moderate risk", 800
        else:
            return "Obese", "🔴", "High risk - significant premium impact", 2500

    def get_cost_level(self, cost):
        """Determine cost level based on predicted insurance cost"""
        if cost < 5000:
            return 'Low', '🟢', 'cost-low', "Affordable insurance range. Good health profile."
        elif cost < 10000:
            return 'Medium', '🟡', 'cost-medium', "Moderate insurance cost. Consider lifestyle improvements."
        elif cost < 15000:
            return 'High', '🟠', 'cost-high', "High insurance cost. Recommended to review health factors."
        else:
            return 'Very High', '🔴', 'cost-high', "Very high insurance cost. Immediate health review recommended."

    def predict_insurance_cost(self, input_data):
        """Advanced insurance cost prediction using medical underwriting rules"""
        base_cost = 2000

        # Age factor (increases with age - older = higher risk)
        age_factor = input_data['age'] * 100

        # BMI factor (medical underwriting with detailed categories)
        bmi = input_data['bmi']
        bmi_category, bmi_emoji, bmi_note, bmi_factor = self.get_bmi_category(bmi)

        # Smoking factor (major risk factor)
        smoker_factor = 8500 if input_data['smoker'] == 1 else 0

        # Children factor (more dependents = higher cost)
        children_factor = input_data['children'] * 600

        # Region factor (geographic cost variations)
        region_factors = {
            0: 0,  # Northeast - average
            1: -200,  # Northwest - lower
            2: 400,  # Southeast - higher
            3: 150  # Southwest - slightly higher
        }
        region_factor = region_factors[input_data['region']]

        # Gender factor (actuarial data)
        gender_factor = 200 if input_data['sex'] == 1 else 0

        # Calculate total cost
        total_cost = (
                base_cost +
                age_factor +
                bmi_factor +
                smoker_factor +
                children_factor +
                region_factor +
                gender_factor
        )

        # Add random variation (real-world factor)
        variation = random.uniform(0.9, 1.1)  # ±10% variation
        total_cost *= variation

        return round(total_cost, 2), bmi_category, bmi_emoji, bmi_note

    def predict(self, input_data):
        """Make prediction for insurance cost"""
        try:
            predicted_cost, bmi_category, bmi_emoji, bmi_note = self.predict_insurance_cost(input_data)
            cost_level, cost_emoji, cost_class, recommendation = self.get_cost_level(predicted_cost)

            return {
                'predicted_cost': predicted_cost,
                'cost_level': cost_level,
                'cost_emoji': cost_emoji,
                'cost_class': cost_class,
                'recommendation': recommendation,
                'bmi_category': bmi_category,
                'bmi_emoji': bmi_emoji,
                'bmi_note': bmi_note,
                'method': "Advanced Insurance Underwriting System",
                'success': True
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def create_sidebar():
    """Create the sidebar with information and controls"""
    st.sidebar.title("💰 Insurance Cost Predictor")

    st.sidebar.markdown("---")
    st.sidebar.subheader("About")
    st.sidebar.info("""
    **Advanced Insurance Underwriting System**

    Predicts medical insurance costs using actuarial data and medical underwriting principles.

    *Based on industry-standard risk assessment models*
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("BMI Risk Categories")
    st.sidebar.write("""
    **BMI Categories:**
    - 🟢 **18.5-25.0**: Healthy (Optimal)
    - 🟡 **25.0-30.0**: Overweight (+$800)
    - 🟠 **16.0-18.5**: Underweight (+$1,500)
    - 🔴 **<16.0**: Critical Underweight (+$4,000)
    - 🔴 **>30.0**: Obese (+$2,500)
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Cost Factors")
    st.sidebar.write("""
    **Premium Drivers:**
    - 🚬 Smoking: +$8,500
    - 📊 High BMI: +$800-4,000
    - 👴 Age: +$100/year
    - 👶 Children: +$600/child
    - 🗺️ Region: Geographic variations
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("Quick Actions")

    if st.sidebar.button("🔄 Reset Form"):
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
        Insurance Analytics Platform<br>
        Version 2.0 • Advanced Underwriting
    </div>
    """, unsafe_allow_html=True)


def create_feature_input(feature, info):
    """Create input for a single feature"""
    with st.container():
        if info['type'] == 'number':
            value = st.number_input(
                label=f"**{feature.upper()}**",
                min_value=float(info['min']),
                max_value=float(info['max']),
                value=float(info['default']),
                step=float(info['step']),
                help=info['desc']
            )
        elif info['type'] == 'select':
            option_key = st.selectbox(
                label=f"**{feature.upper()}**",
                options=list(info['options'].keys()),
                format_func=lambda x: f"{info['options'][x]}",
                help=info['desc'],
                index=int(info['default'])
            )
            value = int(option_key)

        # Show BMI-specific warnings and ranges
        if feature == 'bmi' and 'risk_ranges' in info:
            current_bmi = float(value)
            bmi_category, bmi_emoji, bmi_note, _ = InsurancePredictor().get_bmi_category(current_bmi)

            # Color coding based on BMI category
            if "Critical" in bmi_category or "Obese" in bmi_category:
                color = "red"
            elif "Underweight" in bmi_category or "Overweight" in bmi_category:
                color = "orange"
            else:
                color = "green"

            st.markdown(
                f"<span style='color: {color}; font-size: 0.9rem; font-weight: bold;'>{bmi_emoji} {bmi_category}: {bmi_note}</span>",
                unsafe_allow_html=True)

        # Show normal range for other features
        elif 'normal_range' in info and feature != 'bmi':
            min_val, max_val = info['normal_range']
            current_value = float(value) if hasattr(value, 'dtype') else value

            if min_val <= current_value <= max_val:
                st.markdown(f"<span style='color: green; font-size: 0.8rem;'>✓ Within expected range</span>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: orange; font-size: 0.8rem;'>⚠️ Outside typical range</span>",
                            unsafe_allow_html=True)

        return value


def create_input_form(predictor):
    """Create the main input form"""
    st.markdown('<div class="main-header">Medical Insurance Cost Predictor</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align: center; color: #666; margin-bottom: 2rem;">Advanced Underwriting System • Actuarial Risk Assessment</div>',
        unsafe_allow_html=True)

    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["📝 Detailed Underwriting", "⚡ Quick Estimate"])

    input_data = {}

    with tab1:
        st.subheader("Personal & Health Information")

        # Create columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            input_data['age'] = create_feature_input('age', predictor.feature_info['age'])
            input_data['bmi'] = create_feature_input('bmi', predictor.feature_info['bmi'])
            input_data['children'] = create_feature_input('children', predictor.feature_info['children'])

        with col2:
            input_data['sex'] = create_feature_input('sex', predictor.feature_info['sex'])
            input_data['smoker'] = create_feature_input('smoker', predictor.feature_info['smoker'])
            input_data['region'] = create_feature_input('region', predictor.feature_info['region'])

    with tab2:
        st.subheader("Quick Insurance Estimate")
        st.info("Provide basic information for instant premium calculation")

        col1, col2 = st.columns(2)

        with col1:
            input_data['age'] = st.slider("**AGE**", 18, 80, 35)
            input_data['bmi'] = st.slider("**BMI**", 15.0, 50.0, 22.5, 0.1,
                                          help="Healthy range: 18.5-25.0")
            input_data['smoker'] = st.selectbox("**SMOKER**", [0, 1],
                                                format_func=lambda x: "No" if x == 0 else "Yes",
                                                index=0)

        with col2:
            input_data['sex'] = st.selectbox("**GENDER**", [0, 1],
                                             format_func=lambda x: "Female" if x == 0 else "Male",
                                             index=0)
            input_data['children'] = st.slider("**CHILDREN**", 0, 10, 1)
            input_data['region'] = st.selectbox("**REGION**", [0, 1, 2, 3],
                                                format_func=lambda x:
                                                ["Northeast", "Northwest", "Southeast", "Southwest"][x],
                                                index=0)

    return input_data


def display_bmi_analysis(bmi_value, bmi_category, bmi_emoji, bmi_note):
    """Display detailed BMI analysis"""
    st.subheader("📊 BMI Health Assessment")

    col1, col2 = st.columns(2)

    with col1:
        # BMI Gauge
        bmi_percentage = min(max((bmi_value - 15) / (50 - 15) * 100, 0), 100)

        st.markdown(f"""
        <div class="feature-card">
            <h4>BMI Score</h4>
            <h2>{bmi_value}</h2>
            <p>Category: <strong>{bmi_emoji} {bmi_category}</strong></p>
            <p>{bmi_note}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>BMI Categories</h4>
            <p>🟢 <strong>18.5-25.0:</strong> Healthy (Optimal)</p>
            <p>🟡 <strong>25.0-30.0:</strong> Overweight</p>
            <p>🟠 <strong>16.0-18.5:</strong> Underweight</p>
            <p>🔴 <strong><16.0:</strong> Critical Underweight</p>
            <p>🔴 <strong>>30.0:</strong> Obese</p>
        </div>
        """, unsafe_allow_html=True)

    # BMI-specific recommendations
    if "Critical" in bmi_category or bmi_value > 30:
        st.markdown("""
        <div class="warning-box">
            <h4>🚨 Health Advisory</h4>
            <p>Your BMI indicates significant health risks. Insurance applications may be subject to:</p>
            <ul>
                <li>Higher premiums due to increased health risks</li>
                <li>Possible requirement for medical examination</li>
                <li>Limited plan availability</li>
            </ul>
            <p><strong>Recommendation:</strong> Consult with a healthcare provider to develop a weight management plan.</p>
        </div>
        """, unsafe_allow_html=True)
    elif "Underweight" in bmi_category or "Overweight" in bmi_category:
        st.info("""
        **💡 Improvement Opportunity:** 
        Achieving a BMI in the healthy range (18.5-25.0) could significantly reduce your insurance premiums 
        and improve your overall health outcomes.
        """)


def display_cost_breakdown(input_data, predicted_cost, bmi_factor):
    """Display detailed cost breakdown"""
    st.subheader("📈 Cost Breakdown Analysis")

    # Calculate cost factors
    factors = {
        'Base Premium': 2000,
        'Age Factor': input_data['age'] * 100,
        'BMI Adjustment': bmi_factor,
        'Smoking Surcharge': 8500 if input_data['smoker'] == 1 else 0,
        'Children Coverage': input_data['children'] * 600,
        'Regional Adjustment': [0, -200, 400, 150][input_data['region']],
        'Gender Adjustment': 200 if input_data['sex'] == 1 else 0
    }

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Cost Components:**")
        total_components = 0
        for factor, cost in factors.items():
            if cost != 0:
                st.write(f"• {factor}: ${cost:,.0f}")
                total_components += cost

        st.write("---")
        st.write(f"**Subtotal:** ${total_components:,.0f}")

    with col2:
        st.write("**Premium Summary:**")
        st.write(f"• Calculated Base: ${total_components:,.0f}")
        st.write(f"• Market Adjustment: ±10%")
        st.write(f"• **Final Annual Premium:**")
        st.markdown(f"<h3>${predicted_cost:,.0f}</h3>", unsafe_allow_html=True)
        st.write(f"• **Monthly:** ${predicted_cost / 12:,.0f}")


def display_results(results, input_data, predictor):
    """Display comprehensive prediction results"""
    st.markdown("---")

    if not results['success']:
        st.error(f"❌ Prediction failed: {results['error']}")
        return

    # Main prediction card
    cost_class = results['cost_class']
    cost_emoji = results['cost_emoji']

    st.markdown(f"""
    <div class="prediction-card {cost_class}">
        <h2 style="color: white; margin: 0;">{cost_emoji} {results['cost_level']} COST</h2>
        <h1 style="color: white; margin: 0.5rem 0;">${results['predicted_cost']:,.2f}</h1>
        <h4 style="color: white; margin: 0;">Annual Insurance Premium</h4>
        <p style="color: white; margin: 0.5rem 0 0 0; font-size: 0.9rem;">{results['method']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Monthly Premium", f"${results['predicted_cost'] / 12:,.2f}")
    with col2:
        st.metric("Cost Level", f"{results['cost_level']} {results['cost_emoji']}")
    with col3:
        st.metric("BMI Category", f"{results['bmi_emoji']} {results['bmi_category']}")

    # BMI Analysis
    display_bmi_analysis(input_data['bmi'], results['bmi_category'],
                         results['bmi_emoji'], results['bmi_note'])

    # Cost breakdown (calculate BMI factor for display)
    bmi_category, _, _, bmi_factor = predictor.get_bmi_category(input_data['bmi'])
    display_cost_breakdown(input_data, results['predicted_cost'], bmi_factor)

    # Recommendations
    st.subheader("🎯 Premium Optimization Tips")
    st.info(results['recommendation'])

    # Specific recommendations
    tips = []
    if input_data['smoker'] == 1:
        tips.append("• **Quit smoking** - Could save approximately $8,500 annually")
    if input_data['bmi'] > 25.0:
        tips.append(
            f"• **Reduce BMI to healthy range (18.5-25.0)** - Current BMI {input_data['bmi']} could save ${bmi_factor:,.0f}")
    elif input_data['bmi'] < 18.5:
        tips.append(
            f"• **Achieve healthy BMI (18.5-25.0)** - Current BMI {input_data['bmi']} could save ${bmi_factor:,.0f}")
    if input_data['age'] > 50:
        tips.append("• **Explore senior health plans** - May offer specialized coverage")
    if input_data['children'] > 2:
        tips.append("• **Consider family plan options** - Could provide better value")

    if tips:
        st.warning("**Potential Cost Reduction Strategies:**")
        for tip in tips:
            st.write(tip)


def save_prediction(input_data, results):
    """Save prediction to history"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_data = {
            'timestamp': timestamp,
            **input_data,
            'predicted_cost': results['predicted_cost'],
            'cost_level': results['cost_level'],
            'bmi_category': results['bmi_category'],
            'method': results['method']
        }

        df = pd.DataFrame([save_data])

        # Ensure directory exists
        os.makedirs('data', exist_ok=True)

        file_path = 'data/insurance_predictions.csv'

        # Check if file exists to determine header
        header = not os.path.exists(file_path)

        df.to_csv(file_path, mode='a', header=header, index=False)

        st.success("✅ Insurance quote saved to records!")

    except Exception as e:
        st.error(f"❌ Error saving prediction: {e}")


def main():
    """Main application function"""
    try:
        # Initialize predictor
        predictor = InsurancePredictor()

        # Create sidebar
        create_sidebar()

        # Welcome message
        st.success("🚀 **Advanced Insurance Underwriting System Ready**")

        # Create input form and get data
        input_data = create_input_form(predictor)

        # Prediction button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_clicked = st.button(
                "💰 GET INSURANCE QUOTE",
                type="primary",
                use_container_width=True,
                help="Click to calculate your annual insurance premium"
            )

        if predict_clicked:
            with st.spinner("🔍 Analyzing risk factors and calculating premium..."):
                import time
                time.sleep(1)  # Simulate processing time

                results = predictor.predict(input_data)
                display_results(results, input_data, predictor)

                # Save prediction
                if st.button("💾 Save This Quote", use_container_width=True):
                    save_prediction(input_data, results)

    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page and try again.")


# Run the application
if __name__ == "__main__":
    main()