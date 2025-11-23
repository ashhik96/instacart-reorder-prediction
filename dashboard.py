import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import gdown

# Page config
st.set_page_config(page_title="Instacart Reorder Intelligence", layout="wide", page_icon="🛒")

# Google Drive file IDs
GDRIVE_FILES = {
    'predictions_with_details.csv': '1ape34BYC3fMfnDqCOPE5i8SM687IpQcD',
    'department_reorder_rates.csv': '18pDHrwkLO2EhSeZJRex_YqmJJrsQn_CN',
    'product_reorder_rates.csv': '1kMfYPfgUg-7-iJv5JKShPLq38ZewM4L6',
    'user_segments.csv': '1oOLBLlqame7P6SudMn7BRs2dw3SCkL29',
    'segment_recommendations.csv': '1d1230vkstrXnf12hWnhTG2bTlDLsJ4NRB'
}

# Function to download files from Google Drive if needed
def ensure_data_files():
    """Download files from Google Drive if they don't exist locally"""
    os.makedirs('data/processed', exist_ok=True)
    
    # Use export URLs for Google Sheets files
    export_urls = {
        'predictions_with_details.csv': 'https://docs.google.com/spreadsheets/d/1ape34BYC3fMfnDqCOPE5i8SM687IpQcD/export?format=csv',
        'department_reorder_rates.csv': 'https://docs.google.com/spreadsheets/d/18pDHrwkLO2EhSeZJRex_YqmJJrsQn_CN/export?format=csv',
        'product_reorder_rates.csv': 'https://docs.google.com/spreadsheets/d/1kMfYPfgUg-7-iJv5JKShPLq38ZewM4L6/export?format=csv',
        'user_segments.csv': 'https://docs.google.com/spreadsheets/d/1oOLBLlqame7P6SudMn7BRs2dw3SCkL29/export?format=csv',
        'segment_recommendations.csv': 'https://docs.google.com/spreadsheets/d/1d1230vkstrXnf12hWnhTG2bTlDLsJ4NRB/export?format=csv'
    }
    
    for filename, url in export_urls.items():
        filepath = f'data/processed/{filename}'
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            gdown.download(url, filepath, quiet=False, fuzzy=True)
            print(f"Downloaded {filename}")

# Ensure data files exist before loading
ensure_data_files()

# Load data
@st.cache_data
def load_data():
    predictions = pd.read_csv('data/processed/predictions_with_details.csv')
    dept_rates = pd.read_csv('data/processed/department_reorder_rates.csv')
    product_rates = pd.read_csv('data/processed/product_reorder_rates.csv')
    segments = pd.read_csv('data/processed/user_segments.csv')
    recommendations = pd.read_csv('data/processed/segment_recommendations.csv')
    return predictions, dept_rates, product_rates, segments, recommendations

predictions, dept_rates, product_rates, segments, recommendations = load_data()

# Sidebar navigation
st.sidebar.title("🛒 Instacart Analytics")
page = st.sidebar.radio("Navigate", [
    "📊 Executive Overview",
    "🎯 Product Recommendations",
    "📈 Product Intelligence",
    "👥 Customer Segments",
    "🔍 Model Insights"
])

# Add spacing to push footer down
for _ in range(32):
    st.sidebar.write("")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Built by Ashik Rahman**")
st.sidebar.markdown("Data Scientist")

# Page 1: Executive Overview
if page == "📊 Executive Overview":
    st.title("📊 Executive Overview")
    st.markdown("*Machine learning model predicting which products customers will reorder, enabling targeted marketing and optimized inventory management*")
    st.markdown("")
    
    # Top metrics - business focused
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Prediction Accuracy", "83%", help="Model correctly identifies reorder patterns")
    with col2:
        st.metric("High-Confidence Predictions", "668K", delta="13.8%", help="Predictions with >70% probability")
    with col3:
        st.metric("Total Predictions", "4.8M", help="Customer-product pairs analyzed")
    with col4:
        st.metric("Customers Analyzed", "75,000", help="Unique users in analysis")
    
    st.markdown("---")
    
    # Two column layout with visuals
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Potential Use Cases")
        
        # Colored boxes for use cases
        st.success("**📧 Personalized Email Campaigns**  \nTarget customers with products they're 83% likely to reorder")
        
        st.info("**📦 Inventory Planning**  \nPredict demand for 668K high-confidence reorders")
        
        st.warning("**🎁 Smart Promotions**  \nFocus discounts on exploratory shoppers (37K users)")
        
        st.markdown("")
        st.subheader("💡 Key Insights")
        st.markdown("🔹 **Recency is critical**: Products bought in the last order are 3x more important than frequency")
        st.markdown("🔹 **Essentials lead**: Dairy/Eggs and Produce both have 12.9% reorder rates (vs 9.8% overall)")
        st.markdown("🔹 **Mixed loyalty dominates**: 41K users (32%) show mixed loyalty patterns")
        st.markdown("🔹 **Typical behavior**: Users purchase ~10 items per order, have tried 65 unique products")
        st.markdown("🔹 **Fresh dominates**: Top reorderable products are fresh produce and dairy")
    
    with col2:
        st.subheader("📊 Category Performance")
        
        # Top 5 departments chart
        top_5_depts = dept_rates.nlargest(5, 'reorder_rate')
        fig = px.bar(top_5_depts, y='department', x='reorder_rate', 
                     orientation='h',
                     labels={'reorder_rate': 'Reorder Rate', 'department': ''},
                     color='reorder_rate',
                     color_continuous_scale='Blues')
        fig.update_layout(height=300, showlegend=False, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Customer segment pie chart with different colors
        st.subheader("👥 Customer Mix")
        
        segment_summary = pd.DataFrame({
            'Segment': ['Exploratory (29%)', 'Mixed Loyalty (32%)', 'Loyal (26%)', 'Very Loyal (12%)'],
            'Count': [37324, 41411, 34744, 15788]
        })
        
        fig2 = px.pie(segment_summary, values='Count', names='Segment', 
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig2.update_layout(height=300, showlegend=True)
        fig2.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig2, use_container_width=True)

# Page 2: Product Recommendations
elif page == "🎯 Product Recommendations":
    st.title("🎯 Product Recommendation Engine")
    st.write("Enter a customer ID to generate personalized product recommendations based on their purchase history and predicted reorder probabilities.")
    
    # Debug: Check column names
    if 'user_id' not in predictions.columns:
        st.error(f"Available columns: {predictions.columns.tolist()}")
        st.stop()
    
    valid_users = sorted(predictions['user_id'].unique())
    
    col1, col2 = st.columns([1, 3])
    with col1:
        user_id = st.selectbox("Select User ID:", 
                               options=valid_users,
                               index=valid_users.index(45082) if 45082 in valid_users else 0)
        get_recs = st.button("Get Recommendations", type="primary")
    
    if get_recs:
        user_preds = predictions[predictions['user_id'] == user_id].sort_values(
            'reorder_probability', ascending=False
        ).head(10)
        
        st.markdown(f"### Top 10 Predictions for User {user_id}")
        
        col1, col2 = st.columns([2, 3])
        
        with col1:
            display_df = user_preds[['product_name', 'department', 'reorder_probability']].copy()
            display_df['reorder_probability'] = (display_df['reorder_probability'] * 100).round(1).astype(str) + '%'
            display_df.columns = ['Product', 'Department', 'Probability']
            st.dataframe(display_df, use_container_width=True, hide_index=True, height=400)
        
        with col2:
            fig = px.bar(user_preds.head(10), x='reorder_probability', y='product_name',
                        orientation='h', color='department',
                        labels={'reorder_probability': 'Reorder Probability', 'product_name': ''})
            fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
            st.plotly_chart(fig, use_container_width=True)

# Page 3: Product Intelligence
elif page == "📈 Product Intelligence":
    st.title("📈 Product Intelligence")
    st.markdown("*Analyze reorder patterns across departments and products to identify high-performing categories and optimize product placement*")
    st.markdown("")
    
    tab1, tab2 = st.tabs(["📊 By Department", "🏆 Top Products"])
    
    with tab1:
        st.subheader("Reorder Rates by Department")
        
        fig = px.bar(dept_rates.sort_values('reorder_rate', ascending=True), 
                     x='reorder_rate', y='department', orientation='h',
                     labels={'reorder_rate': 'Reorder Rate', 'department': 'Department'},
                     color='reorder_rate',
                     color_continuous_scale='Viridis')
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📋 View detailed data"):
            st.dataframe(dept_rates.sort_values('reorder_rate', ascending=False), 
                        use_container_width=True, hide_index=True)
        
        # SEPARATED: Key Findings vs Suggested Strategies
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Key Findings")
            st.info("**Highest Reorder Rates**\n\nDairy/Eggs (12.9%) and Produce (12.9%) lead all departments")
            st.success("**Above Average**\n\nBeverages (12.7%), Missing (11.8%), and Pets (11.4%) exceed the 9.8% overall rate")
            st.warning("**Lowest Reorder Rates**\n\nPersonal Care (3.8%), Pantry (3.8%), and International (4.2%) are significantly below average")
        
        with col2:
            st.subheader("💡 Suggested Strategies")
            st.info("**Leverage Essentials**\n\nPromote high-frequency items (dairy, produce) as traffic drivers")
            st.success("**Category Bundling**\n\nPair high-reorder categories (beverages, pets) with complementary products")
            st.warning("**Low-Reorder Focus**\n\nTest promotional campaigns or product variety adjustments for personal care, pantry, international")
    
    with tab2:
        st.subheader("Top 20 Products by Reorder Rate")
        st.caption("Minimum 1,000 purchases required for statistical significance")
        
        top_products = product_rates.head(20)
        fig = px.bar(top_products, x='reorder_rate', y='product_name',
                    orientation='h', color='department',
                    labels={'reorder_rate': 'Reorder Rate', 'product_name': ''})
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # SEPARATED: Key Findings vs Suggested Strategies
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Key Findings")
            st.info("**Fresh Products Dominate**\n\nAll top 20 products are fresh produce or dairy items")
            st.success("**Banana Leadership**\n\nRegular banana: 35.3% reorder rate with 46,964 total purchases - highest on both metrics")
            st.warning("**Organic Presence**\n\nMultiple organic variants appear in top 20, showing strong organic customer loyalty")
        
        with col2:
            st.subheader("💡 Suggested Strategies")
            st.info("**Feature Fresh Items**\n\nHighlight fresh produce/dairy in marketing - these drive repeat purchases")
            st.success("**Optimize Banana Placement**\n\nEnsure prominent positioning and stock levels for banana variants")
            st.warning("**Expand Organic**\n\nConsider increasing organic product selection given strong reorder patterns")

# Page 4: Customer Segments
elif page == "👥 Customer Segments":
    st.title("👥 Customer Segmentation")
    st.markdown("*Customer segments based on shopping frequency and loyalty patterns, with tailored strategies for each group*")
    st.markdown("")
    
    # Visualization of top segments
    st.subheader("Customer Distribution by Segment")
    
    top_10_segments = segments.head(10).copy()
    top_10_segments['segment_label'] = (top_10_segments['shopping_frequency'] + ' | ' + 
                                        top_10_segments['loyalty'])
    
    fig = px.bar(top_10_segments, x='user_count', y='segment_label',
                 orientation='h', 
                 labels={'user_count': 'Number of Users', 'segment_label': 'Segment'},
                 color='user_count',
                 color_continuous_scale='Blues')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Recommended actions full width on top
    st.subheader("💡 Suggested Strategies by Segment")
    st.dataframe(recommendations, use_container_width=True, hide_index=True)
    
    st.markdown("")
    
    # Segment details below
    st.subheader("📊 Detailed Segment Breakdown")
    with st.expander("View all segment details"):
        st.dataframe(segments.head(15), use_container_width=True, hide_index=True)
    
    # SEPARATED: Key Findings only
    st.markdown("---")
    st.subheader("📊 Segmentation Findings")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Largest Segment**\n\nInfrequent + Exploratory (23,661 users, 18%) with 9.79 avg basket size and 37 products tried")
        st.success("**Highest Engagement**\n\nModerate + Mixed (15,401 users, 12%) with 10.49 basket size and 81 products tried")
    with col2:
        st.warning("**Most Loyal**\n\nVery Frequent + Very Loyal (12,394 users, 9%) with 11.24 basket size and 523 products tried")
        st.error("**High Experience**\n\nVery Frequent + Loyal (13,930 users, 11%) with 350 products tried - experienced but selective")

# Page 5: Model Insights
elif page == "🔍 Model Insights":
    st.title("🔍 Model Performance & Insights")
    st.markdown("*Technical details on model performance, feature importance, and the factors driving reorder predictions*")
    st.markdown("")
    
    st.subheader("Model Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ROC-AUC", "0.8291")
        st.caption("Strong discriminative ability")
    with col2:
        st.metric("Best F1", "0.4312")
        st.caption("At threshold 0.7127")
    with col3:
        st.metric("Training Size", "8.47M")
        st.caption("9.78% positive class")
    
    st.markdown("---")
    
    st.subheader("🔑 Feature Importance")
    st.markdown("What drives reorder predictions?")
    
    feature_importance = pd.DataFrame({
        'Feature': ['Orders Since Last Purchase', 'User-Product Order Count', 
                   'Product Reorder Probability', 'User Total Orders', 'User-Product Reorder Count'],
        'Importance': [21400000, 6780000, 1780000, 1380000, 517000],
        'Description': [
            'How many orders ago user bought this product',
            'How many times this user bought this specific product',
            'How often this product is reordered by all users',
            'Total number of orders by this user',
            'How many times user reordered this specific product'
        ]
    })
    
    fig = px.bar(feature_importance, x='Importance', y='Feature', orientation='h',
                labels={'Importance': 'Importance Score', 'Feature': ''},
                color='Importance',
                color_continuous_scale='Teal')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    with st.expander("📋 Feature Details"):
        st.dataframe(feature_importance, use_container_width=True, hide_index=True)
    
    # Model findings - equal sized columns
    st.markdown("---")
    st.subheader("📊 Model Findings")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Recency Dominates**\n\nTop feature is 3.2x more important than second")
    with col2:
        st.warning("**Handles Imbalance**\n\n83% AUC with 9.2:1 class ratio")
    with col3:
        st.success("**Balanced Model**\n\n43% F1 at 0.71 threshold")