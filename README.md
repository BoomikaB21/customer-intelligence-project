# 🎯 Customer Intelligence Dashboard

A professional SaaS-style Customer Intelligence platform built with Streamlit. Analyze customer behavior using RFM segmentation, predict VIP customers with Machine Learning, and track real-time events with a modern, production-ready interface.

**🚀 [Live Demo](https://customer-intelligence-project-9wxktxigoymdmhfgdwqtfm.streamlit.app)**

---

## ✨ Features

### 📊 Analytics & Insights
- **RFM Segmentation** - Recency, Frequency, Monetary analysis for customer behavior
- **Customer Metrics** - Real-time KPIs: Total customers, revenue, purchase frequency
- **Interactive Charts** - Plotly-powered visualizations for segment distribution
- **Data Explorer** - Browse detailed customer data with filtering by segment

### 🤖 Machine Learning
- **VIP Prediction** - RandomForest classifier to identify high-value customers
- **Automated Classification** - Scores customers based on RFM metrics
- **Real-time Predictions** - Predict customer value on-demand

### 🔐 Security & Authentication
- **Login System** - Secure user authentication with hashed credentials
- **Session Management** - Streamlit session state for user context
- **Firebase Ready** - Optional Firebase Auth and Firestore integration

### 📡 Real-Time Features
- **Live Event Stream** - Real-time activity feed with event simulation
- **Event Logging** - Automatic logging of all user actions to database
- **Database Audit Trail** - Complete history of logins, predictions, and interactions

### 🎨 Professional UI/UX
- **Dark Premium Theme** - Modern gradient background with glass-style panels
- **Responsive Design** - Works seamlessly on desktop and mobile
- **Custom CSS** - Professional styling with Streamlit customization
- **Intuitive Navigation** - Clean, organized dashboard layout

---

## 🏗️ Architecture

### Tech Stack
- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python with modular architecture
- **Database**: SQLite (local) / Firebase Firestore (optional)
- **ML**: scikit-learn (RandomForest classifier)
- **Data**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Streamlit Cloud

### Project Structure
```
customer_project/
├── src/
│   ├── app.py                 # Main Streamlit app & UI
│   ├── model.py               # ML model training & prediction
│   ├── utils.py               # Data loading & RFM computation
│   ├── database.py            # Database abstraction layer
│   ├── backend.py             # Local/Firebase backend switching
│   ├── stream_service.py      # Real-time event stream simulation
│   └── firebase_auth.py       # Firebase authentication hooks
├── data/
│   ├── retail.csv             # Sample ecommerce transaction data
│   └── rfm.csv                # Computed RFM metrics
├── .streamlit/
│   ├── config.toml            # Streamlit configuration
│   └── secrets_template.toml  # Secrets management template
├── requirements.txt           # Python dependencies
├── .env                       # Environment configuration
├── .env.example               # Example env template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Option 1: Run Locally

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Installation
```bash
# Clone the repository
git clone https://github.com/BoomikaB21/customer-intelligence-project.git
cd customer_project

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

**Default Login Credentials:**
- Username: `admin`
- Password: `admin123`

### Option 2: Deploy to Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "Create app"
4. Select your repository
5. Set main file path to `src/app.py`
6. Click Deploy

Your app will be live in 1-2 minutes!

---

## 📖 Usage Guide

### Login
1. Enter username: `admin`
2. Enter password: `admin123`
3. Click "Login"

### Dashboard Navigation

#### Metrics Section
View real-time KPIs:
- Total customers in database
- Total revenue generated
- Average purchase frequency
- Current logged-in user

#### Segment Filter
Select a customer segment to view segment-specific analytics:
- All (default)
- High-Value
- Medium-Value
- Low-Value

#### Segment Distribution
Interactive bar chart showing customer count per segment

#### Customer Data
Browse detailed RFM metrics for all customers in the selected segment

#### Predict Customer Value
Enter customer metrics to predict if they're a VIP:
1. Enter Recency (days since last purchase)
2. Enter Frequency (number of purchases)
3. Enter Monetary (total spent)
4. Click "Predict"

Result: **VIP Customer** or **Normal Customer**

#### Live Event Stream
Real-time feed of simulated customer events

#### Recent Database Events
Audit trail of all actions logged to the database

---

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Backend Mode (local or firebase)
USE_FIREBASE=0

# Firebase Configuration (if USE_FIREBASE=1)
FIREBASE_CREDENTIALS_PATH=path/to/serviceAccountKey.json
```

### Streamlit Configuration
Edit `.streamlit/config.toml` for customization:
- Theme colors
- Page layout (wide vs centered)
- Server settings
- Client settings

---

## 🗄️ Database

### Local Database (Default)
- **Type**: SQLite
- **Location**: `data/customer_app.db`
- **Tables**:
  - `users` - User accounts with hashed passwords
  - `events` - Activity log (logins, predictions, etc.)

### Firebase Database (Optional)
To enable Firebase:

1. Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
2. Create a service account and download JSON key
3. Update `.env`:
   ```env
   USE_FIREBASE=1
   FIREBASE_CREDENTIALS_PATH=path/to/serviceAccountKey.json
   ```
4. Set secrets in Streamlit Cloud dashboard

---

## 🤖 Machine Learning Model

### Model Type
- **Algorithm**: Random Forest Classifier
- **Target Variable**: VIP customer (binary classification)
- **Features**: Recency, Frequency, Monetary

### Training Data
- Uses computed RFM metrics from retail transaction data
- Customers with high monetary value labeled as VIP
- Model trained on 80/20 split (default)

### Predictions
- Real-time inference on new customer data
- Returns: VIP (1) or Normal (0)
- Prediction logged to database

### Model File Location
- Trained model stored in memory during session
- Retrained on app startup from RFM data

---

## 📊 Data Pipeline

### Step 1: Raw Data Loading
- Source: `data/retail.csv`
- Columns: InvoiceNo, StockCode, Quantity, UnitPrice, InvoiceDate, CustomerID, etc.
- Data cleaning: Removes nulls, negative quantities, zero prices

### Step 2: RFM Computation
For each customer:
- **Recency**: Days since last purchase
- **Frequency**: Total number of purchases
- **Monetary**: Total amount spent

### Step 3: Segmentation
Customers grouped into segments based on RFM scores:
- High-Value: High R, F, M
- Medium-Value: Medium scores
- Low-Value: Low scores

### Step 4: ML Training
RandomForest trained to classify VIP vs Normal customers

### Output
- RFM data stored in `data/rfm.csv`
- Model ready for predictions

---

## 🔐 Security Features

### Authentication
- ✅ Password hashing (SHA-256)
- ✅ Login session management
- ✅ User context tracking

### Data Protection
- ✅ HTTPS/TLS encryption (Streamlit Cloud)
- ✅ Secure credential storage
- ✅ Environment variable isolation

### Audit Trail
- ✅ All actions logged to database
- ✅ User attribution for events
- ✅ Timestamp recording

### Future Enhancements
- 🔒 OAuth2/Google Sign-In
- 🔒 Role-based access control (RBAC)
- 🔒 Data encryption at rest
- 🔒 API rate limiting

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | ≥1.28.0 | Web framework |
| pandas | ≥2.0.0 | Data manipulation |
| numpy | ≥1.24.0 | Numerical computing |
| scikit-learn | ≥1.3.0 | Machine learning |
| plotly | ≥5.17.0 | Interactive charts |
| firebase-admin | ≥6.2.0 | Firebase integration |
| python-dotenv | ≥1.0.0 | Environment management |

---

## 🚢 Deployment

### Streamlit Cloud (Recommended)
- **Pros**: Easiest, free tier available, automatic scaling, HTTPS
- **Cons**: Limited to Python/Streamlit apps
- **URL**: https://customer-intelligence-project-9wxktxigoymdmhfgdwqtfm.streamlit.app

### AWS
- **Services**: EC2, RDS, S3
- **Pros**: Full control, scalable
- **Cons**: Requires DevOps knowledge

### Google Cloud Run
- **Pros**: Serverless, pay-per-use
- **Cons**: More complex setup

### Heroku
- **Pros**: Simple deployment
- **Cons**: Free tier removed (paid plans start at $7/month)

---

## 🐛 Troubleshooting

### App won't start locally
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Run with debug output
streamlit run src/app.py --logger.level=debug
```

### Login not working
- Default credentials: `admin` / `admin123`
- Check database file exists: `data/customer_app.db`
- Try in incognito/private mode if issues persist

### Port already in use
```bash
# Use different port
streamlit run src/app.py --server.port 8502
```

### Firebase connection errors
- Verify credentials JSON path in `.env`
- Check Firebase project has Firestore/Auth enabled
- Ensure service account has required permissions

---

## 📈 Performance Optimization

### Local
- RFM computation cached during session
- Model loaded once on app start
- SQLite queries indexed on frequently searched fields

### Cloud
- Streamlit Cloud auto-scales
- Consider upgrading to Pro tier for more resources
- Cache large datasets with `@st.cache_data`

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 💡 Future Roadmap

- [ ] Advanced segmentation (K-means clustering)
- [ ] Cohort analysis
- [ ] Churn prediction
- [ ] Customer lifetime value (CLV) modeling
- [ ] A/B testing framework
- [ ] Data export (CSV, Excel, PDF)
- [ ] Multi-user workspaces
- [ ] Advanced data filtering and search
- [ ] API endpoint for external integrations
- [ ] Mobile app (React Native/Flutter)

---

## 📞 Support

### Documentation
- [Streamlit Docs](https://docs.streamlit.io)
- [scikit-learn Docs](https://scikit-learn.org)
- [Pandas Docs](https://pandas.pydata.org/docs)

### Issues & Questions
- Open an issue on GitHub
- Check existing issues for solutions
- Contact support via GitHub Discussions

---

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- ML with [scikit-learn](https://scikit-learn.org)
- Data with [Pandas](https://pandas.pydata.org)
- Visualizations with [Plotly](https://plotly.com)

---

## 📊 Project Status

- ✅ Core functionality complete
- ✅ Professional UI implemented
- ✅ Cloud deployment ready
- ✅ Firebase integration prepared
- 🚀 Production ready

**Last Updated**: August 2026

---

**Made with ❤️ for data-driven decision making**
